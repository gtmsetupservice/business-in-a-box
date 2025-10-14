# Google Ads Conversion Tracking Pattern Documentation

## Discovery Summary
Through testing on woo-potterhead.local, we identified the exact requirements for Google Ads conversion tracking to function without the full Google Ads tag implementation.

## Critical Requirement: The `aw-` Prefix

The `aw-` prefix is **mandatory** for Google Ads conversion tracking to function. This prefix must be present in:
1. The Google Tag ID field when creating the initialization tag
2. The Conversion ID variable value
3. The resulting network request URL

## Working Configuration

### 1. Google Tag (Initialization Tag)
**Purpose**: Establishes Google Ads measurement context on page load

- **Tag Type**: Google Tag
- **Tag ID**: `aw-XXXXXXXXX` (where XXXXXXXXX is your Google Ads account ID)
- **Trigger**: Initialization - All Pages
- **When it fires**: On every page load, before other tags

### 2. Conversion ID Variable
**Purpose**: Stores the Google Ads account ID for reuse in conversion tags

- **Variable Type**: Constant
- **Variable Name**: Can be any name (e.g., "Fake Google Ads Conversion ID")
- **Value**: `aw-XXXXXXXXX` (must include the `aw-` prefix)
- **Used by**: Google Ads Conversion Tracking tags

### 3. Conversion Linker Tag
**Purpose**: Improves conversion tracking accuracy by storing click information

- **Tag Type**: Conversion Linker
- **Trigger**: Initialization - All Pages
- **Function**: Stores GCLID and other click identifiers in first-party cookies

### 4. Google Ads Conversion Tracking Tag
**Purpose**: Fires the actual conversion event

- **Tag Type**: Google Ads Conversion Tracking
- **Conversion ID**: Reference to the variable containing `aw-XXXXXXXXX`
- **Conversion Label**: Your specific conversion label (e.g., "EXTERNAL_CLICK_TEST")
- **Conversion Value**: The monetary value or use a variable
- **Currency Code**: USD or your currency
- **Trigger**: Your conversion event (e.g., External Link Click, Purchase, Form Submit)

## How the Chain Works

1. **Page Load**: Google Tag with `aw-XXXXXXXXX` fires on initialization
2. **Context Established**: This creates the Google Ads measurement context in the browser
3. **User Action**: User performs conversion action (clicks link, submits form, etc.)
4. **Conversion Fires**: Conversion Tracking tag fires, using the variable with `aw-` prefix
5. **Data Sent**: Request sent to `googleadservices.com/pagead/conversion/aw-XXXXXXXXX/`

## Network Request Validation

### What to Look For in Developer Tools

1. **On Page Load**:
   - Request to: `www.googletagmanager.com/gtag/js?id=aw-XXXXXXXXX`
   - This confirms the Google Tag initialized properly

2. **On Conversion Event**:
   - Request to: `https://www.googleadservices.com/pagead/conversion/aw-XXXXXXXXX/`
   - Check the request parameters:
     - `label`: Your conversion label
     - `value`: Conversion value
     - `currency_code`: Currency
     - `en`: Event name (e.g., "purchase")
     - `url`: Page where conversion occurred

### Example Successful Conversion Request
```
URL: https://www.googleadservices.com/pagead/conversion/aw-123456789/
Parameters:
  label: EXTERNAL_CLICK_TEST
  value: 5000
  currency_code: USD
  en: purchase
  bttype: purchase
  url: http://woo-potterhead.local/
```

## Testing Procedure

### Browser Console Verification

```javascript
// 1. Check if Google Ads context exists
window.google_tag_data && window.google_tag_data.ics ? 
  'âœ… Google Ads context established' : 
  'âŒ No Google Ads context';

// 2. Monitor conversion requests in real-time
const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
        if (entry.name.includes('googleadservices.com/pagead/conversion/')) {
            console.log('âœ… Conversion fired:', entry.name);
        }
    }
});
observer.observe({ entryTypes: ['resource'] });

// 3. Check for aw- prefix in active tags
Object.keys(window.google_tag_manager || {}).forEach(key => {
    if (key.includes('aw-')) {
        console.log('âœ… Found Google Ads tag:', key);
    }
});
```

### Manual Testing Steps

1. **Enable Network Tab**:
   - Open Chrome Developer Tools (F12)
   - Go to Network tab
   - Filter by: "google"

2. **Load Page**:
   - Refresh the page
   - Verify you see: `gtag/js?id=aw-XXXXXXXXX`

3. **Trigger Conversion**:
   - Perform the conversion action
   - Look for: `googleadservices.com/pagead/conversion/`
   - Click on the request and check "Payload" tab for parameters

## Common Issues and Solutions

### Issue: "Cannot detect if the Google tag is in your container"
**Solution**: This GTM warning can be ignored when using variables. It's a false positive. As long as the Google Tag with `aw-` prefix fires on init, conversions will work.

### Issue: Conversion tag fires but no data in Google Ads
**Cause**: Missing or incorrect `aw-` prefix
**Solution**: Ensure `aw-` prefix is present in both the Google Tag ID and Conversion ID variable

### Issue: No conversion request in Network tab
**Possible Causes**:
1. Google Tag not firing on initialization
2. Missing `aw-` prefix in configuration
3. Trigger conditions not met
4. Ad blocker interference

## Key Insights

1. **The `aw-` prefix is non-negotiable** - Without it, Google Ads will not recognize the conversion
2. **Variable references work** - Despite GTM warnings, using variables for Conversion ID is valid
3. **Initialization order matters** - The Google Tag must fire before conversion tags
4. **Tag Assistant validation** - Seeing "AW-aw-XXXXXXXXX" in Tag Assistant confirms proper setup

## Implementation Checklist

- [ ] Create Google Tag with `aw-XXXXXXXXX` ID
- [ ] Set trigger to "Initialization - All Pages"
- [ ] Create Constant variable with `aw-XXXXXXXXX` value
- [ ] Create Conversion Linker tag (Initialization trigger)
- [ ] Create Conversion Tracking tag with:
  - [ ] Conversion ID using the variable
  - [ ] Appropriate conversion label
  - [ ] Value and currency settings
  - [ ] Correct trigger for your conversion event
- [ ] Test in Preview mode
- [ ] Verify in Network tab
- [ ] Confirm in Tag Assistant
- [ ] Check Google Ads account for test conversions

## Summary

This pattern enables Google Ads conversion tracking by:
1. Establishing Google Ads context with a properly prefixed (`aw-`) Google Tag on initialization
2. Using that context for subsequent conversion tracking events
3. Properly formatting all account IDs with the required `aw-` prefix

The discovery that the `aw-` prefix is mandatory in the variable value (not just the display) was the key breakthrough that made conversion tracking functional.