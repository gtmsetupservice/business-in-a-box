# Daily Multi-Domain Business Crib Sheet

## Morning JavaScript Drill (2 snippets)
```
load pm agent
```
→ PM Agent tracks which snippets you've completed in call_notes table

```
javascript-drill
```
→ Shows you 2 GTM/Google Ads snippets, you explain line-by-line, get corrected

## Unified Multi-Domain Prospecting Workflow

### Step 1: Load Unified Prospecting Agent
```
load unified prospecting agent
```
→ Activates multi-audience scanning system (Website, GTM, WordPress, Shopify)

### Step 2: Execute Fresh Lead Scan (6-Hour Window)
```
fresh-scan
```
→ Scans all 4 audiences simultaneously with freshness scoring
→ Finds prospects posted in last 6 hours (optimal conversion window)
→ Applies competition analysis and urgency detection

### Step 3: Review Scored Prospects
```
prospect-review
```
→ Shows ranked list of prospects (80+ score = priority)
→ Displays drafted value-first responses for each prospect
→ Includes cross-sell opportunities and DM transition analysis

### Step 4: Cross-Sell Analysis
```
cross-sell-analysis
```
→ Identifies natural upsell opportunities across service areas
→ Website → GTM tracking, WordPress → Performance optimization
→ GTM → Website audit, Shopify → Conversion tracking

### Step 5: Deploy Selected Responses
→ Human review and deployment of agent-drafted responses
→ Maintain Reddit community compliance with value-first approach
→ Deploy responses for prospects scoring 70+ points

### Step 6: Update CRM Pipeline
```
pipeline-update
```
→ Logs selected prospects with complete scoring data
→ Tags by audience type and cross-sell opportunities
→ Tracks response deployment and engagement

### Step 7: Expand Window If Needed
```
expand-window
```
→ If <5 prospects found, extends to 24-hour window
→ Maintains quality over quantity approach
→ Focuses on under-served posts only

### Step 8: Switch to PM Agent for Management
```
load pm agent
```
→ Takes over for ongoing pipeline management and client progression

### Step 9: Track DM Conversations
```
track-lead
```
→ Logs any DM responses or follow-up conversations
→ Updates prospect stages based on engagement level

### Step 10: Schedule Discovery Calls
```
start [prospect-name] diagnostic
```
→ Prepares call documentation and solution walkthrough

## Market Intelligence Commands

**Daily Revenue Analysis:**
```
revenue-by-domain
```
→ Shows which domain (GTM/WordPress/Shopify) generated most prospects/revenue

**Opportunity Mapping:**
```
problem-solution-analysis
```
→ Identifies which problem types convert best across domains

**Domain Performance:**
```
domain-metrics
```
→ Compares prospect quality, conversion rates, and revenue by domain

## Authority Flywheel Content Production

### Load Content Agent (After Client Work)
```
load content agent
```
→ Activates Authority Flywheel Content Agent for case study transformation

### Extract Case Study from CRM
```
extract-case-study
```
→ Pull recent diagnostic case from CRM database
→ Look for Layer 3+ complexity cases with clear diagnostic progression
→ Anonymize client data while preserving technical accuracy

### Create Blog Post
```
write-blog-post
```
→ Transform case study into 2000-3000 word comprehensive article
→ Include diagnostic methodology demonstration
→ Add SEO optimization and service CTAs

### Create YouTube Script
```
write-youtube-script
```
→ Convert blog post to 12-15 minute video script
→ Include screen recording cues and visual demonstrations
→ Focus on problem-solving walkthrough

### Create LinkedIn Series
```
create-linkedin-series
```
→ Break blog post into 5-part professional series
→ Each part 200-300 words for LinkedIn engagement
→ Include B2B credibility signals and agency focus

### Track Flywheel Momentum
```
track-flywheel-momentum
```
→ Monitor content production efficiency
→ Track authority building metrics
→ Identify compound growth indicators

## End of Day: Log Progress
```
wrap
```
→ Updates all prospect statuses and logs daily activity

## Quick Reference Commands

**Check CRM Status:**
```
sqlite3 crm/gtm_crm.db "SELECT username, stage FROM active_prospects WHERE stage != 'lost';"
```
→ Shows all active prospects in pipeline

**Check Today's Priorities:**
```
today
```
→ PM Agent shows what's due based on day of week

**Log Call Notes (After Any Call):**
```
log-call-notes
```
→ Captures diagnostic findings and confidence level

---

## Daily Tracking System

JavaScript Snippets Progress:
- Stored in: call_notes table under 'training' type
- PM Agent remembers which snippets completed
- Rotates through Google Ads payload inspection patterns

Unified Prospecting Pipeline Stages:
discovered → analyzed → responded → dm_active → qualified → proposal_sent → won/lost

Freshness Scoring Thresholds:
- 90+ points: Emergency response (same day)
- 80+ points: Priority prospects (draft responses)
- 70+ points: Qualified prospects (consider for response)
- 60-69 points: Borderline (expand window if needed)
- <60 points: Skip (stale or over-competed)

## Agent Responsibilities

**Unified Prospecting Agent:** Multi-audience scanning (Website, GTM, WordPress, Shopify) with freshness scoring and cross-sell identification
**PM Agent:** Pipeline management, client progression, market intelligence, learning capture
**Authority Flywheel Content Agent:** Transform case studies into blog posts, YouTube scripts, LinkedIn series for authority building
**Jekyll Web Development Agent:** Website prospects choosing static site solutions
**Support Agents (GTM/WordPress/Shopify):** Technical work after client conversion only

## Daily Success Metrics

**Unified Prospecting Goals:**
- 8+ fresh prospects (6-hour window) across all 4 audiences
- 3+ prospects scoring 80+ points (priority responses)
- 2+ cross-sell opportunities identified
- 1+ DM conversation initiated from value-first responses

**Market Intelligence Goals:**
- Daily revenue analysis by domain
- Weekly trend identification
- Monthly domain performance comparison
- Quarterly strategy adjustments based on data

**Authority Flywheel Goals:**
- 1 case study extracted and transformed weekly
- 1 comprehensive blog post (2000-3000 words) published
- 1 YouTube script created for video production
- 1 LinkedIn 5-part series for professional amplification
- Track flywheel momentum acceleration month-over-month