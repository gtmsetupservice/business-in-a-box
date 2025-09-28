# GTM Business Intelligence Tracking - Custom JavaScript Procedure

## Overview
This procedure transforms basic GTM click tracking into business intelligence by adding Custom JavaScript variables that classify user interactions by business value and revenue intent.

## The Business Intelligence Framework

**Instead of just tracking:** "User clicked button"
**We track:** "User showed high-intent conversion behavior on primary CTA"

This enables revenue-focused analytics and optimization decisions.

## Step 1: Set Up DataLayer Monitoring (MANDATORY)

**Always start with evidence gathering:**

```javascript
// Monitor all dataLayer events
window.dataLayer = window.dataLayer || [];
var originalPush = window.dataLayer.push;
window.dataLayer.push = function() {
  console.log('DataLayer Push:', arguments[0]);
  return originalPush.apply(window.dataLayer, arguments);
};
console.log('DataLayer monitoring active. Click all target buttons...');
```

**Test all buttons and record:**
- Button text variations
- Class patterns  
- Business value differences

## Step 2: Create Business Intelligence Variables

### Variable 1: Button Intent Level

**Variable Name:** `Button Intent Level`
**Variable Type:** Custom JavaScript
**Purpose:** Classify clicks by revenue potential

```javascript
function() {
  var text = {{Click Text}}.toLowerCase();
  
  // HIGH INTENT: Direct conversion actions
  if (text.includes('book') || text.includes('call') || text.includes('schedule') || 
      text.includes('buy') || text.includes('purchase') || text.includes('order')) {
    return 'high-intent';
  }
  
  // MEDIUM INTENT: Lead generation actions
  if (text.includes('submit') || text.includes('send') || text.includes('contact') || 
      text.includes('quote') || text.includes('demo') || text.includes('trial')) {
    return 'medium-intent';
  }
  
  // LOW INTENT: Information seeking
  if (text.includes('learn') || text.includes('more') || text.includes('read') || 
      text.includes('about') || text.includes('info') || text.includes('details')) {
    return 'low-intent';
  }
  
  return 'unknown';
}
```

### Variable 2: Button Category

**Variable Name:** `Button Category`
**Variable Type:** Custom JavaScript  
**Purpose:** Classify buttons by business function

```javascript
function() {
  var text = {{Click Text}}.toLowerCase();
  var classes = {{Click Classes}};
  
  // CONVERSION CTAs: Primary revenue drivers
  if (text.includes('book') || text.includes('call') || text.includes('schedule') ||
      text.includes('buy') || text.includes('purchase') || text.includes('order')) {
    return 'conversion-cta';
  }
  
  // FORM SUBMISSIONS: Lead generation
  if (text.includes('submit') && classes.includes('form-submit')) {
    return 'form-submission';
  }
  
  // STANDALONE CTAs: Single-purpose buttons
  if (classes.includes('wp-block-kadence-singlebtn') || classes.includes('standalone')) {
    return 'standalone-cta';
  }
  
  // NAVIGATION: Site navigation buttons
  if (classes.includes('nav') || classes.includes('menu') || 
      text.includes('home') || text.includes('back')) {
    return 'navigation';
  }
  
  // SOCIAL: Social media buttons
  if (text.includes('share') || text.includes('follow') || 
      classes.includes('social')) {
    return 'social';
  }
  
  return 'general-button';
}
```

### Variable 3: Revenue Value Score (Advanced)

**Variable Name:** `Revenue Value Score`
**Variable Type:** Custom JavaScript
**Purpose:** Assign numeric scores for revenue potential

```javascript
function() {
  var text = {{Click Text}}.toLowerCase();
  var classes = {{Click Classes}};
  
  // HIGH VALUE: 100 points
  if (text.includes('book') || text.includes('call') || text.includes('buy')) {
    return 100;
  }
  
  // MEDIUM-HIGH VALUE: 75 points
  if (text.includes('quote') || text.includes('demo') || text.includes('trial')) {
    return 75;
  }
  
  // MEDIUM VALUE: 50 points
  if (text.includes('submit') || text.includes('contact') || text.includes('send')) {
    return 50;
  }
  
  // LOW VALUE: 25 points
  if (text.includes('learn') || text.includes('more') || text.includes('info')) {
    return 25;
  }
  
  // NO VALUE: 0 points
  if (classes.includes('nav') || text.includes('menu')) {
    return 0;
  }
  
  return 10; // Default for unclassified
}
```

## Step 3: Create GA4 Event Tag with Business Parameters

**Tag Name:** `Business Intelligence - Button Clicks`
**Tag Type:** Google Analytics: GA4 Event
**Event Name:** `intelligent_button_click`

