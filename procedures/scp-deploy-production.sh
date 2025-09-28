#!/bin/bash

echo "🚀 SCP Production Deployment - GTMSetupService.com"
echo "================================================="

# Configuration
SSH_KEY="~/.ssh/rack_nerd"
SERVER="fiber22-r.iaasdns.com"
PORT="1588"
USER="acmealli"
REMOTE_PATH="~/public_html/gtmsetupservice.com/wp-content/plugins/gtm-head-injection"
LOCAL_PLUGIN_PATH="/Volumes/Samsung/mo/local-sites/gtmsetupservicecom/app/public/wp-content/plugins/gtm-head-injection"

echo "📋 Pre-deployment Checks"
echo "-------------------------"

# Check local plugin exists
if [ ! -f "$LOCAL_PLUGIN_PATH/gtm-head-injection.php" ]; then
    echo "❌ Local plugin file not found: $LOCAL_PLUGIN_PATH/gtm-head-injection.php"
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

# Test SSH connection
echo "🔗 Testing SSH connection..."
if ! ssh -i $SSH_KEY -p $PORT $USER@$SERVER "pwd" > /dev/null 2>&1; then
    echo "❌ SSH connection failed"
    exit 1
fi

echo "✅ SSH connection successful"

echo ""
echo "📦 Deploying to Production Server"
echo "----------------------------------"

# Deploy main plugin file
echo "📋 Deploying gtm-head-injection.php..."
scp -i $SSH_KEY -P $PORT "$LOCAL_PLUGIN_PATH/gtm-head-injection.php" $USER@$SERVER:$REMOTE_PATH/gtm-head-injection.php

if [ $? -eq 0 ]; then
    echo "✅ Main plugin file deployed"
else
    echo "❌ Failed to deploy main plugin file"
    exit 1
fi

# Deploy README files
echo "📋 Deploying documentation files..."
scp -i $SSH_KEY -P $PORT "$LOCAL_PLUGIN_PATH/README.md" $USER@$SERVER:$REMOTE_PATH/README.md
scp -i $SSH_KEY -P $PORT "$LOCAL_PLUGIN_PATH/readme.txt" $USER@$SERVER:$REMOTE_PATH/readme.txt

echo "✅ Documentation files deployed"

echo ""
echo "🔍 Verifying Deployment"
echo "------------------------"

# Verify deployment
echo "📋 Checking deployed files..."
ssh -i $SSH_KEY -p $PORT $USER@$SERVER "cd $REMOTE_PATH && ls -la && echo '--- Plugin Header ---' && head -10 gtm-head-injection.php | grep -E 'Plugin Name|Version|Description'"

echo ""
echo "🎉 PRODUCTION DEPLOYMENT COMPLETE!"
echo "=================================="
echo "🌐 Plugin deployed to: gtmsetupservice.com"
echo "📁 Server path: $REMOTE_PATH"
echo ""
echo "🔄 Next Steps:"
echo "1. Login to WordPress Admin: https://gtmsetupservice.com/wp-admin"
echo "2. Go to Plugins page and verify plugin appears"
echo "3. Configure GTM settings if needed"
echo "4. Test with Google Tag Assistant"
echo ""
echo "✅ Ready for use!"