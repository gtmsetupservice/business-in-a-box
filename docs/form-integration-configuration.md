# GTMSetupService.com Form Integration Configuration

## Overview

This document describes the complete form submission workflow for gtmsetupservice.com, including webhook handling, data storage, and notification systems.

## Architecture

```
Contact Form (gtmsetupservice.com)
    ↓
Pipedream Webhook
    ↓
├─→ Google Sheets (Data Storage)
└─→ Slack Notification (DM Alert)
```

## 1. Webhook Endpoint

**URL:** `https://eocrrf0lm1scxwv.m.pipedream.net`

**Method:** POST

**Content-Type:** application/json

## 2. Form Payload Structure

### JSON Payload

```json
{
  "email": "test@example.com",
  "name": "Test User",
  "phone": "+1-555-123-4567",
  "website": "https://example.com",
  "problem": "GTM container not loading",
  "details": "GTM debug mode shows no container, Google Ads conversion tracking broken",
  "service_type": "emergency_fix",
  "source_domain": "gtmsetupservice.com",
  "utm_source": "test",
  "utm_medium": "webhook_test",
  "utm_campaign": "form_integration",
  "form_submitted": "2025-10-20T09:30:00.000Z"
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | Contact email address |
| `name` | string | Yes | Full name of submitter |
| `phone` | string | No | Contact phone number (E.164 format recommended) |
| `website` | string | Yes | Client's website URL |
| `problem` | string | Yes | Brief problem description |
| `details` | string | Yes | Detailed problem description |
| `service_type` | string | Yes | Service requested (emergency_fix, complete_audit, monitoring) |
| `source_domain` | string | Yes | Domain where form was submitted |
| `utm_source` | string | No | UTM tracking - traffic source |
| `utm_medium` | string | No | UTM tracking - marketing medium |
| `utm_campaign` | string | No | UTM tracking - campaign name |
| `form_submitted` | string (ISO 8601) | Yes | Timestamp of form submission |

### Service Type Values

- `emergency_fix` - Emergency GTM Recovery ($397)
- `complete_audit` - Complete GTM Audit ($797)
- `monitoring` - Monthly GTM Health Monitoring ($197/month)

## 3. Pipedream Workflow Configuration

### Workflow Steps

#### Step 1: HTTP Trigger
- **Type:** HTTP / Webhook
- **Method:** POST
- **Authentication:** None (open webhook)
- **Trigger URL:** https://eocrrf0lm1scxwv.m.pipedream.net

#### Step 2: Google Sheets Integration
- **Action:** Add Single Row
- **Spreadsheet ID:** 1wB3KU8Dsx8mSIfJlEyfszruo_tFbaykk8j7HjeiYB-A
- **Sheet Name:** `import`
- **Starting Cell:** A3 (headers in row 1, data starts row 3)

**Column Mapping:**
```
Column A: email
Column B: name
Column C: phone
Column D: website
Column E: problem
Column F: details
Column G: service_type
Column H: source_domain
Column I: utm_source
Column J: utm_medium
Column K: utm_campaign
Column L: form_submitted
```

#### Step 3: Slack Notification
- **Account:** vscodr.brad@gmail.com
- **Channel Type:** User / Direct Message (DM)
- **Format:** Slack mrkdwn
- **Include Link to Pipedream:** true
- **Unfurl Links:** false

**Message Template:**
```
🚨 *New Form Submission*

*Name:* {{steps.trigger.event.body.name}}
*Email:* {{steps.trigger.event.body.email}}
*Phone:* {{steps.trigger.event.body.phone}}
*Website:* {{steps.trigger.event.body.website}}

*Problem:* {{steps.trigger.event.body.problem}}
*Details:* {{steps.trigger.event.body.details}}

*Service Type:* {{steps.trigger.event.body.service_type}}

*UTM Source:* {{steps.trigger.event.body.utm_source}}
*UTM Medium:* {{steps.trigger.event.body.utm_medium}}
*UTM Campaign:* {{steps.trigger.event.body.utm_campaign}}

✅ Data has been saved to your spreadsheet
```

## 4. Google Sheets Configuration

### Spreadsheet Details
- **Name:** GTM-Form-1
- **Spreadsheet ID:** 1wB3KU8Dsx8mSIfJlEyfszruo_tFbaykk8j7HjeiYB-A
- **Sheet Name:** import
- **Access:** Google account vscodr.brad@gmail.com

### CSV Header Row

```csv
email,name,phone,website,problem,details,service_type,source_domain,utm_source,utm_medium,utm_campaign,form_submitted
```

### Data Format
- **Row 1:** Column headers
- **Row 2:** (Reserved/empty)
- **Row 3+:** Form submission data (auto-populated by Pipedream)

### Cell Ranges
- Updated range per submission: `import!A{row}:L{row}`
- Typically: `import!A3:L3`, `import!A4:L4`, etc.

## 5. Testing

### Test with cURL

```bash
curl -X POST https://eocrrf0lm1scxwv.m.pipedream.net \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "phone": "+1-555-123-4567",
    "website": "https://example.com",
    "problem": "GTM container not loading",
    "details": "GTM debug mode shows no container, Google Ads conversion tracking broken",
    "service_type": "emergency_fix",
    "source_domain": "gtmsetupservice.com",
    "utm_source": "test",
    "utm_medium": "webhook_test",
    "utm_campaign": "form_integration",
    "form_submitted": "2025-10-20T09:30:00.000Z"
  }'
