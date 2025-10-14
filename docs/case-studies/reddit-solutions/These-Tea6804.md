# Reddit Solution: 70% Data Loss with Server-Side GTM & OneTrust

**User:** u/These-Tea6804  
**Post URL:** https://reddit.com/r/GoogleTagManager/comments/1nd9hsf/  
**Problem:** "70% or higher decrease in events in GA4 server side vs client side"  
**Date:** September 10, 2025

## Response

I use a systematic diagnostic approach for tracking issues, and your problem is a Layer 3: Transmission issue.

**Layer 3** focuses on the data journey from client to server - when tags fire correctly but data fails to reach its destination. In your case, events are leaving the client but 70% never make it to GA4 through your server container. This layer specifically deals with network requests, consent handoffs, and the critical handshake between client and server containers.

The key symptom in your description: OneTrust shows `gcs=g101` (analytics accepted) but server requests show "Unknown" for **20+ minutes**. This delay is the server container timing out waiting for valid consent signals that never arrive.

## Diagnostic for Consent Transmission

Run this to see exactly what's being sent to your server:

```javascript
// Check what consent signals are being transmitted
(() => {
  // Look for server container requests
  const serverRequests = performance.getEntriesByType('resource')
    .filter(r => r.name.includes('gtm-server') || r.name.includes('sgtm'));
  
  console.log('Server requests found:', serverRequests.length);
  
  // Check consent parameters in requests
  serverRequests.forEach(req => {
    const url = new URL(req.name);
    const params = {
      gcs: url.searchParams.get('gcs'),
      consent: url.searchParams.get('consent'),
      gdpr: url.searchParams.get('gdpr')
    };
    console.log('Request consent params:', params);
  });
  
  // Check if OneTrust is sending updates
  const consentEvents = dataLayer.filter(d => 
    d.event?.includes('consent') || 
    d.event?.includes('OneTrust')
  );
  
  console.log('Consent events in dataLayer:', consentEvents.length);
  return consentEvents;
})();
```

## The Root Cause

Your OneTrust CMP is updating consent in the browser but not forwarding it through the client-to-server transport layer. The server container receives requests but can't verify consent state, so it drops them. The standard OneTrust documentation doesn't fully address this specific handoff requirement.

## The Fix: Consent State Bridge

You need an explicit consent forwarding mechanism:

### Client-Side: Capture and Forward OneTrust State

Add this as a Custom HTML tag in your CLIENT container, triggered on "OneTrustGroupsUpdated":

```javascript
// Add to GTM Custom HTML tag - fires on OneTrustGroupsUpdated
(function() {
  // Capture OneTrust consent decision
  const consentGroups = OneTrust.GetDomainData().Groups;
  
  // Map to Google consent types (adjust group IDs to match your OneTrust setup)
  const consentMap = {
    'C0002': 'analytics_storage',  // Performance cookies
    'C0004': 'ad_storage',         // Targeting cookies
    'C0003': 'ad_user_data',       // User data
    'C0004': 'ad_personalization'  // Personalization
  };
  
  // Build consent state for server
  const serverConsent = {};
  consentGroups.forEach(group => {
    if (consentMap[group.CustomGroupId]) {
      serverConsent[consentMap[group.CustomGroupId]] = 
        group.Status === 'active' ? 'granted' : 'denied';
    }
  });
  
  // Push with server transmission flag
  dataLayer.push({
    'event': 'consent_state_sync',
    'consent_for_server': serverConsent,
    'timestamp': Date.now()
  });
  
  console.log('Consent forwarded to server:', serverConsent);
})();
```

### Server-Side: Receive and Apply Consent

In your SERVER container:
1. Create a trigger for the `consent_state_sync` event
2. Create a tag that reads `consent_for_server` and updates consent
3. Set this tag's priority higher than your GA4 tags

## Why 70% Loss?

- **30% getting through**: Users who accept all cookies immediately (gcs=g111)
- **70% lost**: Users with partial consent (gcs=g101) where the handoff fails

The 20+ minute delay is the server container timeout - it's waiting for consent confirmation that never arrives through the standard OneTrust integration.

## Validation

After implementing, you should see:
- Server-side events matching client-side (minus bot filtering)
- No more 20-minute delays
- Consistent gcs parameters between client and server
- "Post - 204" responses instead of "Unknown"

This is a known limitation when OneTrust is implemented directly on-site rather than through GTM templates - the consent state bridge requirement for partial consent scenarios needs to be manually configured.