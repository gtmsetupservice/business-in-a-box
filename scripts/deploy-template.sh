#!/bin/bash

# Business-in-a-Box Template Deployment Script
# Usage: ./deploy-template.sh [client-project-directory]

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Check arguments
if [ $# -lt 1 ]; then
    print_error "Usage: $0 [client-project-directory]"
    echo "Example: $0 /Volumes/Samsung/mo/prod/projects/clients/smiths-plumbing"
    exit 1
fi

CLIENT_DIR="$1"

# Validate client directory exists
if [ ! -d "$CLIENT_DIR" ]; then
    print_error "Client directory does not exist: $CLIENT_DIR"
    exit 1
fi

# Check for client configuration
if [ ! -f "$CLIENT_DIR/client-config.json" ]; then
    print_error "Client configuration not found: $CLIENT_DIR/client-config.json"
    exit 1
fi

print_header "Business-in-a-Box Template Deployment"
print_status "Client directory: $CLIENT_DIR"

cd "$CLIENT_DIR"

# Load client configuration
CLIENT_NAME=$(python3 -c "import json; config=json.load(open('client-config.json')); print(config['client']['name'])")
CLIENT_NICHE=$(python3 -c "import json; config=json.load(open('client-config.json')); print(config['client']['niche'])")
BUSINESS_TYPE=$(python3 -c "import json; config=json.load(open('client-config.json')); print(config['business_type'])")

print_status "Client: $CLIENT_NAME"
print_status "Niche: $CLIENT_NICHE"
print_status "Business Type: $BUSINESS_TYPE"

# Run niche analysis if DataForSEO tools available
if [ -d "scripts" ] && [ -f "scripts/comprehensive_niche_report.py" ]; then
    print_status "Running niche analysis for $CLIENT_NICHE..."

    # Create reports directory
    mkdir -p reports

    # Run competitor analysis
    print_status "Executing competitor research..."
    cd scripts

    # Check for API credentials
    if [ -z "$DATA_FOR_SEO_USER" ] || [ -z "$DATA_FOR_SEO_PASSWORD" ]; then
        print_warning "DataForSEO credentials not found in environment variables"
        print_warning "Set DATA_FOR_SEO_USER and DATA_FOR_SEO_PASSWORD or create .env file"
        print_warning "Skipping niche analysis"
    else
        # Run with basic niche keywords
        python3 comprehensive_niche_report.py \
            --keywords "$CLIENT_NICHE services" "$CLIENT_NICHE $CLIENT_LOCATION" "$CLIENT_NICHE near me" \
            --niche-name "$CLIENT_NICHE" \
            --login "$DATA_FOR_SEO_USER" \
            --password "$DATA_FOR_SEO_PASSWORD" \
            --output-dir "../reports" || {
            print_warning "Niche analysis failed, continuing without competitor data"
        }
    fi

    cd ..
else
    print_warning "DataForSEO scripts not available, skipping niche analysis"
fi

# Business-specific deployment tasks
if [ "$BUSINESS_TYPE" = "locallyknown-pro" ]; then
    print_header "LocallyKnown.pro Deployment Tasks"

    # Jekyll site preparation
    if [ -f "_config.yml" ]; then
        print_status "Preparing Jekyll site for deployment..."

        # Install dependencies if Gemfile exists
        if [ -f "Gemfile" ]; then
            print_status "Installing Jekyll dependencies..."
            bundle install --quiet || print_warning "Bundle install failed"
        fi

        # Generate initial content templates
        print_status "Creating content templates..."
        mkdir -p _posts _drafts

        # Create initial blog post template
        cat > "_drafts/welcome-to-$CLIENT_NICHE.md" << EOF
---
layout: post
title: "Welcome to $CLIENT_NAME"
date: $(date +%Y-%m-%d)
categories: [$CLIENT_NICHE]
---

# Welcome to $CLIENT_NAME

Your trusted $CLIENT_NICHE service provider in $CLIENT_LOCATION.

## Our Services

[Content to be customized by content writer agent]

## Why Choose Us

[Competitive advantages to be identified by competitor research agent]

## Contact Us Today

Ready to get started? Contact $CLIENT_NAME today for professional $CLIENT_NICHE services.
EOF

        print_status "Jekyll site prepared for content creation"
    fi

elif [ "$BUSINESS_TYPE" = "gtm-setups" ]; then
    print_header "GTM Setups Deployment Tasks"

    # Prepare diagnostic tools
    print_status "Setting up GTM diagnostic environment..."

    # Create assessment templates
    mkdir -p assessments templates

    # Create GTM assessment template
    cat > "assessments/initial-assessment.md" << EOF
# GTM Assessment for $CLIENT_NAME

**Date:** $(date)
**Client:** $CLIENT_NAME
**Industry:** $CLIENT_NICHE

## Current State Analysis

### Layer 1: Infrastructure
- [ ] GTM container loading verified
- [ ] Script delivery confirmed
- [ ] Network connectivity tested
- [ ] Browser compatibility checked

### Layer 2: Implementation
- [ ] Tags configuration reviewed
- [ ] Triggers validation completed
- [ ] Variables assessment done
- [ ] Data layer structure analyzed

### Layer 3: Transmission
- [ ] Request monitoring completed
- [ ] Payload verification done
- [ ] Server-side setup checked
- [ ] Data transmission validated

### Layer 4: Processing
- [ ] GA4 configuration reviewed
- [ ] Reporting accuracy verified
- [ ] Custom dimensions checked
- [ ] Conversion tracking validated

## Findings Summary

[To be completed by GTM diagnostics agent]

## Recommended Actions

[To be completed by GTM support agent]

## Implementation Plan

[To be completed by PM agent]
EOF

    print_status "GTM assessment template created"
fi

# Generate deployment report
print_status "Generating deployment report..."
cat > "DEPLOYMENT-REPORT.md" << EOF
# Deployment Report: $CLIENT_NAME

**Date:** $(date)
**Business Type:** $BUSINESS_TYPE
**Client Niche:** $CLIENT_NICHE

## Deployment Summary

✅ Template successfully deployed
✅ Client configuration applied
✅ CRM database initialized
✅ Project structure created

## Next Steps

### Immediate Actions Required:
EOF

if [ "$BUSINESS_TYPE" = "locallyknown-pro" ]; then
    cat >> "DEPLOYMENT-REPORT.md" << EOF
1. **Load competitor research agent:** \`load competitor research\`
2. **Review niche analysis results** in reports/ directory
3. **Load content writer agent:** \`load content writer\`
4. **Begin content creation** for homepage and about page

### Service Delivery Timeline:
- **Days 1-2:** Research & Strategy
- **Days 3-4:** Content Creation
- **Days 5-6:** Jekyll Development
- **Day 7:** Delivery & Handoff

### Expected Deliverables:
- 3-page Jekyll website
- First 2 pages of content + blog setup
- SEO competitor research report
- Analytics tracking implementation
EOF
elif [ "$BUSINESS_TYPE" = "gtm-setups" ]; then
    cat >> "DEPLOYMENT-REPORT.md" << EOF
1. **Load GTM prospect agent:** \`load gtm prospect\`
2. **Complete initial assessment** using assessments/initial-assessment.md
3. **Load GTM diagnostics agent:** \`load gtm diagnostics\`
4. **Execute 4-layer diagnostic process**

### Service Delivery Options:
- **Emergency ($497):** 24-hour resolution
- **Complete Audit ($797):** 48-72 hour full analysis
- **Server-Side Setup ($1,297):** 1-week implementation

### Diagnostic Framework:
- Layer 1: Infrastructure verification
- Layer 2: Implementation analysis
- Layer 3: Transmission validation
- Layer 4: Processing confirmation
EOF
fi

cat >> "DEPLOYMENT-REPORT.md" << EOF

## Project Directory Structure:
\`\`\`
$(find . -type d -name ".*" -prune -o -type d -print | head -20)
\`\`\`

## Configuration Files:
- client-config.json
- CLAUDE.md (customized)
$(if [ "$BUSINESS_TYPE" = "locallyknown-pro" ]; then echo "- _config.yml (Jekyll)"; fi)
$(if [ "$BUSINESS_TYPE" = "gtm-setups" ]; then echo "- emergency-config.json"; fi)

---
*Deployment completed successfully! Ready for agent activation.*
EOF

print_header "Deployment Complete"
print_status "Template deployment successful!"
print_status "Review DEPLOYMENT-REPORT.md for next steps"
print_status "Client project ready for service delivery"

# Log deployment completion
echo "$(date): Template deployment completed successfully" >> logs/project-init.log

print_status "Ready to begin $BUSINESS_TYPE service delivery! 🚀"