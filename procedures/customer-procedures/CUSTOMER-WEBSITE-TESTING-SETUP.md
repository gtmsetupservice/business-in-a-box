# Customer Website Testing Setup - Complete Access & Permissions Guide

## Overview
This document outlines the complete process for gaining necessary access and permissions to test GTM implementations on customer websites. Every detail is included to ensure comprehensive access without security risks.

## Pre-Project Access Requirements Checklist

### 1. Google Tag Manager Access
**Required Permission Level:** PUBLISH access (not just View or Edit)

#### Client Must Provide:
- [ ] GTM Container ID (GTM-XXXXXXX format)
- [ ] Add your Google account to GTM with PUBLISH permissions
- [ ] Confirm you can see all existing tags, triggers, and variables
- [ ] Verify you can create new workspaces

#### Your Actions:
- [ ] Accept GTM container invitation email
- [ ] Log into GTM and verify access level
- [ ] Create dedicated workspace for testing (name: "GTMSetupService-Testing-[Date]")
- [ ] Document existing container structure before making changes

### 2. Google Analytics Access
**Required Permission Level:** EDIT access minimum, MANAGE preferred

#### Client Must Provide:
- [ ] GA4 Property ID (G-XXXXXXXXXX format)
- [ ] Add your Google account to GA4 property
- [ ] Confirm access to DebugView
- [ ] Verify you can see existing events and conversions

#### Your Actions:
- [ ] Accept GA4 invitation
- [ ] Test DebugView functionality
- [ ] Document existing event configuration
- [ ] Verify Enhanced Measurement settings

### 3. Google Ads Access (if applicable)
**Required Permission Level:** STANDARD access for conversion tracking

#### Client Must Provide:
- [ ] Google Ads Account ID
- [ ] Add your Google account with conversion tracking permissions
- [ ] Existing conversion actions list

#### Your Actions:
- [ ] Accept Google Ads invitation
- [ ] Review existing conversion tracking setup
- [ ] Document current conversion actions

### 4. Website/CMS Access

#### WordPress Sites:
**Required Permission Level:** Administrator access

#### Client Must Provide:
- [ ] WordPress admin username and password
- [ ] Site URL and admin URL (/wp-admin)
- [ ] FTP/SFTP credentials (if theme/plugin customization needed)
- [ ] Staging site URL (if available)
- [ ] Backup confirmation (client responsibility)

#### Shopify Sites:
**Required Permission Level:** Full access or Apps and channels permissions

#### Client Must Provide:
- [ ] Shopify store URL
- [ ] Staff account with appropriate permissions
- [ ] Access to theme code editing
- [ ] App installation permissions

#### Other Platforms:
- [ ] Platform-specific admin access
- [ ] Code injection permissions
- [ ] Theme/template editing access

### 5. Domain/DNS Access (if needed)
**Only required for server-side GTM or custom subdomains**

#### Client Must Provide:
- [ ] DNS management access (Cloudflare, etc.)
- [ ] Domain registrar access
- [ ] SSL certificate management access

## Testing Environment Setup

### 1. Create Testing Workspace
```
GTM Workspace Name: "GTMSetupService-Testing-[MMDDYY]"
Description: "Testing environment for GTMSetupService implementation - DO NOT PUBLISH without approval"
```

### 2. Document Baseline State
Before making ANY changes:

- [ ] Screenshot GTM container overview
- [ ] Export GTM container as backup
- [ ] Document all existing tags (names, types, triggers)
- [ ] Screenshot GA4 current events
- [ ] Test existing tracking with GTM Preview mode
- [ ] Document any broken/non-firing tags

### 3. Testing Browser Setup
#### Required Browser Extensions:
- [ ] Google Tag Assistant Legacy
- [ ] Google Tag Assistant (new version)
- [ ] Meta Pixel Helper
- [ ] BuiltWith Technology Profiler

#### Browser Configuration:
- [ ] Disable ad blockers during testing
- [ ] Enable JavaScript console logging
- [ ] Clear cookies before each test session
- [ ] Test in incognito/private mode

## Step-by-Step Testing Protocol

### Phase 1: Access Verification (Day 1)
1. **GTM Access Test**
   - [ ] Log into GTM container
   - [ ] Create test workspace
   - [ ] Verify you can create tags/triggers
   - [ ] Test preview mode functionality

2. **GA4 Access Test**
   - [ ] Access GA4 property
   - [ ] Open DebugView
   - [ ] Verify real-time reporting access
   - [ ] Test event filtering capabilities

3. **Website Access Test**
   - [ ] Log into website admin
   - [ ] Verify you can edit themes/templates
   - [ ] Test plugin installation permissions
   - [ ] Confirm backup access/restoration

### Phase 2: Baseline Testing (Day 1-2)
1. **Current State Analysis**
   - [ ] GTM Preview mode on live site
   - [ ] Document which tags fire correctly
   - [ ] Identify broken/missing tracking
   - [ ] Test all existing conversion events

