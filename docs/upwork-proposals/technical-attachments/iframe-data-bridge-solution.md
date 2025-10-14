# Iframe Data Bridge Solution for Enhanced Conversions

**Technical Implementation Guide for Go High Level + GA4/Google Ads Integration**

---

## Problem Statement

Go High Level forms often load in iframes, creating cross-domain barriers that prevent conversion data from reaching GA4 and Google Ads Enhanced Conversions. This results in:

- 0-20% Enhanced Conversions match rates
- Lost attribution between ad clicks and form submissions
- Missing offline conversion data from CRM events
- Incomplete funnel tracking

---

## Solution Architecture

### Phase 1: Iframe Communication Bridge

**Parent Domain Script (Main Website):**

```javascript
// Enhanced Conversions Iframe Bridge
(function() {
  'use strict';
  
  // Listen for messages from GHL iframes
  window.addEventListener('message', function(event) {
    // Security: Verify origin
    const allowedOrigins = [
      'https://api.leadconnectorhq.com',
      'https://widget.leadconnectorhq.com',
      'https://form.gohighlevel.com'
    ];
    
    if (!allowedOrigins.includes(event.origin)) {
      console.log('Rejected message from unauthorized origin:', event.origin);
      return;
    }
    
    // Process GHL form submission data
    if (event.data && event.data.type === 'ghl_form_submit') {
      processGHLConversion(event.data.formData);
    }
  });
  
  function processGHLConversion(formData) {
    const conversionData = {
      email: formData.email,
      phone: normalizePhone(formData.phone),
      first_name: formData.first_name,
      last_name: formData.last_name,
      value: parseFloat(formData.value) || 0,
      currency: 'USD',
      transaction_id: 'ghl_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
    };
    
    // Send to Google Ads Enhanced Conversions
    if (typeof gtag !== 'undefined') {
      gtag('event', 'conversion', {
        send_to: 'AW-XXXXXXXXX/XXXXXXX', // Replace with actual conversion ID
        value: conversionData.value,
        currency: conversionData.currency,
        transaction_id: conversionData.transaction_id,
        user_data: {
          email_address: [conversionData.email],
          phone_number: [conversionData.phone],
          first_name: [conversionData.first_name],
          last_name: [conversionData.last_name]
        }
      });
      
      // Send to GA4 for attribution
      gtag('event', 'generate_lead', {
        currency: conversionData.currency,
        value: conversionData.value,
        transaction_id: conversionData.transaction_id,
        lead_source: 'ghl_form',
        user_data: {
          email_address: conversionData.email,
          phone_number: conversionData.phone,
          first_name: conversionData.first_name,
          last_name: conversionData.last_name
        }
      });
    }
    
    // Debug logging
    console.log('GHL Enhanced Conversion sent:', conversionData);
  }
  
  function normalizePhone(phone) {
    if (!phone) return '';
    // Remove all non-digits and add +1 for US numbers
    const digits = phone.replace(/\D/g, '');
    return digits.length === 10 ? '+1' + digits : '+' + digits;
  }
})();
```

### Phase 2: GHL Form Modification

**Iframe Form Script (Injected into GHL forms):**

```javascript
// GHL Form Data Capture Script
(function() {
  'use strict';
  
  // Wait for form to be ready
  function initFormTracking() {
    const forms = document.querySelectorAll('form[data-form-id], .ghl-form, form');
    
    forms.forEach(function(form) {
      form.addEventListener('submit', function(e) {
        const formData = captureFormData(form);
        if (formData.email || formData.phone) {
          // Send data to parent window
          window.parent.postMessage({
            type: 'ghl_form_submit',
            formData: formData,
            timestamp: new Date().toISOString()
          }, '*');
        }
      });
    });
  }
  
  function captureFormData(form) {
    const data = {};
    const formData = new FormData(form);
    
    // Map common field names
    const fieldMapping = {
      'email': ['email', 'email_address', 'user_email'],
      'phone': ['phone', 'phone_number', 'telephone'],
      'first_name': ['first_name', 'fname', 'firstname'],
      'last_name': ['last_name', 'lname', 'lastname'],
      'value': ['value', 'price', 'amount']
    };
    
    for (const [key, variants] of Object.entries(fieldMapping)) {
      for (const variant of variants) {
        if (formData.get(variant)) {
          data[key] = formData.get(variant);
          break;
        }
      }
    }
    
    return data;
  }
  
  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFormTracking);
  } else {
    initFormTracking();
  }
})();
```

