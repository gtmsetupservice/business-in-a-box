#!/bin/bash

# Deploy GTM Live Monitor Plugin Fix
# Updates the plugin with GA4 duplication fixes and visibility controls

echo "🚀 Deploying GTM Live Monitor Plugin Fix..."

# Plugin path
LOCAL_PLUGIN_PATH="/Volumes/Samsung/mo/prod/projects/gtmsetupservice.com/wp-content/plugins/gtm-live-monitor"
REMOTE_PATH="/var/www/gtmsetupservice.com/wp-content/plugins/gtm-live-monitor"

# Remote server details
REMOTE_USER="gtmsetupservice"
REMOTE_HOST="gtmsetupservice.com"

echo "📋 Changes in this update:"
echo "  ✅ Added is_gtm_already_loaded() method to prevent GTM duplication"
echo "  ✅ Enhanced detection of existing GTM/GA4 implementations"
echo "  ✅ Added visibility controls (admin only, logged in, public)"
echo "  ✅ Fixed GA4 cookie duplication issue"

# Check if plugin files exist
if [ ! -f "$LOCAL_PLUGIN_PATH/gtm-live-monitor.php" ]; then
    echo "❌ Plugin file not found: $LOCAL_PLUGIN_PATH/gtm-live-monitor.php"
    exit 1
fi

# Check PHP syntax before deployment
echo "🔍 Checking PHP syntax..."
php -l "$LOCAL_PLUGIN_PATH/gtm-live-monitor.php"
if [ $? -ne 0 ]; then
    echo "❌ PHP syntax errors detected. Aborting deployment."
    exit 1
fi

# Create backup on remote server
echo "💾 Creating backup on remote server..."
ssh $REMOTE_USER@$REMOTE_HOST "cp -r $REMOTE_PATH ${REMOTE_PATH}.backup-$(date +%Y%m%d-%H%M%S)"

# Deploy updated plugin files
echo "📤 Uploading updated plugin files..."
rsync -avz --delete \
    "$LOCAL_PLUGIN_PATH/" \
    "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/"

if [ $? -eq 0 ]; then
    echo "✅ Plugin deployed successfully!"
    echo ""
    echo "🧪 Test the fix by:"
    echo "  1. Visit gtmsetupservice.com in browser"
    echo "  2. Open browser console (F12)"
    echo "  3. Run the diagnostic script from test-ga4-fix.js"
    echo "  4. Check for 'FIXED' status in diagnosis"
    echo ""
    echo "⚙️ Configure visibility in WordPress admin:"
    echo "  Settings > GTM Live Monitor > Monitor Visibility"
else
    echo "❌ Deployment failed!"
    exit 1
fi