---
prospect_id: reddit_glidingadmiral_1nospjh
username: u/glidingadmiral
subreddit: r/GoogleTagManager
post_url: https://reddit.com/r/GoogleTagManager/comments/1nospjh/need_help_tracking_an_event_flow_across_pages/
post_date: 2025-09-24
discovery_date: 2025-09-26
response_date: 2025-09-26
layer: 2
layer_name: Configuration
scope: client-gtm
confidence: high
root_cause: Group triggers breaking on page load, need cross-page event persistence
service_type: advanced_setup
estimated_price: 497
estimated_hours: 6
current_capability: full_service
current_stage: response-sent
competitive_analysis:
  existing_responses: 2
  quality_assessment: "svkmndl97 provided generic sessionStorage suggestion and asked for details. victorallen_1 suggested URL parameters as primary with sessionStorage as backup. Both responses were basic suggestions without diagnostic validation."
  opportunity: "Provide systematic diagnostic approach before implementation recommendations"
progression:
  - stage: discovered
    date: 2025-09-26
    action: found_in_prospect_scan
    notes: "Multi-step cross-page event tracking issue"
  - stage: response-sent
    date: 2025-09-26
    action: posted_reddit_reply
    notes: "Posted diagnostic validation approach for data persistence checking"
outcome:
  status: active
  close_date: null
  revenue: 0
  notes: "AI competition concern - need faster response times going forward"
---

# Multi-Step Cross-Page Event Tracking - glidingadmiral

## Problem Description
I have a use case where I have to track a multi step process as an event; issue is that since it includes a page load, group triggers are not effective. Read about using sessionstorage for this use case, if anyone has experience with this or have something I could refer to, would be a great help! Thanks!

## Reddit Reply Posted
Cross-page event tracking is tricky. You can validate what's actually happening in your current setup.

You can check what's available for tracking by this in your browser console on each step:

```javascript
// Check what data persists across page loads
(() => {
  const checks = {
    dataLayer: dataLayer?.length || 0,
    sessionStorage: Object.keys(sessionStorage).length,
    urlParams: new URLSearchParams(window.location.search).toString(),
    currentStep: window.location.pathname
  };
  console.log('Step tracking data:', checks);
  return checks;
})();
```

This will show you what information is available at each step, which determines whether sessionStorage, URL parameters, or a hybrid approach works best for your flow.

## DM Script
Hi! Thanks for running that diagnostic. Cross-page tracking definitely requires careful setup. I run GTMSetupService.com and we implement these multi-step tracking systems regularly. Would you like me to guide you through the sessionStorage approach, or would you prefer we handle the implementation for you?

## Full Solution
1. Design step-by-step data persistence strategy
2. Implement sessionStorage with GTM custom variables
3. Create cross-page trigger logic
4. Set up funnel tracking in GA4
5. Test complete user journey flow

## Objection Handling
Without proper cross-page tracking, you lose visibility into your conversion funnel and can't optimize drop-off points.

## AI Competition Notes
- Posted Sept 26 - 2 days after original post
- Reddit AI Answers threat identified
- Future responses need 15-30 minute speed to beat AI
- Focus on "I can implement this now" rather than diagnostic education