```

### Expected Response
- **Status Code:** 200 OK
- **Response Body:** "OK"

### Verification Checklist
- [ ] Pipedream shows successful execution (no errors)
- [ ] New row appears in Google Sheets (import!A3:L3 or next available row)
- [ ] Slack DM notification received
- [ ] All 12 fields populated correctly

## 6. Integration Points

### Website Form Handler
Location: `/assets/js/form-handler.js`

The form should POST to the webhook endpoint with the payload structure above.

**Example Integration:**
```javascript
const formData = {
  email: form.querySelector('[name="email"]').value,
  name: form.querySelector('[name="name"]').value,
  phone: form.querySelector('[name="phone"]').value,
  website: form.querySelector('[name="website"]').value,
  problem: form.querySelector('[name="problem"]').value,
  details: form.querySelector('[name="details"]').value,
  service_type: form.querySelector('[name="service_type"]').value,
  source_domain: window.location.hostname,
  utm_source: new URLSearchParams(window.location.search).get('utm_source') || '',
  utm_medium: new URLSearchParams(window.location.search).get('utm_medium') || '',
  utm_campaign: new URLSearchParams(window.location.search).get('utm_campaign') || '',
  form_submitted: new Date().toISOString()
};

const response = await fetch('https://eocrrf0lm1scxwv.m.pipedream.net', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(formData)
});
```

## 7. Monitoring & Alerts

### Pipedream Event History
- **Location:** https://pipedream.com (requires login)
- **Retention:** Free tier retains limited event history
- **Upgrade:** Extended event history available with paid plans

### Slack Notifications
- **Account:** vscodr.brad@gmail.com
- **Channel:** Direct Message (DM)
- **Format:** Formatted message with emoji indicators

### Google Sheets Access
- **URL:** https://docs.google.com/spreadsheets/d/1wB3KU8Dsx8mSIfJlEyfszruo_tFbaykk8j7HjeiYB-A
- **Access:** Direct via Google account
- **Export:** Download as CSV, Excel, or other formats

## 8. Data Privacy & Security

### Data Storage
- All form data stored in Google Sheets
- No data stored in Pipedream beyond event history retention
- Slack notifications contain PII (handle accordingly)

### Security Considerations
- Webhook endpoint is public (no authentication)
- Consider adding rate limiting for production
- Monitor for spam submissions
- GDPR compliance: Document data retention policies
- Consider adding honeypot fields for spam prevention

### Recommended Enhancements
1. **Rate Limiting:** Implement per-IP rate limiting
2. **Spam Protection:** Add reCAPTCHA or hCaptcha
3. **Data Validation:** Server-side validation in Pipedream
4. **Webhook Authentication:** Add shared secret verification
5. **Error Handling:** Configure fallback notifications if Google Sheets fails

## 9. Troubleshooting

### Common Issues

**Issue: Slack notification fails with "invalid_arguments"**
- **Cause:** User/channel not selected in Pipedream Slack step
- **Solution:** Select specific user or channel from dropdown in Pipedream workflow

**Issue: Google Sheets not updating**
- **Cause:** Spreadsheet ID or sheet name incorrect
- **Solution:** Verify spreadsheet ID and sheet name in Pipedream step configuration

**Issue: Missing fields in spreadsheet**
- **Cause:** Column mapping mismatch
- **Solution:** Verify all 12 columns mapped correctly in Pipedream Google Sheets step

**Issue: Webhook returns error**
- **Cause:** Invalid JSON payload
- **Solution:** Validate JSON structure matches expected payload format

### Debug Steps
1. Check Pipedream event history for error details
2. Verify Google Sheets permissions (Pipedream must have write access)
3. Test with minimal payload first, then add fields
4. Check Slack workspace permissions

## 10. Changelog

| Date | Change | Author |
|------|--------|--------|
| 2025-10-20 | Initial form integration setup | Claude Code |
| 2025-10-20 | Fixed Slack DM configuration | Claude Code |
| 2025-10-20 | Documented complete workflow | Claude Code |

## 11. Related Documentation

- [14-Day Launch Action Plan](./14-day-launch-action-plan.md) - Day 2 form setup
- [GTM Setup Service Repo Structure](./gtmsetupservice-repo-structure.md) - Site structure
- Site assets: `/sites/gtmsetupservice.com/assets/js/form-handler.js`

## 12. Next Steps

- [ ] Update `/assets/js/form-handler.js` with webhook endpoint
- [ ] Add form validation (client-side and server-side)
- [ ] Implement spam protection (reCAPTCHA)
- [ ] Set up automated response email (via Pipedream or Google Apps Script)
- [ ] Create dashboard for form analytics
- [ ] Configure data retention policy
- [ ] Set up backup/export automation for Google Sheets data
