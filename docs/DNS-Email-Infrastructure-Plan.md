# DNS & Email Infrastructure Audit & Cleanup Plan

**Date:** 2025-09-29
**Objective:** Document current DNS configuration and plan DMARC improvements across all domains

---

## Domain Analysis Summary

### **✅ PROPERLY CONFIGURED DOMAINS**
- **gtmsetupservice.com** - Ready for production use
- **ifixwpquick.com** - Ready for production use
- **locallyknown.pro** - Ready for production use (missing DMARC only)

### **❌ NEEDS MIGRATION**
- **metacranium.com** - Still using Namecheap email forwarding

---

## **1. gtmsetupservice.com** - PRODUCTION READY

### Current Configuration:
```
Main Domain: 185.199.108.153 (GitHub Pages)
MX Record: mail.gtmsetupservice.com (206.168.149.50)
DKIM: ✅ Configured with valid key
SPF: ✅ v=spf1 +a +mx +ip4:206.168.149.50 include:relay.mailbaby.net ~all
DMARC: ⚠️ v=DMARC1; p=none; (monitoring only)
```

### Required Changes:
- **Update DMARC record:**
  ```
  _dmarc.gtmsetupservice.com     TXT
  v=DMARC1; p=reject; rua=mailto:dmarc@gtmsetupservice.com; ruf=mailto:dmarc@gtmsetupservice.com; fo=1; adkim=s; aspf=s
  ```
- **Create email:** `dmarc@gtmsetupservice.com` in RackNerd cPanel

---

## **2. locallyknown.pro** - PRODUCTION READY

### Current Configuration:
```
Main Domain: 206.168.149.50 (RackNerd hosting)
MX Record: locallyknown.pro (self-referential)
DKIM: ✅ Configured with valid key
SPF: ✅ v=spf1 ip4:206.168.149.50 include:relay.mailbaby.net ip4:148.135.49.178 +a +mx +ip4:66.152.180.82 ~all
DMARC: ❌ MISSING
```

### Required Changes:
- **Add DMARC record:**
  ```
  _dmarc.locallyknown.pro     TXT
  v=DMARC1; p=reject; rua=mailto:dmarc@locallyknown.pro; ruf=mailto:dmarc@locallyknown.pro; fo=1; adkim=s; aspf=s
  ```
- **Create email:** `dmarc@locallyknown.pro` in RackNerd cPanel

### Configuration Issues Found:
- **Mixed SRV targets:** Some calendar/contact services point to `acmealliedllc.com` instead of RackNerd
  - Should point to `locallyknown.pro` for consistency

---

## **3. ifixwpquick.com** - PRODUCTION READY

### Current Configuration:
```
Main Domain: 206.168.149.50 (RackNerd hosting - CORRECTED)
MX Record: ifixwpquick.com (self-referential, resolves to 206.168.149.50)
DKIM: ✅ Configured with valid key
SPF: ✅ v=spf1 +a +mx +ip4:206.168.149.50 include:relay.mailbaby.net ~all
DMARC: ⚠️ v=DMARC1; p=none; (monitoring only)
```

### Key Difference from Zone Export:
- **Live DNS:** Points to RackNerd (206.168.149.50)
- **Zone Export:** Showed GitHub Pages IPs (185.199.x.x)
- **This means the site is hosted on RackNerd, not GitHub Pages**

### Required Changes:
- **Update DMARC record:**
  ```
  _dmarc.ifixwpquick.com     TXT
  v=DMARC1; p=reject; rua=mailto:dmarc@ifixwpquick.com; ruf=mailto:dmarc@ifixwpquick.com; fo=1; adkim=s; aspf=s
  ```
- **Create email:** `dmarc@ifixwpquick.com` in RackNerd cPanel

---

## **4. metacranium.com** - NEEDS MIGRATION

