-- GTMSetupService CRM Database Schema
-- Complete prospect-to-content pipeline tracking

PRAGMA foreign_keys = ON;

-- Reddit Posts/Problems (The source material)
CREATE TABLE IF NOT EXISTS reddit_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_url TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    subreddit TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    discovered_date DATE DEFAULT CURRENT_DATE,
    problem_category TEXT, -- GTM, Shopify, WordPress
    business_size_indicator TEXT, -- small, medium, enterprise
    urgency_level TEXT, -- low, medium, high, emergency
    service_type TEXT, -- prospect, support, mixed
    agent_discovered TEXT, -- which agent found this
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Our Solutions (What we'd provide)
CREATE TABLE IF NOT EXISTS solutions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    solution_text TEXT NOT NULL,
    estimated_value DECIMAL(10,2),
    complexity_level TEXT, -- simple, moderate, complex
    service_type TEXT NOT NULL, -- GTM, Shopify, WordPress
    implementation_hours INTEGER,
    solution_category TEXT, -- emergency, standard, maintenance
    created_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES reddit_posts(id) ON DELETE CASCADE
);

-- Response Analysis (Your "stepping on dick" evaluation)
CREATE TABLE IF NOT EXISTS response_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    existing_responses TEXT,
    should_respond BOOLEAN DEFAULT 0,
    reason TEXT,
    competitive_analysis TEXT,
    response_quality_score INTEGER, -- 1-10 scale
    engagement_potential TEXT, -- low, medium, high
    analysis_date DATE DEFAULT CURRENT_DATE,
    analyzed_by TEXT, -- which agent did the analysis
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES reddit_posts(id) ON DELETE CASCADE
);

-- Actual Responses (If we decide to engage)
CREATE TABLE IF NOT EXISTS our_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    response_text TEXT NOT NULL,
    response_date DATE DEFAULT CURRENT_DATE,
    engagement_level TEXT, -- helpful, diagnostic, referral
    follow_up_needed BOOLEAN DEFAULT 0,
    dm_initiated BOOLEAN DEFAULT 0,
    conversion_potential TEXT, -- low, medium, high
    agent_type TEXT, -- prospecting, support
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES reddit_posts(id) ON DELETE CASCADE
);

-- Content Opportunities (Case studies, blog posts, etc.)
CREATE TABLE IF NOT EXISTS content_opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    content_type TEXT NOT NULL, -- case_study, blog_post, video, linkedin
    angle TEXT,
    potential_reach TEXT,
    content_status TEXT DEFAULT 'planned', -- planned, created, published
    priority_level INTEGER DEFAULT 5, -- 1-10 scale
    target_audience TEXT,
    estimated_engagement INTEGER,
    created_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES reddit_posts(id) ON DELETE CASCADE
);

-- Pipeline Stages (Track prospect progression)
CREATE TABLE IF NOT EXISTS pipeline_stages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    stage TEXT NOT NULL, -- discovered, analyzed, responded, dm_active, qualified, proposal_sent, won, lost
    stage_date DATE DEFAULT CURRENT_DATE,
    notes TEXT,
    agent_updated TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES reddit_posts(id) ON DELETE CASCADE
);

-- Audience Tracking (Reddit users we've interacted with)
CREATE TABLE IF NOT EXISTS audience_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    first_interaction_date DATE DEFAULT CURRENT_DATE,
    last_interaction_date DATE DEFAULT CURRENT_DATE,
    interaction_count INTEGER DEFAULT 1,
    primary_service_interest TEXT, -- GTM, Shopify, WordPress
    business_type TEXT,
    engagement_score INTEGER DEFAULT 0, -- 0-100 scale
    conversion_status TEXT DEFAULT 'prospect', -- prospect, client, lost
    lifetime_value DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Link audience members to specific posts
CREATE TABLE IF NOT EXISTS audience_interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    audience_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    interaction_type TEXT, -- viewed, responded, dm_received
    interaction_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (audience_id) REFERENCES audience_members(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES reddit_posts(id) ON DELETE CASCADE
);

-- Client Projects (When prospects convert)
CREATE TABLE IF NOT EXISTS client_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    audience_id INTEGER,
    project_name TEXT NOT NULL,
    service_type TEXT NOT NULL, -- GTM, Shopify, WordPress
    project_value DECIMAL(10,2),
    start_date DATE,
    end_date DATE,
    status TEXT DEFAULT 'planning', -- planning, active, completed, cancelled
    source_post_id INTEGER, -- Which Reddit post led to this
    project_manager TEXT DEFAULT 'PM Agent',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (audience_id) REFERENCES audience_members(id),
    FOREIGN KEY (source_post_id) REFERENCES reddit_posts(id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_reddit_posts_date ON reddit_posts(discovered_date);
CREATE INDEX IF NOT EXISTS idx_reddit_posts_category ON reddit_posts(problem_category);
CREATE INDEX IF NOT EXISTS idx_reddit_posts_subreddit ON reddit_posts(subreddit);
CREATE INDEX IF NOT EXISTS idx_pipeline_stages_post ON pipeline_stages(post_id);
CREATE INDEX IF NOT EXISTS idx_pipeline_stages_stage ON pipeline_stages(stage);
CREATE INDEX IF NOT EXISTS idx_audience_username ON audience_members(username);
CREATE INDEX IF NOT EXISTS idx_audience_service ON audience_members(primary_service_interest);

-- Views for common queries
CREATE VIEW IF NOT EXISTS active_prospects AS
SELECT
    rp.*,
    ps.stage,
    ps.stage_date,
    am.username as audience_username,
    am.engagement_score
FROM reddit_posts rp
LEFT JOIN pipeline_stages ps ON rp.id = ps.post_id
LEFT JOIN audience_members am ON rp.username = am.username
WHERE ps.stage NOT IN ('won', 'lost') OR ps.stage IS NULL
ORDER BY rp.discovered_date DESC;

CREATE VIEW IF NOT EXISTS conversion_pipeline AS
SELECT
    rp.problem_category,
    ps.stage,
    COUNT(*) as count,
    AVG(s.estimated_value) as avg_value
FROM reddit_posts rp
LEFT JOIN pipeline_stages ps ON rp.id = ps.post_id
LEFT JOIN solutions s ON rp.id = s.post_id
GROUP BY rp.problem_category, ps.stage;

-- Initial data placeholder (removed problematic foreign key insert)