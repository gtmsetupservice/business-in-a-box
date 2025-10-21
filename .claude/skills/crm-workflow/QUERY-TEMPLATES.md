# CRM SQL Query Templates

Quick reference for common CRM database queries.

## Connection Helper

```bash
# Set environment variables from .env
export $(grep -v '^#' .env | xargs)

# Connect to CRM
psql postgresql://$CRM_POSTGRES_USER:$CRM_POSTGRES_PASSWORD@$CRM_POSTGRES_HOST:$CRM_POSTGRES_PORT/$CRM_POSTGRES_DB
```

## Prospecting Queries

### Find Recent High-Priority Prospects
```sql
SELECT
  id,
  title,
  subreddit,
  problem_category,
  urgency_level,
  discovered_date
FROM reddit_posts
WHERE urgency_level IN ('high', 'emergency', 'critical')
  AND discovered_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY discovered_date DESC;
```

### Prospects with No Pipeline Stage (CRITICAL)
```sql
SELECT
  rp.id,
  rp.title,
  rp.username,
  rp.problem_category,
  rp.discovered_date
FROM reddit_posts rp
LEFT JOIN pipeline_stages ps ON rp.id = ps.post_id
WHERE ps.id IS NULL
ORDER BY rp.discovered_date DESC;
```

### Active DM Conversations
```sql
SELECT
  rp.id,
  rp.title,
  rp.username,
  ps.stage_date,
  ps.notes
FROM reddit_posts rp
JOIN pipeline_stages ps ON rp.id = ps.post_id
WHERE ps.stage = 'dm_active'
ORDER BY ps.stage_date DESC;
```

## Solution Queries

### High-Value Solutions Without Content
```sql
SELECT
  rp.id,
  rp.title,
  s.estimated_value,
  s.complexity_level,
  s.service_type
FROM reddit_posts rp
JOIN solutions s ON rp.id = s.post_id
LEFT JOIN content_opportunities co ON rp.id = co.post_id
WHERE co.id IS NULL
  AND s.estimated_value >= 300
ORDER BY s.estimated_value DESC;
```

### Solution Revenue by Service Type
```sql
SELECT
  service_type,
  COUNT(*) as count,
  SUM(estimated_value) as total_value,
  AVG(estimated_value) as avg_value,
  MIN(estimated_value) as min_value,
  MAX(estimated_value) as max_value
FROM solutions
GROUP BY service_type
ORDER BY total_value DESC;
```

### Complex Problems Needing Attention
```sql
SELECT
  rp.id,
  rp.title,
  s.complexity_level,
  s.estimated_value,
  ps.stage
FROM reddit_posts rp
JOIN solutions s ON rp.id = s.post_id
LEFT JOIN pipeline_stages ps ON rp.id = ps.post_id
WHERE s.complexity_level = 'complex'
  AND (ps.stage IS NULL OR ps.stage IN ('discovered', 'analyzed'))
ORDER BY s.estimated_value DESC;
```

## Content Production Queries

### Planned Content Not Yet Created
```sql
SELECT
  co.id,
  rp.title,
  co.content_type,
  co.priority_level,
  co.angle,
  rp.problem_category
FROM content_opportunities co
JOIN reddit_posts rp ON co.post_id = rp.id
WHERE co.content_status = 'planned'
ORDER BY co.priority_level DESC;
```

### Best Case Studies for This Week
```sql
SELECT
  rp.id,
  rp.title,
  rp.problem_category,
  s.estimated_value,
  s.complexity_level,
  cn.confidence_level,
  cn.key_learning
FROM reddit_posts rp
JOIN solutions s ON rp.id = s.post_id
LEFT JOIN call_notes cn ON rp.id = cn.post_id
LEFT JOIN content_opportunities co ON rp.id = co.post_id
WHERE s.complexity_level IN ('moderate', 'complex')
  AND co.id IS NULL  -- Not yet turned into content
  AND (cn.confidence_level >= 6 OR cn.confidence_level IS NULL)
ORDER BY s.estimated_value DESC
LIMIT 5;
```

### Content Production Status
```sql
SELECT
  content_type,
  content_status,
  COUNT(*) as count
FROM content_opportunities
GROUP BY content_type, content_status
ORDER BY content_type, content_status;
```

## Pipeline Health Queries

### Pipeline Stage Distribution
```sql
SELECT
  COALESCE(ps.stage, 'no_stage') as stage,
  COUNT(*) as count
FROM reddit_posts rp
LEFT JOIN pipeline_stages ps ON rp.id = ps.post_id
GROUP BY ps.stage
ORDER BY count DESC;
```