**Event Parameters:**
- `button_text`: `{{Click Text}}`
- `button_classes`: `{{Click Classes}}`  
- `button_intent_level`: `{{Button Intent Level}}`
- `button_category`: `{{Button Category}}`
- `revenue_value_score`: `{{Revenue Value Score}}`
- `page_hostname`: `{{Page Hostname}}`
- `page_path`: `{{Page Path}}`

## Step 4: Create Smart Trigger

**Trigger Name:** `Smart Button Clicks`
**Trigger Type:** Click - All Elements
**This trigger fires on:** Some Clicks

**Conditions (adjust based on your dataLayer evidence):**
- Click Classes contains `kb-button` (or your site's button pattern)
- OR Click Element matches `button`
- OR Click Element matches `[role="button"]`

## Step 5: Test and Validate

### Expected Results for Different Button Types:

**"Book a Call" Button:**
- `button_intent_level`: "high-intent"
- `button_category`: "conversion-cta"  
- `revenue_value_score`: 100

**"Submit" Form Button:**
- `button_intent_level`: "medium-intent"
- `button_category`: "form-submission"
- `revenue_value_score`: 50

**"Learn More" Button:**
- `button_intent_level`: "low-intent" 
- `button_category`: "general-button"
- `revenue_value_score`: 25

## Step 6: GA4 Business Intelligence Reports

### Custom Dimensions to Create:
1. **Button Intent Level** → Event parameter: `button_intent_level`
2. **Button Category** → Event parameter: `button_category`  
3. **Revenue Value Score** → Custom metric: `revenue_value_score`

### Business Reports You Can Build:

**Revenue Optimization Report:**
- Events where `button_intent_level` = "high-intent"
- Group by `button_text` to see best-performing CTAs
- Compare conversion rates by intent level

**Button Performance Analysis:**
- Sum of `revenue_value_score` by page
- Identify highest-value pages and optimize
- Track value score trends over time

**Customer Journey Intelligence:**
- Path analysis: low-intent → medium-intent → high-intent
- Time between intent levels
- Pages that drive intent escalation

## Customization for Different Industries

### E-commerce Modifications:
```javascript
// Add to Button Intent Level variable
if (text.includes('add to cart') || text.includes('checkout')) {
  return 'high-intent';
}
if (text.includes('wishlist') || text.includes('compare')) {
  return 'medium-intent';
}
```

### B2B Service Modifications:
```javascript
// Add to Button Category variable  
if (text.includes('consultation') || text.includes('audit')) {
  return 'lead-qualifier';
}
if (text.includes('case study') || text.includes('whitepaper')) {
  return 'content-download';
}
```

### SaaS Modifications:
```javascript
// Add to Revenue Value Score variable
if (text.includes('upgrade') || text.includes('premium')) {
  return 150; // Higher value for upgrades
}
if (text.includes('free trial') || text.includes('demo')) {
  return 90;
}
```

## Business Intelligence Use Cases

### 1. Conversion Rate Optimization
**Question:** Which high-intent buttons have the lowest conversion rates?
**Data:** High-intent clicks that don't lead to goal completions
**Action:** A/B test button copy, placement, or design

### 2. Content Strategy
**Question:** Which pages generate the most high-intent behavior?
**Data:** Pages with highest revenue value scores
**Action:** Create more content similar to top-performing pages

### 3. User Journey Optimization  
**Question:** What path leads users from low-intent to high-intent?
**Data:** Sequence of intent levels in user sessions
**Action:** Optimize content flow and CTA placement

### 4. ROI Attribution
**Question:** What's the revenue value of each marketing channel?
**Data:** Revenue value scores by traffic source
**Action:** Allocate budget to highest-value channels

## Success Metrics

### Implementation Success:
- ✅ 100% of button clicks classified by intent level
- ✅ Revenue value scores align with actual conversion rates
- ✅ Business categories enable actionable insights

### Business Impact:
- 📈 Increased high-intent click conversion rates
- 📊 Data-driven button optimization decisions  
- 💰 Measurable ROI improvement from analytics insights
- 🎯 Better understanding of customer intent journey

## Maintenance and Updates

### Monthly Reviews:
- Analyze new button text variations
- Update JavaScript logic for new CTAs
- Verify intent classifications match business outcomes
- Add new button categories as site evolves

### Quarterly Optimizations:
- Review revenue value score accuracy
- Update scoring based on actual conversion data
- Expand variables for new business objectives
- Train team on new business intelligence insights

---

## Key Takeaway

**This procedure transforms GTM from technical tracking to business intelligence.** 

Instead of just knowing "users clicked buttons," you now understand:
- **Intent level** (how likely to convert)
- **Business value** (revenue potential)  
- **Optimization opportunities** (where to improve)
- **ROI attribution** (what drives revenue)

**This is the difference between amateur button tracking and professional business intelligence.**