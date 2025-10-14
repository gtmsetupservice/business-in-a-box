# Reddit Solution: 40% (not set) Traffic After WordPress to Node.js Migration

**User:** u/Embarrassed_Tour8392  
**Post URL:** https://reddit.com/r/GoogleAnalytics/comments/1nddn4d/  
**Problem:** "Still stuck with 'not set' traffic after migration"  
**Date:** September 10, 2025

## Response

I use a systematic diagnostic approach, and your "(not set)" issue after migrating from WordPress to Node.js is a Layer 4: Processing issue with elements of Layer 2.

**Layer 4** deals with how GA4 processes and interprets the data it receives. The "(not set)" value appears when GA4 receives events but can't properly attribute session source information. After platform migrations, this usually means the implementation is sending incomplete data.

## The Node.js Specific Problem

WordPress with plugins handles GA4 session management automatically. Node.js doesn't. Your dev team likely implemented basic tracking but missed critical session attribution requirements.

## Quick Diagnostic

Run this on pages showing "(not set)" traffic:

```javascript
// Check GA4 session continuity in Node.js app
(() => {
  // Check for GA4 cookies
  const cookies = document.cookie.split(';').map(c => c.trim());
  const gaCookie = cookies.find(c => c.startsWith('_ga='));
  const sessionCookie = cookies.filter(c => c.includes('_ga_'));
  
  // Check page_view timing
  const pageViewEvents = dataLayer.filter(d => d.event === 'page_view');
  const sessionStarts = dataLayer.filter(d => d.event === 'session_start');
  
  console.log('GA Client ID:', gaCookie ? 'Found' : 'MISSING');
  console.log('Session cookies:', sessionCookie.length);
  console.log('Page views fired:', pageViewEvents.length);
  console.log('Session starts:', sessionStarts.length);
  
  // Check if page_location is being sent
  const hasPageLocation = pageViewEvents.some(e => 
    e.page_location || e.event_parameters?.page_location
  );
  
  console.log('Page location parameter:', hasPageLocation ? 'Present' : 'MISSING');
  
  // Check referrer preservation
  console.log('Document referrer:', document.referrer || 'EMPTY');
  
  return 'Check console for session attribution gaps';
})();
```

## Root Causes for Node.js Apps

Your 35-40% "(not set)" likely comes from:

1. **Client-Side Rendering Issues** (Most likely)
   - Node.js SSR sends initial HTML without GA4
   - GA4 loads after React/Vue hydration
   - First page_view fires without referrer data

2. **Session Continuity Breaks**
   - GA4 script reinitializes on route changes
   - Session cookies not persisting properly
   - Missing page_location parameters

3. **Referrer Loss**
   - Node.js app strips referrer headers
   - Internal navigation overwrites external source
   - URL fragments (#) breaking attribution

## The Fix for Node.js

### 1. Ensure Proper GA4 Initialization

In your Node.js app's main template/layout:

```javascript
// Initialize GA4 BEFORE any route changes
// Place in your app's head or earliest loading point
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}

// Preserve original landing page data
if (!sessionStorage.getItem('original_referrer')) {
  sessionStorage.setItem('original_referrer', document.referrer);
  sessionStorage.setItem('original_location', window.location.href);
}

gtag('js', new Date());
gtag('config', 'G-XXXXXXXXXX', {
  'send_page_view': false,  // Control page_view manually
  'page_location': window.location.href,
  'page_referrer': sessionStorage.getItem('original_referrer') || document.referrer
});
```

### 2. Handle Route Changes Properly

For single-page apps (React/Vue/Angular):

```javascript
// On route change (React Router example)
history.listen((location) => {
  gtag('event', 'page_view', {
    page_location: window.location.href,
    page_path: location.pathname,
    page_referrer: sessionStorage.getItem('previous_page') || document.referrer
  });
  sessionStorage.setItem('previous_page', window.location.href);
});
```

### 3. Server-Side Fix (Node.js/Express)

Ensure your Node.js server preserves attribution:

```javascript
// Preserve referrer headers
app.use((req, res, next) => {
  // Don't strip referrer for analytics
  res.setHeader('Referrer-Policy', 'no-referrer-when-downgrade');
  next();
});

// For SSR, inject referrer into initial state
app.get('*', (req, res) => {
  const referrer = req.get('Referrer') || '';
  // Pass referrer to your template
  res.render('index', { 
    referrer: referrer,
    landing_page: req.url 
  });
});
```

## Why WordPress → Node.js Breaks Attribution

- **WordPress**: Plugins handle session management, referrer preservation, and proper event sequencing
- **Node.js**: You must manually implement all attribution logic
- **The Gap**: Your dev team implemented basic tracking but not attribution preservation

## Expected Results

After implementing these fixes:
- "(not set)" should drop from 35-40% to under 5%
- Organic traffic will show proper sources
- Campaign parameters will persist correctly
- Management will see accurate channel attribution

## Quick Win

As an immediate test, check if "(not set)" traffic spikes during your highest organic traffic periods. If yes, it confirms the attribution is being lost, not that the traffic is actually direct.

This typically requires 6-8 hours to properly audit and fix across a Node.js application, including testing all entry points and navigation patterns.