### Prospects Stuck in Stage
```sql
SELECT
  ps.stage,
  rp.title,
  rp.username,
  ps.stage_date,
  CURRENT_DATE - ps.stage_date as days_in_stage
FROM reddit_posts rp
JOIN pipeline_stages ps ON rp.id = ps.post_id
WHERE ps.stage IN ('analyzed', 'responded')
  AND ps.stage_date < CURRENT_DATE - INTERVAL '7 days'
ORDER BY days_in_stage DESC;
```

### Conversion Funnel
```sql
SELECT
  ps.stage,
  COUNT(DISTINCT rp.id) as prospects,
  SUM(s.estimated_value) as pipeline_value
FROM reddit_posts rp
JOIN pipeline_stages ps ON rp.id = ps.post_id
LEFT JOIN solutions s ON rp.id = s.post_id
GROUP BY ps.stage
ORDER BY
  CASE ps.stage
    WHEN 'discovered' THEN 1
    WHEN 'analyzed' THEN 2
    WHEN 'responded' THEN 3
    WHEN 'dm_active' THEN 4
    WHEN 'qualified' THEN 5
    WHEN 'proposal_sent' THEN 6
    WHEN 'won' THEN 7
    WHEN 'lost' THEN 8
    ELSE 9
  END;
```

## Audience Tracking Queries

### Top Engaged Audience Members
```sql
SELECT
  username,
  primary_service_interest,
  engagement_score,
  interaction_count,
  conversion_status,
  lifetime_value
FROM audience_members
ORDER BY engagement_score DESC
LIMIT 20;
```

### Audience Members Without Recent Interaction
```sql
SELECT
  username,
  primary_service_interest,
  last_interaction_date,
  CURRENT_DATE - last_interaction_date as days_since_interaction,
  interaction_count
FROM audience_members
WHERE last_interaction_date < CURRENT_DATE - INTERVAL '14 days'
  AND conversion_status = 'prospect'
ORDER BY days_since_interaction DESC;
```

## Business Metrics Queries

### Monthly Prospect Discovery
```sql
SELECT
  DATE_TRUNC('month', discovered_date) as month,
  COUNT(*) as prospects_discovered,
  COUNT(DISTINCT agent_discovered) as active_agents
FROM reddit_posts
WHERE discovered_date >= CURRENT_DATE - INTERVAL '6 months'
GROUP BY DATE_TRUNC('month', discovered_date)
ORDER BY month DESC;
```

### Agent Performance
```sql
SELECT
  agent_discovered,
  COUNT(*) as prospects_found,
  AVG(CASE
    WHEN urgency_level IN ('high', 'emergency', 'critical') THEN 1
    ELSE 0
  END) * 100 as pct_high_priority
FROM reddit_posts
WHERE discovered_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY agent_discovered
ORDER BY prospects_found DESC;
```

### Revenue Metrics
```sql
SELECT
  COUNT(DISTINCT rp.id) as total_prospects,
  COUNT(DISTINCT s.id) as solutions_created,
  SUM(s.estimated_value) as pipeline_value,
  COUNT(DISTINCT cp.id) as clients,
  SUM(cp.project_value) as actual_revenue,
  ROUND(
    COUNT(DISTINCT cp.id)::numeric / COUNT(DISTINCT rp.id) * 100,
    2
  ) as conversion_rate
FROM reddit_posts rp
LEFT JOIN solutions s ON rp.id = s.post_id
LEFT JOIN client_projects cp ON rp.id = cp.source_post_id;
```

## Diagnostic & Learning Queries

### Call Notes Summary
```sql
SELECT
  call_type,
  COUNT(*) as calls,
  AVG(confidence_level) as avg_confidence,
  AVG(call_duration) as avg_duration_minutes,
  COUNT(CASE WHEN proposal_sent THEN 1 END) as proposals_sent
FROM call_notes
GROUP BY call_type
ORDER BY calls DESC;
```

### Common Problem Categories
```sql
SELECT
  problem_category,
  COUNT(*) as occurrences,
  AVG(s.estimated_value) as avg_solution_value,
  COUNT(CASE WHEN ps.stage = 'won' THEN 1 END) as conversions
FROM reddit_posts rp
LEFT JOIN solutions s ON rp.id = s.post_id
LEFT JOIN pipeline_stages ps ON rp.id = ps.post_id
GROUP BY problem_category
ORDER BY occurrences DESC;
```

