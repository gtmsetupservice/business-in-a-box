---
name: CRM Workflow & Database
description: Manage the PostgreSQL CRM database for prospect tracking, solution documentation, content creation, and client project management. Use when working with prospects, creating content, logging interactions, or querying business data.
---

# CRM Workflow & Database

The CRM database is the central hub for all business operations: prospecting, problem documentation, solution creation, content production, and client management.

## Database Connection

**Host:** 192.168.0.150
**Port:** 5432
**Database:** crm
**User:** crm_admin
**Password:** Available in .env file (CRM_POSTGRES_PASSWORD)

Connection string:
```bash
PGPASSWORD=$CRM_POSTGRES_PASSWORD psql -h $CRM_POSTGRES_HOST -p $CRM_POSTGRES_PORT -U $CRM_POSTGRES_USER -d $CRM_POSTGRES_DB
```

## Core Workflow

```
1. Prospect Discovery (Reddit)
   ↓
2. Problem Analysis
   ↓
3. Solution Creation
   ↓
4. Response & Engagement
   ↓
5. Content Creation (Case Studies, Blog Posts, Videos)
   ↓
6. Client Conversion
```

## Database Tables & Relationships

### 1. reddit_posts (Source of Prospects)
Central table that all other tables reference.

**Key Fields:**
- `post_url` - Unique Reddit post URL
- `username` - Reddit username
- `subreddit` - Where discovered
- `title`, `content` - Problem description
- `problem_category` - GTM, Shopify, WordPress
- `urgency_level` - low, medium, high, emergency
- `service_type` - prospect, support, mixed
- `agent_discovered` - Which agent found this

**Common Query:**
```sql
SELECT * FROM reddit_posts
WHERE problem_category = 'GTM'
  AND urgency_level IN ('high', 'emergency')
  AND discovered_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY discovered_date DESC;
```

### 2. solutions (Problem Solutions)
Links to `reddit_posts.id`

**Key Fields:**
- `post_id` - Foreign key to reddit_posts
- `solution_text` - How to solve the problem
- `estimated_value` - Revenue potential
- `complexity_level` - simple, moderate, complex
- `service_type` - GTM, Shopify, WordPress
- `implementation_hours` - Time estimate

**Common Query:**
```sql
SELECT rp.title, s.solution_text, s.estimated_value, s.complexity_level
FROM reddit_posts rp
JOIN solutions s ON rp.id = s.post_id
WHERE s.service_type = 'WordPress'
ORDER BY s.estimated_value DESC;
```

### 3. pipeline_stages (Prospect Progression)
Tracks movement through sales pipeline. Links to `reddit_posts.id`

**Pipeline Stages (in order):**
1. `discovered` - Post found in Reddit
2. `analyzed` - Problem analyzed
3. `responded` - Response sent
4. `dm_active` - Direct message conversation
5. `qualified` - Real prospect
6. `proposal_sent` - Pricing sent
7. `won` - Became client
8. `lost` - Didn't convert

**Other Stages:**
- `unresponsive` - No reply
- `not_qualified` - Not a fit
- `resolved` - Problem solved (no revenue)

**Key Fields:**
- `post_id` - Foreign key to reddit_posts
- `stage` - Current stage
- `stage_date` - When entered this stage
- `notes` - Stage transition notes
- `agent_updated` - Which agent updated

**Common Query:**
```sql
-- Active prospects by stage
SELECT ps.stage, COUNT(*) as count
FROM pipeline_stages ps
WHERE ps.stage NOT IN ('won', 'lost')
GROUP BY ps.stage
ORDER BY count DESC;
```

### 4. content_opportunities (Content Ideas)
Links problems to content creation. Links to `reddit_posts.id`

**Key Fields:**
- `post_id` - Source problem
- `content_type` - case_study, blog_post, video, linkedin
- `content_status` - planned, created, published
- `priority_level` - 1-10
- `target_audience` - Who this is for
- `angle` - Content angle/hook

**Workflow:**
```sql
-- Find high-priority unpublished content opportunities
SELECT co.*, rp.title, rp.problem_category
FROM content_opportunities co
JOIN reddit_posts rp ON co.post_id = rp.id
WHERE co.content_status IN ('planned', 'created')
  AND co.priority_level >= 7
ORDER BY co.priority_level DESC;
```

