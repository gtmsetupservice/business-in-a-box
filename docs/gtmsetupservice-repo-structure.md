# GTMSetupService.com Repository Structure

**Repository:** https://github.com/gtmsetupservice/business-in-a-box
**Live Site:** https://gtmsetupservice.com
**Platform:** Jekyll + GitHub Pages
**GitHub Account:** gtmsetupservice

---

## Repository Information

**Git Remote:**
```
origin: https://github.com/gtmsetupservice/business-in-a-box.git
Authentication: Token-based (via environment variable)
```

**Recent Commits:**
```
21d8aa0 Add 4-layer GTM diagnostic blog posts
2241d87 Fix domain to singular gtmsetupservice.com
e46e0e1 Fix GTMSetupServices.com malformed feed URLs
f35fe32 Fix GTMSetupServices.com SEO indexing issues
b15b069 Fix LocallyKnown.pro SEO and sync all sites from GitHub
```

---

## Directory Structure

```
gtmsetupservice.com/
├── _config.yml              # Jekyll site configuration
├── _headers                 # Custom HTTP headers for hosting
├── CNAME                    # Custom domain configuration (gtmsetupservice.com)
├── Gemfile                  # Ruby dependencies
├── Gemfile.lock            # Locked dependency versions
│
├── _includes/              # Reusable HTML components
│   ├── benefits.html
│   ├── contact-form.html
│   ├── hero.html
│   ├── problem-agitation.html
│   ├── quick-wins.html
│   └── solution-intro.html
│
├── _layouts/               # Page templates
│   ├── default.html        # Base layout with header/footer
│   └── post.html           # Blog post layout
│
├── _posts/                 # Blog posts (Markdown)
│   ├── 2025-01-17-ga4-debugview-shows-data-reports-empty-processing-diagnostic.md
│   ├── 2025-01-17-ga4-events-not-reaching-google-transmission-diagnostic.md
│   ├── 2025-01-17-gtm-container-wont-load-infrastructure-diagnostic.md
│   └── 2025-01-17-gtm-tags-wont-fire-implementation-diagnostic.md
│
├── assets/                 # Static assets
│   ├── css/               # Stylesheets (empty - using Tailwind CDN)
│   └── js/
│       └── form-handler.js # Contact form JavaScript
│
├── audiences/              # Audience data (for prospecting)
│   └── wordpress-frustrated-business-owners.json
│
├── blog/
│   └── index.html         # Blog listing page
│
├── about.md               # About page content
├── index.md               # Homepage content
├── privacy.md             # Privacy policy
│
├── llm.txt                # LLM-readable site summary
├── robots.txt             # Search engine directives
└── sitemap.xml            # XML sitemap for SEO
```

---

## Site Configuration (_config.yml)

```yaml
# Core Settings
title: GTM Setup Services
description: Emergency GTM recovery and comprehensive tracking audits. Fix broken Google Tag Manager in 2-4 hours.
url: https://gtmsetupservice.com
baseurl: ""

# SEO
tagline: Fix Your GTM Tracking Issues Today
author:
  name: GTM Setup Services
  email: support@gtmsetupservice.com

# Jekyll Configuration
markdown: kramdown
permalink: /blog/:title/

# Plugins
plugins:
  - jekyll-seo-tag
  - jekyll-sitemap

# Analytics (not yet configured)
google_analytics: # GA4 Measurement ID
gtm_container: # GTM Container ID

# Service Pricing
service_type: gtm
emergency_price: "$497"
audit_price: "$797"
monitoring_price: "$197/month"
```

---

## Content Structure

### Blog Posts (4 currently)

**Format:** `YYYY-MM-DD-slug.md` in `_posts/` directory

**Current Posts:**
1. GTM Container Won't Load - Infrastructure Diagnostic (Layer 1)
2. GTM Tags Won't Fire - Implementation Diagnostic (Layer 2)
3. GA4 Events Not Reaching Google - Transmission Diagnostic (Layer 3)
4. GA4 DebugView Shows Data, Reports Empty - Processing Diagnostic (Layer 4)

**Post Structure:**
```yaml
---
layout: post
title: "Post Title"
date: 2025-01-17 09:00:00 +0800
description: "SEO description"
categories: [diagnostics, troubleshooting]
tags: [GTM, Layer-X, Keywords]
author: GTM Setup Service
---

[Markdown content]
```

