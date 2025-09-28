#!/usr/bin/env python3
"""
GTMSetupService CRM Database Manager
Handles SQLite database operations for the complete pipeline
"""

import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class CRMDatabase:
    def __init__(self, db_path: str = "crm/gtm_crm.db"):
        """Initialize database connection and ensure schema exists"""
        self.db_path = db_path
        self.ensure_database_exists()

    def ensure_database_exists(self):
        """Create database and tables if they don't exist"""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        # Initialize database with schema
        with sqlite3.connect(self.db_path) as conn:
            # Read and execute schema
            schema_path = "crm/init_database.sql"
            if os.path.exists(schema_path):
                with open(schema_path, 'r') as f:
                    conn.executescript(f.read())

    def add_reddit_post(self, post_url: str, username: str, subreddit: str,
                       title: str, content: str = "", problem_category: str = "",
                       business_size: str = "", urgency: str = "",
                       agent_discovered: str = "") -> int:
        """Add a new Reddit post to the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reddit_posts
                (post_url, username, subreddit, title, content, problem_category,
                 business_size_indicator, urgency_level, agent_discovered)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (post_url, username, subreddit, title, content, problem_category,
                  business_size, urgency, agent_discovered))

            post_id = cursor.lastrowid

            # Add to pipeline at discovered stage
            cursor.execute("""
                INSERT INTO pipeline_stages (post_id, stage, agent_updated)
                VALUES (?, 'discovered', ?)
            """, (post_id, agent_discovered))

            # Add/update audience member
            self.add_audience_member(username, problem_category)

            return post_id

    def add_solution(self, post_id: int, solution_text: str, estimated_value: float,
                    complexity: str, service_type: str, hours: int = 0) -> int:
        """Add a solution for a Reddit post"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO solutions
                (post_id, solution_text, estimated_value, complexity_level,
                 service_type, implementation_hours)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (post_id, solution_text, estimated_value, complexity, service_type, hours))
            return cursor.lastrowid

    def add_response_analysis(self, post_id: int, existing_responses: str,
                            should_respond: bool, reason: str,
                            competitive_analysis: str = "", score: int = 5,
                            analyzed_by: str = "") -> int:
        """Add response analysis for a post"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO response_analysis
                (post_id, existing_responses, should_respond, reason,
                 competitive_analysis, response_quality_score, analyzed_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (post_id, existing_responses, should_respond, reason,
                  competitive_analysis, score, analyzed_by))
            return cursor.lastrowid

    def add_our_response(self, post_id: int, response_text: str,
                        engagement_level: str = "helpful",
                        follow_up_needed: bool = False,
                        dm_initiated: bool = False,
                        agent_type: str = "prospecting") -> int:
        """Record that we responded to a post"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO our_responses
                (post_id, response_text, engagement_level, follow_up_needed,
                 dm_initiated, agent_type)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (post_id, response_text, engagement_level, follow_up_needed,
                  dm_initiated, agent_type))

            # Update pipeline stage
            self.update_pipeline_stage(post_id, "responded", agent_type)

            return cursor.lastrowid

    def update_pipeline_stage(self, post_id: int, stage: str, agent_updated: str = "",
                             notes: str = ""):
        """Update the pipeline stage for a post"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pipeline_stages (post_id, stage, notes, agent_updated)
                VALUES (?, ?, ?, ?)
            """, (post_id, stage, notes, agent_updated))

    def add_audience_member(self, username: str, service_interest: str = "",
                           business_type: str = ""):
        """Add or update audience member"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO audience_members
                (username, last_interaction_date, primary_service_interest,
                 business_type, interaction_count)
                VALUES (?, CURRENT_DATE, ?, ?,
                        COALESCE((SELECT interaction_count FROM audience_members WHERE username = ?) + 1, 1))
            """, (username, service_interest, business_type, username))

    def add_content_opportunity(self, post_id: int, content_type: str,
                              angle: str = "", priority: int = 5) -> int:
        """Flag a post as a content opportunity"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO content_opportunities
                (post_id, content_type, angle, priority_level)
                VALUES (?, ?, ?, ?)
            """, (post_id, content_type, angle, priority))
            return cursor.lastrowid

    def get_active_prospects(self, service_type: str = "") -> List[Dict]:
        """Get all active prospects, optionally filtered by service type"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = """
                SELECT * FROM active_prospects
                WHERE (? = '' OR problem_category = ?)
                ORDER BY discovered_date DESC
            """
            cursor.execute(query, (service_type, service_type))
            return [dict(row) for row in cursor.fetchall()]

    def get_pipeline_summary(self) -> Dict:
        """Get pipeline summary across all stages"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM conversion_pipeline")
            pipeline_data = [dict(row) for row in cursor.fetchall()]

            # Get total counts by stage
            cursor.execute("""
                SELECT stage, COUNT(*) as count
                FROM pipeline_stages ps
                JOIN reddit_posts rp ON ps.post_id = rp.id
                WHERE ps.id IN (
                    SELECT MAX(id) FROM pipeline_stages GROUP BY post_id
                )
                GROUP BY stage
                ORDER BY
                    CASE stage
                        WHEN 'discovered' THEN 1
                        WHEN 'analyzed' THEN 2
                        WHEN 'responded' THEN 3
                        WHEN 'dm_active' THEN 4
                        WHEN 'qualified' THEN 5
                        WHEN 'proposal_sent' THEN 6
                        WHEN 'won' THEN 7
                        WHEN 'lost' THEN 8
                        ELSE 9
                    END
            """)
            stage_counts = dict(cursor.fetchall())

            return {
                'by_category_and_stage': pipeline_data,
                'by_stage': stage_counts
            }

    def get_recent_activity(self, days: int = 7) -> Dict:
        """Get recent activity summary"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Posts discovered in last N days
            cursor.execute("""
                SELECT COUNT(*) as count, problem_category
                FROM reddit_posts
                WHERE discovered_date >= date('now', '-' || ? || ' days')
                GROUP BY problem_category
            """, (days,))
            recent_posts = dict(cursor.fetchall())

            # Responses sent in last N days
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM our_responses
                WHERE response_date >= date('now', '-' || ? || ' days')
            """, (days,))
            recent_responses = cursor.fetchone()['count']

            return {
                'posts_discovered': recent_posts,
                'responses_sent': recent_responses,
                'period_days': days
            }

    def search_posts(self, keyword: str, service_type: str = "") -> List[Dict]:
        """Search posts by keyword in title or content"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = """
                SELECT rp.*, ps.stage, ps.stage_date
                FROM reddit_posts rp
                LEFT JOIN pipeline_stages ps ON rp.id = ps.post_id
                WHERE (rp.title LIKE ? OR rp.content LIKE ?)
                AND (? = '' OR rp.problem_category = ?)
                ORDER BY rp.discovered_date DESC
            """
            search_term = f"%{keyword}%"
            cursor.execute(query, (search_term, search_term, service_type, service_type))
            return [dict(row) for row in cursor.fetchall()]

# Utility functions for agents
def get_crm() -> CRMDatabase:
    """Get CRM database instance"""
    return CRMDatabase()

def log_prospect_discovery(post_url: str, username: str, subreddit: str,
                         title: str, content: str, category: str,
                         agent_name: str) -> int:
    """Convenient function for agents to log new prospects"""
    crm = get_crm()
    return crm.add_reddit_post(
        post_url=post_url,
        username=username,
        subreddit=subreddit,
        title=title,
        content=content,
        problem_category=category,
        agent_discovered=agent_name
    )

def log_response_decision(post_id: int, should_respond: bool, reason: str,
                         existing_responses: str, agent_name: str) -> int:
    """Log the decision about whether to respond to a post"""
    crm = get_crm()
    return crm.add_response_analysis(
        post_id=post_id,
        existing_responses=existing_responses,
        should_respond=should_respond,
        reason=reason,
        analyzed_by=agent_name
    )

def log_our_response(post_id: int, response_text: str, agent_name: str) -> int:
    """Log that we responded to a post"""
    crm = get_crm()
    return crm.add_our_response(
        post_id=post_id,
        response_text=response_text,
        agent_type=agent_name
    )

if __name__ == "__main__":
    # Initialize database
    crm = CRMDatabase()
    print("✅ CRM Database initialized successfully")

    # Test basic functionality
    print("\n📊 Pipeline Summary:")
    summary = crm.get_pipeline_summary()
    for stage, count in summary['by_stage'].items():
        print(f"  {stage}: {count}")