### 5. audience_members (People We Track)
Tracks individuals across multiple interactions.

**Key Fields:**
- `username` - Reddit username (unique)
- `primary_service_interest` - GTM, Shopify, WordPress
- `engagement_score` - 0-100
- `conversion_status` - prospect, client, lost
- `lifetime_value` - Total revenue
- `interaction_count` - Number of interactions

### 6. client_projects (Actual Work)
Tracks paid projects. Links to `audience_members.id` and `reddit_posts.id`

**Key Fields:**
- `audience_id` - Who is the client
- `source_post_id` - Which Reddit post led to this
- `service_type` - GTM, Shopify, WordPress
- `project_value` - Revenue
- `status` - planning, active, completed, cancelled

### 7. call_notes (Diagnostic Calls)
Documents sales/diagnostic calls.

**Key Fields:**
- `post_id` - Source problem
- `call_type` - discovery, diagnostic, closing, follow-up
- `issue_layer` - Layer 1-4 (diagnostic framework)
- `root_cause` - What was actually broken
- `technical_diagnosis` - Full diagnosis
- `key_learning` - For case studies
- `confidence_level` - 1-10 self-assessment

## Common Workflows

### Workflow 1: Log New Prospect from Reddit

```sql
-- 1. Insert prospect
INSERT INTO reddit_posts (
  post_url, username, subreddit, title, content,
  problem_category, urgency_level, service_type, agent_discovered
) VALUES (
  'https://reddit.com/r/GoogleTagManager/abc123',
  'username_here',
  'GoogleTagManager',
  'GA4 events not firing',
  'Full post content...',
  'GTM',
  'high',
  'prospect',
  'daily-prospecting-v1'
) RETURNING id;

-- 2. Insert pipeline stage
INSERT INTO pipeline_stages (post_id, stage, notes, agent_updated)
VALUES (
  <id_from_above>,
  'discovered',
  'Found via daily prospecting scan',
  'daily-prospecting-v1'
);
```

### Workflow 2: Create Solution

```sql
-- After analyzing problem, create solution
INSERT INTO solutions (
  post_id, solution_text, estimated_value,
  complexity_level, service_type, implementation_hours
) VALUES (
  123,
  'Install GTM4WP plugin, configure GA4 container...',
  500.00,
  'moderate',
  'GTM',
  3
);

-- Update pipeline stage
INSERT INTO pipeline_stages (post_id, stage, notes, agent_updated)
VALUES (123, 'analyzed', 'Solution created, ready to respond', 'gtm-prospecting-agent');
```

### Workflow 3: Find Content Opportunities

```sql
-- Find high-value problems with solutions but no content
SELECT
  rp.id,
  rp.title,
  rp.problem_category,
  s.solution_text,
  s.estimated_value,
  s.complexity_level
FROM reddit_posts rp
JOIN solutions s ON rp.id = s.post_id
LEFT JOIN content_opportunities co ON rp.id = co.post_id
WHERE co.id IS NULL  -- No content created yet
  AND s.complexity_level IN ('moderate', 'complex')
  AND s.estimated_value >= 300
ORDER BY s.estimated_value DESC
LIMIT 10;
```

### Workflow 4: Extract Data for Blog Post

```sql
-- Get full context for case study creation
SELECT
  rp.title AS problem_title,
  rp.content AS problem_description,
  rp.subreddit,
  rp.problem_category,
  s.solution_text,
  s.complexity_level,
  s.implementation_hours,
  cn.technical_diagnosis,
  cn.key_learning,
  cn.root_cause
FROM reddit_posts rp
JOIN solutions s ON rp.id = s.post_id
LEFT JOIN call_notes cn ON rp.id = cn.post_id
WHERE rp.id = 123;
```

### Workflow 5: Track Pipeline Health

```sql
-- Use built-in view
SELECT * FROM active_prospects
WHERE stage IN ('dm_active', 'qualified', 'proposal_sent')
ORDER BY stage_date DESC;

-- Pipeline conversion metrics
SELECT * FROM conversion_pipeline
WHERE problem_category = 'GTM';
```

## Content Creation Process

