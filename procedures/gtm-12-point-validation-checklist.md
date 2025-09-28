# GTM 12-Point Validation Checklist

**Purpose:** Comprehensive validation checklist to ensure GTM implementations are complete, accurate, and optimized before handoff.

---

## Pre-Implementation Checks (Points 1-3)

### ✅ 1. Container Access & Permissions
- [ ] GTM container access verified
- [ ] Correct workspace selected
- [ ] User permissions appropriate for changes
- [ ] Backup/version created before changes

### ✅ 2. Site Infrastructure Verification
- [ ] GTM container snippet in correct location (`<head>` and `<body>`)
- [ ] No duplicate GTM containers loading
- [ ] No conflicting tag managers present
- [ ] WordPress theme compatibility confirmed

### ✅ 3. DataLayer Foundation
- [ ] DataLayer initialized before GTM
- [ ] No JavaScript errors in console
- [ ] DataLayer push events working
- [ ] Variable naming conventions consistent

---

## Core Implementation Checks (Points 4-8)

### ✅ 4. Google Analytics 4 Configuration
- [ ] GA4 Configuration tag present
- [ ] Measurement ID correct
- [ ] Enhanced measurements enabled appropriately
- [ ] Debug mode working in GA4 DebugView

### ✅ 5. Event Tracking Setup
- [ ] Page view tracking confirmed
- [ ] Click tracking operational
- [ ] Form submission tracking working
- [ ] Scroll tracking (if required) active
- [ ] Custom events firing correctly

### ✅ 6. Conversion Tracking
- [ ] Google Ads conversion tags configured
- [ ] Conversion linker tag active
- [ ] Enhanced conversions (if applicable) working
- [ ] Transaction/purchase events (if e-commerce) validated
- [ ] Phone call tracking (if applicable) tested

### ✅ 7. Trigger Configuration
- [ ] All triggers firing at correct times
- [ ] No trigger conflicts or duplicates
- [ ] Page path/URL triggers accurate
- [ ] Custom event triggers validated
- [ ] Blocking triggers working as expected

### ✅ 8. Variable Accuracy
- [ ] Built-in variables enabled as needed
- [ ] Custom JavaScript variables returning correct values
- [ ] DataLayer variables mapping correctly
- [ ] Lookup tables (if used) accurate
- [ ] No undefined variables in tags

---

## Quality & Performance Checks (Points 9-12)

### ✅ 9. Cross-Browser Testing
- [ ] Chrome - all tags firing
- [ ] Safari - all tags firing
- [ ] Firefox - all tags firing
- [ ] Mobile browsers tested
- [ ] No console errors across browsers

### ✅ 10. Data Flow Validation
- [ ] GTM Preview mode showing all events
- [ ] Network tab showing successful requests (200/204 status)
- [ ] GA4 Real-time reports receiving data
- [ ] Google Ads receiving conversions (if applicable)
- [ ] No failed or blocked requests

### ✅ 11. Performance & Loading
- [ ] Tags loading asynchronously
- [ ] No impact on Core Web Vitals
- [ ] Page load time acceptable
- [ ] No render-blocking scripts
- [ ] Tag sequencing (if used) correct

### ✅ 12. Documentation & Handoff
- [ ] Container version published with descriptive notes
- [ ] Tag naming convention documented
- [ ] Custom code commented
- [ ] Testing procedures documented
- [ ] Client training materials provided
- [ ] Emergency rollback plan in place

---

## Usage Instructions

### When to Use This Checklist:
1. **Before going live** with any new GTM implementation
2. **After major updates** to existing containers
3. **During audits** of existing setups
4. **Before client handoff** for all projects

### How to Use:
1. Work through each point systematically
2. Check all sub-items under each point
3. Document any issues found
4. Resolve all critical issues before marking complete
5. Save completed checklist with project documentation

### Validation Methods:
- **Points 1-3:** Manual inspection and console checking
- **Points 4-8:** GTM Preview Mode and GA4 DebugView
- **Points 9-10:** Browser DevTools and real-time reports
- **Points 11-12:** Performance testing tools and documentation review

---

## Quick Reference Testing Tools

### Essential Tools:
- **GTM Preview Mode** - Primary debugging tool
- **GA4 DebugView** - Real-time event validation
- **Browser DevTools** - Network and console monitoring
- **Tag Assistant Legacy** - Chrome extension for validation

### Testing URLs:
```
# Add test parameters to URLs
?gtm_debug=x     # Force GTM debug mode
&gtm_auth=ABC    # Authentication string
&gtm_preview=env-X # Preview environment
&gtm_cookies_win=x # Cookie settings
```

### Console Commands:
```javascript
// Check dataLayer
dataLayer

// Check GTM loaded
google_tag_manager

// Check specific container
google_tag_manager['GTM-XXXXXX']

// Monitor dataLayer pushes
dataLayer.push = function(e) { console.log('DataLayer:', e); Array.prototype.push.call(dataLayer, e); }
```

---

## Sign-off

**Project:** _______________________
**Date Completed:** _______________________
**Validated By:** _______________________
**Client Approval:** _______________________

**Notes:**
_______________________
_______________________
_______________________

---

*This 12-point validation ensures professional, reliable GTM implementations that perform optimally and track accurately.*