#!/bin/bash

echo "🚀 GTM Live Monitor Plugin Deployment to Production"
echo "===================================================="

# Configuration from existing deployment script
SSH_KEY="~/.ssh/rack_nerd"
SERVER="fiber22-r.iaasdns.com"
PORT="1588"
USER="acmealli"
REMOTE_PLUGIN_PATH="~/public_html/gtmsetupservice.com/wp-content/plugins/gtm-live-monitor"
LOCAL_PLUGIN_PATH="wp-content/plugins/gtm-live-monitor"

echo "📋 Pre-deployment Checks"
echo "-------------------------"

# Check local plugin exists
if [ ! -f "$LOCAL_PLUGIN_PATH/gtm-live-monitor.php" ]; then
    echo "❌ Local plugin file not found: $LOCAL_PLUGIN_PATH/gtm-live-monitor.php"
    exit 1
fi

echo "✅ Local plugin found"

# Check PHP syntax
echo "🔍 Validating PHP syntax..."
if ! php -l "$LOCAL_PLUGIN_PATH/gtm-live-monitor.php" > /dev/null 2>&1; then
    echo "❌ PHP syntax error in plugin file"
    exit 1
fi

echo "✅ PHP syntax valid"

# Expand SSH key path
SSH_KEY_EXPANDED=$(eval echo $SSH_KEY)

# Test SSH connection
echo "🔗 Testing SSH connection..."
if ! ssh -o ConnectTimeout=5 -i $SSH_KEY_EXPANDED -p $PORT $USER@$SERVER "pwd" > /dev/null 2>&1; then
    echo "❌ SSH connection failed"
    echo "Please ensure:"
    echo "  - SSH key exists at: $SSH_KEY_EXPANDED"
    echo "  - Server is accessible: $SERVER:$PORT"
    echo "  - User credentials are correct: $USER"
    exit 1
fi

echo "✅ SSH connection successful"

echo ""
echo "📦 Creating Remote Directory Structure"
echo "---------------------------------------"

# Create remote plugin directory if it doesn't exist
ssh -i $SSH_KEY_EXPANDED -p $PORT $USER@$SERVER "mkdir -p $REMOTE_PLUGIN_PATH"

echo "✅ Remote directory prepared"

echo ""
echo "📦 Deploying Plugin Files to Production"
echo "-----------------------------------------"

# Use rsync for efficient deployment
echo "📋 Syncing plugin files..."
rsync -avz --delete \
    -e "ssh -i $SSH_KEY_EXPANDED -p $PORT" \
    "$LOCAL_PLUGIN_PATH/" \
    "$USER@$SERVER:$REMOTE_PLUGIN_PATH/"

if [ $? -eq 0 ]; then
    echo "✅ Plugin files synchronized successfully"
else
    echo "❌ Failed to sync plugin files"
    echo "Trying fallback SCP method..."

    # Fallback to SCP if rsync fails
    echo "📋 Deploying main plugin file..."
    scp -i $SSH_KEY_EXPANDED -P $PORT "$LOCAL_PLUGIN_PATH/gtm-live-monitor.php" $USER@$SERVER:$REMOTE_PLUGIN_PATH/

    echo "📋 Deploying documentation..."
    scp -i $SSH_KEY_EXPANDED -P $PORT "$LOCAL_PLUGIN_PATH/README.md" $USER@$SERVER:$REMOTE_PLUGIN_PATH/
    scp -i $SSH_KEY_EXPANDED -P $PORT "$LOCAL_PLUGIN_PATH/PLUGIN-PLAN.md" $USER@$SERVER:$REMOTE_PLUGIN_PATH/
    scp -i $SSH_KEY_EXPANDED -P $PORT "$LOCAL_PLUGIN_PATH/KADENCE-INTEGRATION-PLAN.md" $USER@$SERVER:$REMOTE_PLUGIN_PATH/

    if [ $? -eq 0 ]; then
        echo "✅ Files deployed via SCP"
    else
        echo "❌ Deployment failed"
        exit 1
    fi
fi

echo ""
echo "🔍 Verifying Deployment"
echo "------------------------"

# Verify deployment and show plugin info
echo "📋 Checking deployed files..."
ssh -i $SSH_KEY_EXPANDED -p $PORT $USER@$SERVER "
    echo 'Files in plugin directory:'
    ls -la $REMOTE_PLUGIN_PATH/
    echo ''
    echo '--- Plugin Header ---'
    head -15 $REMOTE_PLUGIN_PATH/gtm-live-monitor.php | grep -E 'Plugin Name|Description|Version|Author'
"

echo ""
echo "🎉 PRODUCTION DEPLOYMENT COMPLETE!"
echo "=================================="
echo ""
echo "📊 Deployment Summary:"
echo "----------------------"
echo "🌐 Website: https://gtmsetupservice.com"
echo "📁 Plugin Path: ~/public_html/gtmsetupservice.com/wp-content/plugins/gtm-live-monitor/"
echo "🔌 Plugin Name: GTM Live Monitor v1.0.0"
echo ""
echo "🔄 Next Steps:"
echo "--------------"
echo "1. Login to WordPress Admin: https://gtmsetupservice.com/wp-admin"
echo "2. Navigate to: Plugins → Installed Plugins"
echo "3. Find 'GTM Live Monitor' and click 'Activate'"
echo "4. Configure at: Settings → GTM Live Monitor"
echo "5. Set your GTM Container ID (or use demo mode)"
echo "6. Visit frontend while logged in as admin to see the monitor bar"
echo ""
echo "🧪 Testing:"
echo "-----------"
echo "• Enable demo mode for client demonstrations"
echo "• Monitor will appear at top/bottom of page (configurable)"
echo "• Shows real-time dataLayer events"
echo "• Only visible to logged-in administrators"
echo ""
echo "✅ Plugin deployed and ready for activation!"