### From CRM → Case Study → Multi-Format Content

**Step 1: Identify High-Value Case Study**
```sql
SELECT
  rp.id,
  rp.title,
  rp.problem_category,
  s.estimated_value,
  cn.confidence_level,
  cn.key_learning
FROM reddit_posts rp
JOIN solutions s ON rp.id = s.post_id
LEFT JOIN call_notes cn ON rp.id = cn.post_id
WHERE s.complexity_level IN ('moderate', 'complex')
  AND (cn.confidence_level >= 7 OR cn.confidence_level IS NULL)
ORDER BY s.estimated_value DESC
LIMIT 5;
```

**Step 2: Mark as Content Opportunity**
```sql
INSERT INTO content_opportunities (
  post_id, content_type, angle, priority_level,
  target_audience, content_status
) VALUES (
  123,
  'case_study',
  'How we diagnosed and fixed [problem] in [timeframe]',
  8,
  'Business owners with [problem_category] issues',
  'planned'
);
```

**Step 3: Create Content Variations**
From one case study, create:
1. **Blog post** - Full technical write-up
2. **LinkedIn series** - 5-part breakdown
3. **Video script** - Demonstration walkthrough
4. **Social proof** - Before/after results

**Step 4: Test in Local Environment**
- **Tool:** Local by Flywheel (WordPress)
- **Platform:** WooCommerce (for e-commerce demos)
- **Purpose:** Demonstrate solution in controlled environment
- **Output:** Screenshots, videos, step-by-step documentation

**Step 5: Publish and Track**
```sql
UPDATE content_opportunities
SET content_status = 'published'
WHERE post_id = 123;
```

## Key Metrics to Monitor

### Pipeline Health
```sql
-- Prospects with no pipeline stage (CRITICAL ISSUE)
SELECT COUNT(*) FROM reddit_posts rp
LEFT JOIN pipeline_stages ps ON rp.id = ps.post_id
WHERE ps.id IS NULL;
```

### Revenue Potential
```sql
-- Total pipeline value by service type
SELECT
  service_type,
  COUNT(*) as opportunities,
  SUM(estimated_value) as total_value,
  AVG(estimated_value) as avg_value
FROM solutions
GROUP BY service_type;
```

### Content Production
```sql
-- Content opportunities by status
SELECT content_status, content_type, COUNT(*)
FROM content_opportunities
GROUP BY content_status, content_type;
```

### Conversion Rate
```sql
-- Prospects → Clients
SELECT
  COUNT(DISTINCT rp.id) as total_prospects,
  COUNT(DISTINCT cp.id) as clients,
  ROUND(COUNT(DISTINCT cp.id)::numeric / COUNT(DISTINCT rp.id) * 100, 2) as conversion_rate
FROM reddit_posts rp
LEFT JOIN client_projects cp ON rp.id = cp.source_post_id;
```

## Critical Issues to Avoid

**Issue 1: Missing Pipeline Stages**
- ALWAYS insert pipeline_stages when creating reddit_posts
- Current issue: 75% of prospects have no stage tracked

**Issue 2: No Audience Interaction Logging**
- After sending response, log to audience_interactions
- Update audience_members.last_interaction_date

**Issue 3: Content Flywheel Dormant**
- Weekly: Extract 1 case study from high-confidence calls
- Track in content_opportunities table

**Issue 4: No Client Conversion Tracking**
- When prospect converts, create client_projects entry
- Link back to source_post_id

## Test Environment Details

**Platform:** Local by Flywheel
**Purpose:** WordPress site testing and demonstration
**E-commerce:** WooCommerce installed
**Use Case:** Create reproducible problem scenarios and demonstrate solutions

**Workflow:**
1. Replicate problem from CRM in test environment
2. Document steps to reproduce
3. Implement solution
4. Capture screenshots/video
5. Use for case study content

## Views Available

**active_prospects**
- All prospects not in 'won' or 'lost' stage
- Includes engagement score from audience_members

**conversion_pipeline**
- Pipeline metrics by problem_category and stage
- Average value per stage

## Reference Documents

- Full schema: `migrations/crm_schema_postgres.sql`
- Performance analysis: `reports/CRM-DATABASE-ANALYSIS-2025-10-03.md`
