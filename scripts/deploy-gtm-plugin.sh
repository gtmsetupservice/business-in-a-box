#!/bin/bash

echo "🚀 GTM Head Injection Plugin Deployment Script"
echo "=============================================="

# Configuration
LOCAL_PLUGIN_PATH="/Volumes/Samsung/mo/local-sites/gtmsetupservicecom/app/public/wp-content/plugins/gtm-head-injection"
PROD_PLUGIN_PATH="/Volumes/Samsung/mo/prod/projects/gtmsetupservice.com/wp-content/plugins/gtm-head-injection"
GITHUB_REPO_PATH="/Volumes/Samsung/mo/prod/projects/gtmsetupservice.com"

echo "📋 Pre-deployment Checks"
echo "-------------------------"

# Check if local plugin exists
if [ ! -d "$LOCAL_PLUGIN_PATH" ]; then
    echo "❌ Local plugin directory not found: $LOCAL_PLUGIN_PATH"
    exit 1
fi

echo "✅ Local plugin found"

# Check PHP syntax
echo "🔍 Validating PHP syntax..."
if ! php -l "$LOCAL_PLUGIN_PATH/gtm-head-injection.php" > /dev/null 2>&1; then
    echo "❌ PHP syntax error in plugin file"
    exit 1
fi

echo "✅ PHP syntax valid"

echo ""
echo "📦 Deployment Phase 1: Copy to Production Directory"
echo "---------------------------------------------------"

# Create production plugin directory if it doesn't exist
mkdir -p "$PROD_PLUGIN_PATH"

# Copy plugin files
echo "📋 Copying plugin files..."
rsync -av "$LOCAL_PLUGIN_PATH/" "$PROD_PLUGIN_PATH/"

if [ $? -eq 0 ]; then
    echo "✅ Plugin files copied to production directory"
else
    echo "❌ Failed to copy plugin files"
    exit 1
fi

echo ""
echo "🔧 Deployment Phase 2: GitHub Repository Setup"
echo "----------------------------------------------"

cd "$GITHUB_REPO_PATH"

# Initialize git repository if not already done
if [ ! -d ".git" ]; then
    echo "🆕 Initializing git repository..."
    git init
    
    # Create .gitignore for WordPress project
    cat > .gitignore << 'EOF'
# WordPress core
/wp-admin/
/wp-includes/
/wp-*.php
/index.php
/readme.html
/license.txt

# Configuration
wp-config.php
.htaccess
wp-config-sample.php

# Uploads and cache
wp-content/uploads/
wp-content/cache/
wp-content/upgrade/
wp-content/upgrade-temp-backup/

# Third-party themes/plugins
wp-content/themes/kadence/
wp-content/themes/twentytwenty*/
wp-content/plugins/kadence-*/
wp-content/plugins/hello.php
wp-content/plugins/akismet/

# Only track our custom plugins
!wp-content/plugins/gtm-head-injection/

# System files
.DS_Store
Thumbs.db
*.log

# IDE files
.vscode/
.idea/

# Temporary files
*.tmp
*.bak
*~
EOF

    echo "✅ Git repository initialized with .gitignore"
fi

# Add plugin files to git
echo "📋 Adding plugin files to git..."
git add wp-content/plugins/gtm-head-injection/
git add reports/ scripts/ *.md

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "ℹ️  No new changes to commit"
else
    # Commit changes
    echo "💾 Committing changes..."
    git commit -m "Add GTM Head Injection plugin v1.0.0

- Lightweight WordPress plugin for GTM container injection
- Highest priority wp_head hook (priority 1)
- Generic container ID support (not hard-coded)
- Admin interface in Settings → GTM Settings
- Proper noscript fallback implementation
- WordPress coding standards compliant
- Ready for production deployment

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

    echo "✅ Changes committed to git"
fi

echo ""
echo "🎯 Deployment Phase 3: Production Deployment Summary"
echo "----------------------------------------------------"

# Verify deployment
if [ -f "$PROD_PLUGIN_PATH/gtm-head-injection.php" ]; then
    echo "✅ Plugin deployed successfully"
    echo "📁 Location: $PROD_PLUGIN_PATH"
    
    # Show plugin info
    echo ""
    echo "📋 Plugin Information:"
    echo "----------------------"
    head -10 "$PROD_PLUGIN_PATH/gtm-head-injection.php" | grep -E "Plugin Name|Description|Version|Author"
    
    echo ""
    echo "📋 Files Deployed:"
    echo "------------------"
    ls -la "$PROD_PLUGIN_PATH/"
    
else
    echo "❌ Plugin deployment failed"
    exit 1
fi

echo ""
echo "🔄 Next Steps (Manual):"
echo "------------------------"
echo "1. 🌐 Upload wp-content/plugins/gtm-head-injection/ to your live server"
echo "2. 🔌 Activate plugin in WordPress Admin → Plugins"
echo "3. ⚙️  Configure GTM container ID in Settings → GTM Settings"
echo "4. 🔍 Verify GTM firing with Google Tag Assistant"
echo "5. 🚀 Push to GitHub: git push origin main"
echo ""
echo "🎉 LOCAL DEPLOYMENT COMPLETE!"
echo "📍 Plugin ready at: $PROD_PLUGIN_PATH"