### Subreddit Performance
```sql
SELECT
  subreddit,
  COUNT(*) as posts_found,
  COUNT(DISTINCT CASE WHEN ps.stage IN ('dm_active', 'qualified', 'proposal_sent', 'won') THEN rp.id END) as engaged_prospects,
  AVG(s.estimated_value) as avg_value
FROM reddit_posts rp
LEFT JOIN pipeline_stages ps ON rp.id = ps.post_id
LEFT JOIN solutions s ON rp.id = s.post_id
GROUP BY subreddit
HAVING COUNT(*) >= 3
ORDER BY engaged_prospects DESC, posts_found DESC;
```

## Insert Templates

### Log New Prospect
```sql
WITH new_post AS (
  INSERT INTO reddit_posts (
    post_url, username, subreddit, title, content,
    problem_category, urgency_level, service_type, agent_discovered
  ) VALUES (
    'https://reddit.com/r/subreddit/postid',
    'reddit_username',
    'subreddit_name',
    'Post title',
    'Post content...',
    'GTM',  -- or 'Shopify', 'WordPress'
    'high', -- or 'medium', 'low', 'emergency'
    'prospect',
    'agent-name'
  ) RETURNING id
)
INSERT INTO pipeline_stages (post_id, stage, notes, agent_updated)
SELECT id, 'discovered', 'Found via prospecting', 'agent-name'
FROM new_post;
```

### Create Solution
```sql
WITH new_solution AS (
  INSERT INTO solutions (
    post_id, solution_text, estimated_value,
    complexity_level, service_type, implementation_hours
  ) VALUES (
    123,  -- post_id
    'Detailed solution...',
    500.00,
    'moderate',  -- or 'simple', 'complex'
    'GTM',
    3
  ) RETURNING post_id
)
INSERT INTO pipeline_stages (post_id, stage, notes, agent_updated)
SELECT post_id, 'analyzed', 'Solution created', 'agent-name'
FROM new_solution;
```

### Log Response Sent
```sql
WITH new_response AS (
  INSERT INTO our_responses (
    post_id, response_text, engagement_level,
    conversion_potential, agent_type
  ) VALUES (
    123,
    'Response text...',
    'diagnostic',  -- or 'helpful', 'referral'
    'medium',      -- or 'low', 'high'
    'prospecting'
  ) RETURNING post_id
)
INSERT INTO pipeline_stages (post_id, stage, notes, agent_updated)
SELECT post_id, 'responded', 'Response posted', 'agent-name'
FROM new_response;
```

### Create Content Opportunity
```sql
INSERT INTO content_opportunities (
  post_id, content_type, angle, priority_level,
  target_audience, content_status
) VALUES (
  123,
  'case_study',  -- or 'blog_post', 'video', 'linkedin'
  'How we solved [problem] in [timeframe]',
  8,  -- 1-10
  'Business owners with GTM tracking issues',
  'planned'  -- or 'created', 'published'
);
```

### Log Call Notes
```sql
INSERT INTO call_notes (
  post_id, username, call_date, call_type, call_duration,
  technical_diagnosis, confidence_level, key_learning,
  estimated_value, service_recommended
) VALUES (
  123,
  'reddit_username',
  NOW(),
  'diagnostic',  -- or 'discovery', 'closing', 'follow-up'
  45,  -- minutes
  'Full technical diagnosis...',
  7,   -- 1-10
  'Key learning for case study...',
  500.00,
  'Emergency GTM Recovery'
);
```

### Update to Client
```sql
WITH new_client AS (
  INSERT INTO client_projects (
    audience_id, source_post_id, project_name,
    service_type, project_value, status
  ) VALUES (
    45,   -- audience_id
    123,  -- post_id that led to this
    'GTM Conversion Tracking Setup',
    'GTM',
    500.00,
    'active'
  ) RETURNING source_post_id
)
INSERT INTO pipeline_stages (post_id, stage, notes, agent_updated)
SELECT source_post_id, 'won', 'Converted to client', 'pm-agent'
FROM new_client;
```

## Maintenance Queries

### Fix Missing Pipeline Stages
```sql
-- Find posts without stages
INSERT INTO pipeline_stages (post_id, stage, notes, agent_updated)
SELECT
  rp.id,
  'discovered',
  'Backfilled missing stage',
  'system'
FROM reddit_posts rp
LEFT JOIN pipeline_stages ps ON rp.id = ps.post_id
WHERE ps.id IS NULL;
```

### Update Audience Engagement Scores
```sql
UPDATE audience_members
SET engagement_score = (
  SELECT COUNT(*) * 10  -- Simple scoring: 10 points per interaction
  FROM audience_interactions ai
  WHERE ai.audience_id = audience_members.id
);
```
