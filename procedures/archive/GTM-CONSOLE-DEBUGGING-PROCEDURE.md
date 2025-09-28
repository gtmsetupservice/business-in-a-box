# GTM Console Debugging Procedure - Professional Client Support

**For GTMSetupService.com Professional Implementations**

## 🎯 Overview

This procedure provides a systematic approach to debugging GTM implementations using browser console commands. Developed through live testing on gtmsetupservice.com production environment.

## 📋 Step-by-Step Console Debugging Workflow

### Step 1: GTM Container Health Check
**Command:**
```javascript
google_tag_manager
```

**Purpose:** Verify GTM is loaded and functional  
**Expected Result:** Object containing container data  
**If undefined:** GTM failed to load - check script installation  

**Success indicators:**
- Container ID appears in object (e.g., GTM-XXXXXXX)
- Bootstrap timestamp present
- dataLayer object present

### Step 2: DataLayer Event Analysis
**Command:**
```javascript
dataLayer
```

**Purpose:** Review all events sent to GTM  
**Expected Result:** Array of event objects  
**Key events to look for:**
- `gtm.js` - Container initialization
- `gtm.dom` - DOM ready
- `gtm.load` - Page fully loaded
- Custom events (form submissions, clicks, etc.)

**Analysis:**
- Length should be 3+ for normal page load
- Events should have `gtm.uniqueEventId` values
- Scroll events indicate enhanced measurement active

### Step 3: Custom Event Testing
**Command:**
```javascript
dataLayer.push({'event': 'console_test', 'debug_source': 'gtm_health_check', 'timestamp': new Date().toISOString()})
```

**Purpose:** Test event firing mechanism  
**Expected Result:** `true` return value  
**Follow-up:** Check if event appears in dataLayer

**Verification Command:**
```javascript
dataLayer[dataLayer.length - 1]
```

**Should show:** Your test event with GTM-assigned uniqueEventId

### Step 4: Script Implementation Verification
**Command:**
```javascript
document.querySelectorAll('script[src*="googletagmanager"]').length
```

**Purpose:** Count GTM script tags  
**Expected Results:**
- **1:** Single GTM implementation (JavaScript only)
- **2:** Professional implementation (JavaScript + noscript fallback)
- **3+:** Potential duplicate/conflict issues

**Detailed Analysis Command:**
```javascript
document.querySelectorAll('script[src*="googletagmanager"]').forEach((script, i) => console.log(`Script ${i+1}:`, script.src))
```

### Step 5: Implementation Source Analysis
**Command:**
```javascript
console.log('GTM Head:', document.head.innerHTML.includes('GTM-XXXXXXX')); console.log('GTM Body:', document.body.innerHTML.includes('GTM-XXXXXXX'));
```

**Purpose:** Confirm proper placement of GTM code  
**Replace:** `GTM-XXXXXXX` with actual container ID  

### Step 6: Advanced Diagnostics
**Container-Specific Check:**
```javascript
window.google_tag_manager['GTM-XXXXXXX']
```

**Network Validation:**
1. Open DevTools → Network tab
2. Filter: `googletagmanager`
3. Refresh page
4. Verify: gtm.js loads with 200 status

**DataLayer Event Filtering:**
```javascript
dataLayer.filter(item => item.event !== undefined)
```

## 🚨 Common Issues & Solutions

### Issue: `google_tag_manager` returns `undefined`
**Diagnosis:** GTM not loaded  
**Solutions:**
- Check for JavaScript errors blocking execution
- Verify GTM script in page source
- Test in incognito mode (ad blocker issues)
- Check network connectivity to googletagmanager.com

### Issue: Empty or minimal dataLayer
**Diagnosis:** GTM not firing or blocked  
**Solutions:**
- Check for Content Security Policy blocking
- Verify script placement (should be in `<head>`)
- Test with GTM Preview Mode

### Issue: Multiple script tags (3+)
**Diagnosis:** Duplicate GTM implementations  
**Solutions:**
- Audit all tracking code sources
- Remove hardcoded GTM tags
- Deactivate conflicting plugins

### Issue: Test events not appearing
**Diagnosis:** DataLayer communication broken  
**Solutions:**
- Check JavaScript console for errors
- Verify dataLayer array is mutable
- Test with simpler event structure

## 💻 Text Expander Script

**Abbreviation:** `;gtmcheck`

**Expansion:**
```javascript
// GTM Professional Health Check - GTMSetupService.com
console.log('🔍 GTM HEALTH CHECK');
console.log('===================');

// 1. Container Status
if (typeof google_tag_manager !== 'undefined') {
    console.log('✅ GTM Loaded');
    console.log('📦 Containers:', Object.keys(google_tag_manager).filter(k => k.startsWith('GTM-')));
} else {
    console.log('❌ GTM Not Loaded');
}

// 2. DataLayer Health
if (typeof dataLayer !== 'undefined') {
    console.log('✅ DataLayer Active');
    console.log('📊 Events:', dataLayer.length);
    console.log('📋 Recent:', dataLayer.slice(-3).map(e => e.event || 'data').join(', '));
} else {
    console.log('❌ DataLayer Missing');
}

// 3. Test Event
dataLayer.push({'event': 'gtm_health_check', 'debug_timestamp': new Date().toISOString()});
console.log('🚀 Test Event Fired');

// 4. Script Count
console.log('📄 GTM Scripts:', document.querySelectorAll('script[src*="googletagmanager"]').length);

// 5. Implementation Check
console.log('🔧 GTM in Head:', document.head.innerHTML.includes('googletagmanager'));
console.log('🔧 GTM in Body:', document.body.innerHTML.includes('ns.html'));

console.log('✅ Debug Complete - Review above results');
```

## 📞 Professional Support Escalation

**When to escalate:**
- GTM object undefined after script verification
- DataLayer events not firing consistently
- Multiple container conflicts detected
- Network requests failing to googletagmanager.com

**Information to gather:**
1. Console output from all debugging steps
2. Screenshot of Network tab showing GTM requests
3. WordPress plugin list and theme details
4. Any JavaScript console errors

**GTMSetupService.com Support:**
- Emergency: Critical tracking failures
- Standard: Implementation review and optimization
- Training: Team education on debugging procedures

## 🎯 Success Criteria

**Healthy GTM Implementation Checklist:**
- [x] `google_tag_manager` object present
- [x] DataLayer contains initialization events
- [x] Custom test events fire successfully
- [x] Script count appropriate (1-2 expected)
- [x] No JavaScript console errors
- [x] GTM Preview Mode connects successfully
- [x] Network requests to googletagmanager.com succeed

**Professional Implementation Indicators:**
- [x] Both head script AND noscript fallback present
- [x] Container ID matches client configuration
- [x] Events have proper GTM uniqueEventId assignment
- [x] Enhanced measurement events appear (scroll, click, etc.)

---

**This procedure tested and validated on gtmsetupservice.com production environment. Updated based on real-world debugging scenarios.**