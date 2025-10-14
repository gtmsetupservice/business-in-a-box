---
prospect_id: reddit____throwaway____9_1ne69rg
username: u/___throwaway____9
subreddit: r/GoogleTagManager
post_url: https://reddit.com/r/GoogleTagManager/comments/1ne69rg/tracking_multiple_buttons_on_a_website/
post_date: 2025-09-11
discovery_date: 2025-09-15
layer: 2
layer_name: Implementation
scope: client-gtm
confidence: high
root_cause: Missing button identification in event parameters
service_type: basic_setup
estimated_price: 497
estimated_hours: 4
current_capability: full_service
current_stage: response-sent
competitive_analysis:
  existing_responses: 2
  quality_assessment: "AdhesivenessLow7173 provided detailed solution with custom JavaScript variable approach and parameter passing. Living-Big-1567 gave brief mention of Click ID/Text variables. Both gave away solutions rather than diagnostic approach."
  opportunity: "Provide validation method first before suggesting implementation approach"
progression:
  - stage: discovered
    date: 2025-09-15
    action: created_record
    notes: "Multi-button tracking setup needed"
  - stage: response-sent
    date: 2025-09-15
    action: posted_reddit_reply
    notes: "Posted diagnostic validation approach for configuration issue"
outcome:
  status: active
  close_date: null
  revenue: 0
  notes: null
---

# Multi-Button Tracking Issue - throwaway9

## Problem Description
Im trying to track a series of buttons on my website and I setup a tag that fires but it isn't showing me which buttons are being used in GA4. My current trigger looks something like this: {Click Element} - matches CSS selector - then I have several CSS IDs that match the ones I assigned my website buttons. I have 20+ buttons and would like one GTM tag and trigger if possible.

## Reddit Reply

I can see how frustrating this must be - setting up tracking for 20+ buttons and not being able to tell which ones are actually driving engagement is a real problem for optimization.

Looking at your issue, this appears to be a **configuration issue** - your GTM setup needs a way to capture which specific button was clicked.

To validate what's happening, you can check in GTM Preview mode:
1. Click one of your buttons
2. Look at the Variables tab
3. Check if Click Text or Click ID shows the button identity

You can also run this diagnostic to see what identifying information is available:

```javascript
(() => {
  document.addEventListener('click', (e) => {
    if (e.target.matches('button, [role="button"], a')) {
      console.log('Button clicked:', {
        text: e.target.innerText,
        id: e.target.id,
        classes: e.target.className
      });
    }
  });
  return 'Monitoring button clicks - click any button';
})();
```

This will show you what identifying information GTM has access to for each button, which helps determine the best approach for your tracking setup.

## DM Script
Hi! Thanks for the diagnostic info. For 20+ buttons, you definitely want a single tag solution using a Custom JavaScript variable to capture the button identity. I run GTMSetupService.com and we set up these multi-button tracking systems regularly. Would you like me to guide you through the configuration, or would you prefer we set it up for you?

## Full Solution
1. Create Custom JS variable for button identity
2. Single GA4 event tag with dynamic parameters
3. One trigger for all buttons
4. Pass button identity as event parameter
5. Configure custom dimension in GA4

## Objection Handling
Without proper button tracking, you can't optimize user flow or identify conversion paths.