### Pages

**Homepage (index.md):**
- Uses modular includes for sections
- Hero section
- Quick wins
- Problem-agitation
- Solution intro
- Benefits
- Testimonials (placeholder)
- 3-step process
- Pricing/services
- Contact form

**About (about.md):**
- Company information
- Services overview
- B and B Holdings LLC details

**Privacy (privacy.md):**
- Privacy policy

**Blog Index (blog/index.html):**
- Lists all blog posts

---

## Component Includes

### hero.html
- Above-the-fold section
- Main headline: "Stop Losing Money to GTM Tracking Failures"
- CTA: "Get Emergency GTM Fix - $497"
- Social proof: "247+ GTM emergencies resolved"

### problem-agitation.html
- Lists common GTM problems
- Builds urgency
- Pain point enumeration

### quick-wins.html
- Benefits highlight section

### solution-intro.html
- Service introduction

### benefits.html
- Detailed benefits breakdown

### contact-form.html
- Lead capture form
- Problem qualification dropdown
- Hidden fields for UTM tracking
- Formspree integration ready (needs endpoint)

---

## Deployment Workflow

**Build Process:**
1. Jekyll builds static site from markdown/layouts
2. Generated files go to `_site/` directory
3. GitHub Pages serves from `_site/`
4. Custom domain via CNAME file

**Deployment Steps:**
```bash
# Make changes to markdown/includes
git add .
git commit -m "Description of changes"
git push origin main

# GitHub Pages automatically rebuilds
# Check status: https://github.com/gtmsetupservice/business-in-a-box/actions
```

**GitHub Pages Settings:**
- Source: Deploy from branch
- Branch: main / root
- Custom domain: gtmsetupservice.com
- HTTPS: Enforced

**DNS Configuration:**
```
Type: CNAME
Host: www
Value: gtmsetupservice.github.io

Type: A (4 records)
Host: @
Values:
  185.199.108.153
  185.199.109.153
  185.199.110.153
  185.199.111.153
```

---

## Key Features

### Current State
- ✅ Jekyll static site generator
- ✅ Tailwind CSS (CDN)
- ✅ GitHub Pages hosting ($0/month)
- ✅ Custom domain configured
- ✅ HTTPS enabled
- ✅ 4 blog posts (4-layer diagnostic framework)
- ✅ Homepage with full conversion funnel
- ✅ Contact form structure ready
- ✅ SEO plugins (jekyll-seo-tag, sitemap)
- ✅ XML sitemap auto-generated
- ✅ Blog listing page
- ✅ GA4 tracking configured (G-QD2PEKQ375)
- ✅ GTM container implemented (GTM-M3CR8QZP)

### Needs Configuration
- ⚠️ Contact form backend (Formspree endpoint)
- ⚠️ Real testimonials (currently placeholder)
- ⚠️ Case study images/graphics
- ⚠️ Lead magnet (diagnostic snippets PDF)

### Missing Content
- ❌ 6+ more blog posts (target: 10+ total)
- ❌ Service-specific landing pages
- ❌ Monitoring service page (/monitoring.md)
- ❌ Emergency landing page variant
- ❌ Resources/downloads section

---

## Development Workflow

### Local Development
```bash
cd /Volumes/Samsung/mo/prod/projects/business-in-a-box/sites/gtmsetupservice.com

# Install dependencies (first time)
bundle install

# Run local server
bundle exec jekyll serve

# Visit: http://localhost:4000
```

### Creating New Blog Post
```bash
cd _posts/

# Create new file: YYYY-MM-DD-slug.md
touch 2025-01-18-new-post-title.md

# Add front matter and content
# Test locally
# Commit and push to deploy
```

### Adding New Page
```bash
# Create markdown file in root
touch new-page.md

# Add front matter:
---
layout: default
title: "Page Title"
description: "SEO description"
---

# Commit and push
```

---

## Integration Points

### Contact Form → CRM
**Current:** Form structure exists, not connected
**Needs:**
- Formspree endpoint configured in `assets/js/form-handler.js`
- OR: Custom backend integration
- OR: Direct to email (simplest)

**Form Data Captured:**
- Name
- Email
- Website URL
- Problem type (dropdown)
- Additional details
- Service type (hidden: "gtm")
- UTM parameters (hidden)

