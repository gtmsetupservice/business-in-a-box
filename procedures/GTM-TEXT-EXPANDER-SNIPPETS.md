# GTM Text Expander Snippets - Professional Console Debugging

**For GTMSetupService.com Client Support & Training**

## 🚀 Quick GTM Health Check

**Abbreviation:** `;gtmcheck`  
**Use Case:** Instant GTM diagnostic for client sites

```javascript
// GTM Professional Health Check - GTMSetupService.com
console.log('🔍 GTM HEALTH CHECK');
console.log('===================');

// 1. Container Status
if (typeof google_tag_manager !== 'undefined') {
    console.log('✅ GTM Loaded');
    const containers = Object.keys(google_tag_manager).filter(k => k.startsWith('GTM-'));
    console.log('📦 Containers:', containers);
    containers.forEach(c => console.log(`   🔧 ${c}:`, google_tag_manager[c] ? 'Active' : 'Inactive'));
} else {
    console.log('❌ GTM Not Loaded');
}

// 2. DataLayer Health
if (typeof dataLayer !== 'undefined') {
    console.log('✅ DataLayer Active');
    console.log('📊 Events:', dataLayer.length);
    const events = dataLayer.slice(-5).map(e => e.event || 'data').filter(Boolean);
    console.log('📋 Recent Events:', events.join(', '));
} else {
    console.log('❌ DataLayer Missing');
}

// 3. Test Event
dataLayer.push({
    'event': 'gtm_health_check', 
    'debug_source': 'gtmsetupservice_console',
    'timestamp': new Date().toISOString(),
    'page_url': window.location.href
});
console.log('🚀 Test Event Fired: gtm_health_check');

// 4. Script Analysis
const gtmScripts = document.querySelectorAll('script[src*="googletagmanager"]');
console.log('📄 GTM Scripts:', gtmScripts.length);
gtmScripts.forEach((script, i) => {
    const type = script.src.includes('/gtm.js') ? 'GTM Container' : 
                 script.src.includes('/gtag/js') ? 'GA4 via GTM' : 'Other';
    console.log(`   📜 Script ${i+1}: ${type}`);
});

// 5. Implementation Verification
console.log('🔧 Head Implementation:', document.head.innerHTML.includes('googletagmanager'));
console.log('🔧 Noscript Fallback:', document.body.innerHTML.includes('ns.html'));

// 6. Performance Check
console.log('⚡ Page Load Events:', dataLayer.filter(e => ['gtm.js', 'gtm.dom', 'gtm.load'].includes(e.event)).length);

console.log('✅ Debug Complete - Professional GTM Analysis');
console.log('💡 Next: Enable GTM Preview Mode for live tag testing');
```

## 🎯 Event Testing Suite

**Abbreviation:** `;gtmtest`  
**Use Case:** Test custom event firing and validation

```javascript
// GTM Event Testing Suite - GTMSetupService.com
console.log('🧪 GTM EVENT TESTING');
console.log('=====================');

// Test 1: Basic Custom Event
console.log('Test 1: Basic Event Firing');
dataLayer.push({
    'event': 'test_basic_event',
    'test_id': 'console_test_' + Date.now(),
    'test_timestamp': new Date().toISOString()
});

// Test 2: Ecommerce Event Structure
console.log('Test 2: Ecommerce Event Structure');
dataLayer.push({
    'event': 'test_purchase',
    'ecommerce': {
        'transaction_id': 'TEST_' + Date.now(),
        'value': 99.99,
        'currency': 'USD',
        'items': [{
            'item_name': 'Test Product',
            'item_category': 'Testing',
            'quantity': 1,
            'price': 99.99
        }]
    }
});

// Test 3: Form Submission Event
console.log('Test 3: Form Event');
dataLayer.push({
    'event': 'test_form_submit',
    'form_id': 'contact_form',
    'form_name': 'Console Test Form'
});

// Verification
setTimeout(() => {
    console.log('📊 Latest Events:');
    dataLayer.slice(-3).forEach((event, i) => {
        console.log(`   ${i+1}. ${event.event} (ID: ${event.gtm.uniqueEventId})`);
    });
}, 100);

console.log('✅ Test Events Fired - Check GTM Preview Mode');
```

## 🔍 Advanced Diagnostics

**Abbreviation:** `;gtmdiag`  
**Use Case:** Deep diagnostic for complex issues