### Current Configuration:
```
Main Domain: 192.64.119.133 (Cloudflare proxied)
MX Records: ❌ eforward*.registrar-servers.com (Namecheap)
DKIM: ❌ MISSING
SPF: ❌ v=spf1 include:spf.efwd.registrar-servers.com ~all (Namecheap only)
DMARC: ❌ MISSING
n8n Tunnel: ✅ Configured (2c0c054b-8574-4544-8835-5218e66cb2eb.cfargotunnel.com)
```

### Required Migration:
1. **Replace MX records:**
   ```
   Remove: eforward*.registrar-servers.com
   Add: mail.metacranium.com (206.168.149.50)
   ```
2. **Update SPF record:**
   ```
   v=spf1 +a +mx +ip4:206.168.149.50 include:relay.mailbaby.net ~all
   ```
3. **Add DKIM record** (from RackNerd cPanel)
4. **Add DMARC record:**
   ```
   _dmarc.metacranium.com     TXT
   v=DMARC1; p=reject; rua=mailto:dmarc@metacranium.com; ruf=mailto:dmarc@metacranium.com; fo=1; adkim=s; aspf=s
   ```

---

## Implementation Priority

### **Phase 1: DMARC Updates (Immediate)**
1. Create DMARC email addresses in RackNerd cPanel:
   - `dmarc@gtmsetupservice.com`
   - `dmarc@ifixwpquick.com`
   - `dmarc@locallyknown.pro`

2. Update/Add DMARC records in Cloudflare for all domains

### **Phase 2: Form System Implementation**
Since gtmsetupservice.com, ifixwpquick.com, and locallyknown.pro are email-ready:
- Deploy FastAPI form handler using existing n8n tunnel infrastructure
- Configure Telegram notifications
- Integrate with CRM database
- Test form submissions

### **Phase 3: metacranium.com Migration**
- Migrate from Namecheap to RackNerd email
- Full DNS cleanup and testing

---

## Email Architecture Schema

### **Proposed Email Structure:**
```
gtmsetupservice.com:
  - emergency@gtmsetupservice.com → main email (form submissions)
  - leads@gtmsetupservice.com → CRM integration
  - support@gtmsetupservice.com → client support
  - dmarc@gtmsetupservice.com → DMARC reports
  - noreply@gtmsetupservice.com → automated emails

ifixwpquick.com:
  - emergency@ifixwpquick.com → main email (form submissions)
  - support@ifixwpquick.com → client support
  - dmarc@ifixwpquick.com → DMARC reports
  - noreply@ifixwpquick.com → automated emails

locallyknown.pro:
  - contact@locallyknown.pro → main email
  - dmarc@locallyknown.pro → DMARC reports
  - noreply@locallyknown.pro → automated emails

metacranium.com:
  - admin@metacranium.com → main email
  - dmarc@metacranium.com → DMARC reports
  - noreply@metacranium.com → automated emails
```

---

## Security Configuration

### **DMARC Policy Explanation:**
- **`p=reject`** - Strict authentication policy
- **`rua=`** - Aggregate reports (weekly summaries)
- **`ruf=`** - Forensic reports (real-time failures)
- **`fo=1`** - Report any authentication failure
- **`adkim=s`** - Strict DKIM alignment
- **`aspf=s`** - Strict SPF alignment

### **Benefits:**
- Maximum email security against spoofing
- Protection of domain reputation
- Detailed reporting for monitoring
- Compliance with enterprise email requirements

---

## Form System Integration

### **Ready Domains for Form Implementation:**
1. **ifixwpquick.com** - WordPress emergency forms
2. **gtmsetupservice.com** - GTM service inquiries
3. **locallyknown.pro** - Digital marketing contacts

### **Infrastructure Available:**
- ✅ RackNerd SMTP servers configured
- ✅ Cloudflare Tunnel on metacranium.com for n8n
- ✅ DKIM authentication active
- ✅ SPF records include RackNerd servers
- 🔄 DMARC policies to be strengthened

### **Next Steps:**
1. Complete DMARC updates
2. Deploy FastAPI form handler
3. Configure Telegram notifications for instant alerts
4. Test full form-to-iPhone notification pipeline

---

**Status:** Ready for implementation
**Last Updated:** 2025-09-29