2. **Cross-Platform Verification**
   - [ ] Check GTM events in GA4 DebugView
   - [ ] Verify Google Ads conversion tracking
   - [ ] Test Meta Pixel events (if applicable)
   - [ ] Compare data across platforms

### Phase 3: Implementation Testing (Day 2-5)
1. **Workspace Testing**
   - [ ] Implement changes in testing workspace
   - [ ] Use GTM Preview mode extensively
   - [ ] Test on staging site first (if available)
   - [ ] Document all changes made

2. **Multi-Device Testing**
   - [ ] Desktop testing (Chrome, Firefox, Safari)
   - [ ] Mobile testing (iOS Safari, Android Chrome)
   - [ ] Tablet testing
   - [ ] Different connection speeds

3. **User Journey Testing**
   - [ ] Complete purchase flows
   - [ ] Form submission testing
   - [ ] Newsletter signup testing
   - [ ] Download/CTA button testing

### Phase 4: Validation & Sign-off (Day 5-6)
1. **Client Review Session**
   - [ ] Screen share GTM Preview mode
   - [ ] Show before/after DebugView comparison
   - [ ] Demonstrate improved tracking
   - [ ] Get explicit approval to publish

2. **Final Documentation**
   - [ ] Before/after comparison report
   - [ ] New events documentation
   - [ ] Testing screenshots/videos
   - [ ] Maintenance recommendations

## Security & Best Practices

### Data Protection
- [ ] Only access data necessary for testing
- [ ] Do not download customer data unnecessarily
- [ ] Use secure connections only
- [ ] Document all access timestamps

### Version Control
- [ ] Always work in dedicated workspace
- [ ] Export container versions before changes
- [ ] Create restore points before major changes
- [ ] Never edit production directly

### Communication Protocol
- [ ] Daily progress updates during testing
- [ ] Immediate notification of any issues
- [ ] Screenshot evidence for all changes
- [ ] Written approval before publishing

## Emergency Procedures

### If Something Breaks
1. **Immediate Actions:**
   - [ ] Do NOT publish workspace changes
   - [ ] Switch to previous GTM version if published
   - [ ] Document exactly what was changed
   - [ ] Notify client immediately

2. **Recovery Steps:**
   - [ ] Restore from GTM backup
   - [ ] Clear GTM cache if needed
   - [ ] Test restoration thoroughly
   - [ ] Document lessons learned

### If Access is Lost
1. **GTM Access Issues:**
   - [ ] Contact client for re-invitation
   - [ ] Verify correct Google account being used
   - [ ] Check spam folder for invitations
   - [ ] Document access loss timestamp

## Client Communication Templates

### Initial Access Request Email
```
Subject: GTM Implementation - Access Requirements

Hi [Client Name],

To begin your GTM implementation, I'll need the following access:

GOOGLE TAG MANAGER:
- Please add [your-email] to GTM Container [GTM-XXXXXXX] with PUBLISH permissions
- Instructions: [GTM sharing instructions link]

GOOGLE ANALYTICS:
- Please add [your-email] to GA4 Property [G-XXXXXXXXXX] with EDIT permissions  
- Instructions: [GA4 sharing instructions link]

WEBSITE ACCESS:
- WordPress admin credentials for [site-url]
- Or please create admin account: username "gtmsetupservice"

I'll confirm all access within 24 hours and begin baseline testing immediately.

Best regards,
[Your name]
```

### Testing Complete Email
```
Subject: GTM Testing Complete - Ready for Review

Hi [Client Name],

GTM testing is complete and ready for your review:

IMPROVEMENTS MADE:
- [List specific improvements]
- [Include before/after metrics]

NEXT STEPS:
- Schedule 30-minute review call
- I'll demonstrate all changes using screen share
- Upon your approval, I'll publish changes to live site

ATTACHED:
- Testing report with screenshots
- New events documentation

Available for review call: [Your availability]

Best regards,
[Your name]
```

## Post-Implementation Checklist

### After Publishing Changes
- [ ] Test live site immediately after publishing
- [ ] Monitor GA4 DebugView for 24 hours
- [ ] Check for any error reports
- [ ] Document final configuration
- [ ] Remove testing workspace
- [ ] Revoke unnecessary access (if requested)

### Client Handoff
- [ ] Provide complete documentation
- [ ] Schedule training session (if included)
- [ ] Set up monitoring alerts
- [ ] Establish ongoing support protocol

---

## Important Notes

### Legal Considerations
- Always have signed service agreement before requesting access
- Maintain confidentiality of all client data
- Follow GDPR/privacy requirements for data access
- Document access for compliance purposes

### Technical Limitations
- Some platforms limit simultaneous admin sessions
- Browser extensions may interfere with testing
- Ad blockers affect GTM functionality
- Different CMS versions may have different access methods

### Success Metrics
- 100% of planned tracking events working
- Cross-platform data consistency
- No performance degradation
- Client satisfaction with demonstration

---

**Remember: Never make changes to live production without explicit client approval and comprehensive testing in preview mode.**