```javascript
// GTM Advanced Diagnostics - GTMSetupService.com
console.log('🔬 GTM ADVANCED DIAGNOSTICS');
console.log('============================');

// 1. Container Deep Analysis
console.log('1. Container Analysis:');
if (typeof google_tag_manager !== 'undefined') {
    Object.keys(google_tag_manager).forEach(key => {
        if (key.startsWith('GTM-')) {
            const container = google_tag_manager[key];
            console.log(`   📦 ${key}:`);
            console.log(`      Bootstrap: ${new Date(container.bootstrap)}`);
            console.log(`      DataLayer: ${container.dataLayer ? 'Connected' : 'Missing'}`);
        }
    });
}

// 2. Network Request Analysis
console.log('2. Network Analysis (Check Network Tab):');
const gtmRequests = performance.getEntriesByType('resource').filter(r => 
    r.name.includes('googletagmanager.com')
);
console.log(`   📡 GTM Requests: ${gtmRequests.length}`);
gtmRequests.forEach(req => {
    console.log(`      ${req.name.split('?')[0]} - ${req.duration.toFixed(2)}ms`);
});

// 3. Error Detection
console.log('3. Error Detection:');
const errors = window.addEventListener('error', function(e) {
    if (e.message.includes('gtm') || e.message.includes('dataLayer')) {
        console.warn('   ⚠️ GTM-related error:', e.message);
    }
});

// 4. Tag Manager State
console.log('4. Tag Manager State:');
console.log(`   Sequence: ${google_tag_manager.sequence || 'Unknown'}`);
console.log(`   Debug Mode: ${google_tag_manager.debugGroupId ? 'Active' : 'Inactive'}`);

// 5. DataLayer Event Analysis
console.log('5. DataLayer Event Analysis:');
const eventTypes = {};
dataLayer.forEach(item => {
    if (item.event) {
        eventTypes[item.event] = (eventTypes[item.event] || 0) + 1;
    }
});
console.log('   📊 Event Frequency:', eventTypes);

// 6. DOM Integration Check
console.log('6. DOM Integration:');
console.log(`   GTM in HTML: ${document.documentElement.outerHTML.includes('googletagmanager')}`);
console.log(`   DataLayer Global: ${window.dataLayer === dataLayer}`);

console.log('✅ Advanced Diagnostics Complete');
console.log('📋 Review all sections above for issues');
```

## 🚨 Error Analysis

**Abbreviation:** `;gtmerror`  
**Use Case:** Specific error debugging and troubleshooting

```javascript
// GTM Error Analysis - GTMSetupService.com
console.log('🚨 GTM ERROR ANALYSIS');
console.log('======================');

// 1. Basic Availability Check
console.log('1. Availability Check:');
console.log(`   google_tag_manager: ${typeof google_tag_manager}`);
console.log(`   dataLayer: ${typeof dataLayer}`);
console.log(`   gtag: ${typeof gtag}`);

// 2. Common Error Patterns
console.log('2. Common Issues:');

// Check for dataLayer before GTM
if (typeof dataLayer !== 'undefined') {
    const hasPreGTM = dataLayer.some(item => !item.hasOwnProperty('gtm.uniqueEventId'));
    console.log(`   DataLayer pre-GTM events: ${hasPreGTM ? '✅ Good' : '⚠️ Check timing'}`);
}

// Check for multiple containers
if (typeof google_tag_manager !== 'undefined') {
    const containers = Object.keys(google_tag_manager).filter(k => k.startsWith('GTM-'));
    if (containers.length > 1) {
        console.warn(`   ⚠️ Multiple Containers: ${containers.join(', ')}`);
    }
}

// Check for blocked requests
const blockedRequests = performance.getEntriesByType('resource')
    .filter(r => r.name.includes('googletagmanager') && r.transferSize === 0);
if (blockedRequests.length > 0) {
    console.warn('   ⚠️ Blocked Requests:', blockedRequests.length);
}

// 3. Console Error Monitoring
console.log('3. Error Monitoring (5 seconds):');
const originalError = console.error;
const gtmErrors = [];
console.error = function(...args) {
    const message = args.join(' ');
    if (message.includes('gtm') || message.includes('dataLayer') || message.includes('googletagmanager')) {
        gtmErrors.push(message);
    }
    originalError.apply(console, args);
};

setTimeout(() => {
    console.error = originalError;
    if (gtmErrors.length > 0) {
        console.warn('   🔥 GTM Errors Found:', gtmErrors);
    } else {
        console.log('   ✅ No GTM errors detected');
    }
}, 5000);

console.log('⏳ Monitoring for 5 seconds...');
```