### Analytics Stack (CONFIGURED - Dogfooding Own Service)
**Live Tracking Implementation:**
- GA4 Measurement ID: `G-QD2PEKQ375`
- GTM Container ID: `GTM-M3CR8QZP`

**Currently Tracking:**
1. Page views
2. Blog post engagement
3. Form submissions
4. CTA clicks
5. Service tier interest

**Implementation Notes:**
- Properly dogfooding own GTM setup service
- Can be used as live case study: "How We Track Our Own Site"
- Real-world testing of 4-layer diagnostic framework

### CRM Integration
**Variables in _config.yml:**
```yaml
crm_endpoint: # Your FluentCRM API endpoint
crm_api_key: # Your FluentCRM API key
```

**Not yet configured** - awaits CRM decision

---

## Content Strategy

### 4-Layer Diagnostic Framework
All blog posts follow this structure:

**Layer 1: Infrastructure**
- GTM container loading
- Script delivery
- Network issues

**Layer 2: Implementation**
- Tag configuration
- Trigger setup
- Variable mapping

**Layer 3: Transmission**
- Data delivery
- Ad blockers
- Network transmission

**Layer 4: Processing**
- GA4 processing
- Reporting issues
- Data thresholding

### SEO Strategy
**Primary Keywords (from business-plan.md):**
- Google Tag Manager setup (260/month)
- GTM setup (50/month)
- GTM implementation (70/month)
- Google Ads conversion tracking (high value)

**Current Blog Posts Target:**
- Layer 1: Infrastructure keywords
- Layer 2: Implementation keywords
- Layer 3: Transmission keywords
- Layer 4: Processing keywords

---

## Service Tiers

**Emergency Recovery: $497**
- 2-4 hour response
- Critical tracking fixes
- Root cause analysis
- Prevention measures
- Full documentation

**Comprehensive Audit: $797**
- 4-layer diagnostic audit
- Performance optimization
- Security review
- Detailed findings report
- Implementation roadmap

**Monthly Monitoring: $197/month**
- Proactive monitoring
- Break detection alerts
- Monthly health reports
- Priority support
- Optimization recommendations

---

## Performance Characteristics

### Jekyll Static Site Advantages
- ✅ Sub-1-second load times
- ✅ No database queries
- ✅ No server-side processing
- ✅ CDN-friendly (GitHub Pages CDN)
- ✅ Extremely secure (no dynamic code)
- ✅ $0 hosting costs
- ✅ Automatic HTTPS
- ✅ Git-based version control

### Build Times
- Average: 2-3 seconds locally
- GitHub Pages: 30-60 seconds
- Incremental builds supported

---

## Next Actions (Per 14-Day Plan)

**Week 1:**
1. Generate 5+ blog posts using AI
2. Configure Formspree for contact form
3. Push updates to GitHub
4. Set up GA4 + GTM (dogfood service)
5. Submit to Google Search Console
6. LinkedIn launch announcement

**Week 2:**
7. Create 3+ additional blog posts
8. Build monitoring service page
9. A/B test service positioning
10. Content multiplication (LinkedIn, Twitter)
11. Reach out for real testimonials
12. Create lead magnet (diagnostic snippets PDF)

---

## Repository Maintenance

### Regular Updates
- Blog posts: 2-4 per week (initial phase)
- Case studies: As clients are completed
- Testimonials: Ongoing collection
- Service pages: As offerings expand

### Monitoring
- GitHub Actions: Check build status
- Google Search Console: SEO performance
- Analytics: Traffic and conversions
- Form submissions: Daily check

### Backup Strategy
- Git version control (primary backup)
- GitHub repository (cloud backup)
- Local development copy
- Generated site in `_site/` can be statically hosted anywhere

---

## Technical Stack Summary

**Frontend:**
- HTML5
- Tailwind CSS (via CDN)
- Vanilla JavaScript (form handling)

**Backend:**
- Jekyll static site generator
- Ruby + Bundler
- Markdown content

**Hosting:**
- GitHub Pages
- Custom domain via CNAME
- Automatic HTTPS

**Build:**
- Jekyll 4.3.4
- kramdown markdown processor
- jekyll-seo-tag plugin
- jekyll-sitemap plugin

**Version Control:**
- Git
- GitHub repository
- Token-based authentication

---

**Last Updated:** 2025-01-18
**Status:** Functional, ready for content expansion and traffic generation