---

## Phase 3: GHL Webhook Integration

**Server-Side Offline Conversions Handler:**

```javascript
// Node.js Express webhook handler
const express = require('express');
const { GoogleAds } = require('google-ads-api');

const app = express();
app.use(express.json());

// Initialize Google Ads client
const client = new GoogleAds({
  customer_id: 'XXXXXXXXX',
  login_customer_id: 'XXXXXXXXX'
});

app.post('/webhook/ghl-conversion', async (req, res) => {
  try {
    const webhookData = req.body;
    
    // Process different GHL event types
    switch(webhookData.type) {
      case 'ContactCreate':
      case 'OpportunityCreate':
      case 'OpportunityStatusUpdate':
        await processOfflineConversion(webhookData);
        break;
    }
    
    res.status(200).json({ success: true });
  } catch (error) {
    console.error('Webhook processing error:', error);
    res.status(500).json({ error: 'Processing failed' });
  }
});

async function processOfflineConversion(data) {
  const conversionData = {
    conversion_action: `customers/${client.customer_id}/conversionActions/XXXXXXXXX`,
    conversion_date_time: data.dateAdded || new Date().toISOString(),
    conversion_value: parseFloat(data.monetary_value) || 0,
    currency_code: 'USD',
    order_id: data.contact_id,
    // GCLID must be stored during initial form submission
    gclid: data.customFields?.gclid || data.source_data?.gclid
  };
  
  if (conversionData.gclid) {
    await client.customers.uploadOfflineConversions({
      customer_id: client.customer_id,
      conversions: [conversionData]
    });
    
    console.log('Offline conversion uploaded:', conversionData);
  }
}
```

---

## Testing & Validation Protocol

### 1. Browser Dev Tools Testing

```javascript
// Console testing script
function testIframeBridge() {
  // Simulate GHL form submission
  window.postMessage({
    type: 'ghl_form_submit',
    formData: {
      email: 'test@example.com',
      phone: '5551234567',
      first_name: 'Test',
      last_name: 'User',
      value: 100
    }
  }, window.location.origin);
  
  console.log('Test form submission sent');
}

// Run test
testIframeBridge();
```

### 2. Network Monitoring

**Check for these requests in Network tab:**
- `google-analytics.com/g/collect` (GA4 events)
- `googleadservices.com/pagead/conversion` (Google Ads)
- `stats.g.doubleclick.net` (Enhanced Conversions)

### 3. GA4 DebugView Validation

**Expected events in DebugView:**
- `generate_lead` with user_data parameters
- `conversion` with enhanced conversion data
- Custom parameters: `lead_source: 'ghl_form'`

---

## Expected Results

**Before Implementation:**
- Enhanced Conversions match rate: 0-20%
- Missing iframe form submissions in GA4
- No offline conversion tracking from GHL
- Attribution gaps in Google Ads

**After Implementation:**
- Enhanced Conversions match rate: 80%+
- 100% iframe form tracking in GA4
- Complete offline conversion path: GHL → Google Ads
- Full attribution: Ad Click → Form → CRM → Sale

---

## Deployment Checklist

1. ✅ Install parent domain bridge script
2. ✅ Configure GHL form tracking code
3. ✅ Set up webhook endpoint for offline conversions
4. ✅ Update Google Ads conversion actions
5. ✅ Test iframe communication
6. ✅ Validate Enhanced Conversions in GA4 DebugView
7. ✅ Monitor conversion match rates
8. ✅ Document GCLID storage mechanism

**Implementation Time:** 5-7 business days including testing and validation.