## 📱 Mobile-Specific Debug

**Abbreviation:** `;gtmmobile`  
**Use Case:** Mobile device GTM debugging

```javascript
// GTM Mobile Debug - GTMSetupService.com
console.log('📱 GTM MOBILE DEBUG');
console.log('===================');

// 1. Device Detection
console.log('1. Device Info:');
console.log(`   User Agent: ${navigator.userAgent}`);
console.log(`   Screen: ${screen.width}x${screen.height}`);
console.log(`   Viewport: ${window.innerWidth}x${window.innerHeight}`);
console.log(`   Touch Support: ${('ontouchstart' in window) ? 'Yes' : 'No'}`);

// 2. Performance Impact
console.log('2. Performance:');
const gtmResources = performance.getEntriesByType('resource')
    .filter(r => r.name.includes('googletagmanager'));
const totalTime = gtmResources.reduce((sum, r) => sum + r.duration, 0);
console.log(`   GTM Load Time: ${totalTime.toFixed(2)}ms`);
console.log(`   Resource Count: ${gtmResources.length}`);

// 3. Mobile-Specific Events
console.log('3. Mobile Events Test:');
dataLayer.push({
    'event': 'mobile_debug_test',
    'device_type': screen.width < 768 ? 'mobile' : 'desktop',
    'connection': navigator.connection ? navigator.connection.effectiveType : 'unknown',
    'viewport_width': window.innerWidth
});

// 4. Scroll Tracking
console.log('4. Scroll Tracking:');
const scrollEvents = dataLayer.filter(e => e.event === 'gtm.scrollDepth');
console.log(`   Scroll Events: ${scrollEvents.length}`);

console.log('✅ Mobile Debug Complete');
```

## 🎓 Training Mode

**Abbreviation:** `;gtmlearn`  
**Use Case:** Educational debugging for training sessions

```javascript
// GTM Learning Mode - GTMSetupService.com Training
console.log('🎓 GTM LEARNING SESSION');
console.log('========================');

console.log('📚 Step 1: Understanding the GTM Object');
console.log('The google_tag_manager object contains:');
if (typeof google_tag_manager !== 'undefined') {
    Object.keys(google_tag_manager).forEach(key => {
        console.log(`   ${key}: ${typeof google_tag_manager[key]}`);
    });
}

console.log('\n📚 Step 2: DataLayer Structure');
console.log('DataLayer is an array where each item is an event or data:');
if (typeof dataLayer !== 'undefined') {
    dataLayer.slice(0, 3).forEach((item, i) => {
        console.log(`   Item ${i}:`, item);
    });
}

console.log('\n📚 Step 3: Event Firing Process');
console.log('When you push an event:');
console.log('   1. Event added to dataLayer array');
console.log('   2. GTM assigns unique ID');  
console.log('   3. Triggers evaluate conditions');
console.log('   4. Matching tags fire');

dataLayer.push({
    'event': 'learning_example',
    'category': 'education',
    'action': 'console_training'
});

console.log('\n📚 Step 4: Verification');
console.log('Your learning event:', dataLayer[dataLayer.length - 1]);

console.log('\n🎯 Learning Complete!');
console.log('💡 Try: Enable GTM Preview Mode for visual debugging');
```

---

## 📋 Usage Instructions

### Text Expander Setup:
1. **TextExpander/Alfred/Espanso:** Create new snippet
2. **Abbreviation:** Use provided shortcuts (e.g., `;gtmcheck`)
3. **Content:** Copy the JavaScript code block
4. **Format:** Plain text (will auto-format in console)

### Console Usage:
1. **Open any website** with GTM
2. **Press F12** → Console tab
3. **Type abbreviation** → Text expander inserts code
4. **Press Enter** to execute
5. **Review results** for issues

### Professional Application:
- **Client Audits:** Quick health checks
- **Support Calls:** Real-time debugging  
- **Training Sessions:** Educational demonstrations
- **Quality Assurance:** Implementation verification

**These snippets tested and validated on gtmsetupservice.com production environment.**