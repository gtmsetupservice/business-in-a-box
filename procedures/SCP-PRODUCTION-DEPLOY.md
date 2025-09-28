# SCP Production Deployment Procedure
**GTMSetupService.com Production Server Deployment via SCP**

## 🎯 Quick Production Deploy

```bash
# Deploy plugin to production server
scp -i ~/.ssh/rack_nerd -P 1588 /path/to/local/plugin/file.php acmealli@fiber22-r.iaasdns.com:~/public_html/gtmsetupservice.com/wp-content/plugins/plugin-folder/file.php
```

## 📋 Production Server Details

### Connection Information
- **Server**: fiber22-r.iaasdns.com
- **Port**: 1588
- **User**: acmealli  
- **SSH Key**: `~/.ssh/rack_nerd`
- **WordPress Path**: `~/public_html/gtmsetupservice.com`
- **Plugin Directory**: `~/public_html/gtmsetupservice.com/wp-content/plugins/`

### Hosting Provider
- **Provider**: Rackspace
- **Server Type**: Shared hosting with jailshell (rsync not available)
- **File Transfer**: SCP only (rsync disabled)

## 🚀 Step-by-Step SCP Deployment

### Step 1: Verify Local Plugin
```bash
# Check local plugin exists and syntax is valid
LOCAL_PLUGIN="/Volumes/Samsung/mo/local-sites/gtmsetupservicecom/app/public/wp-content/plugins/gtm-head-injection/gtm-head-injection.php"
php -l "$LOCAL_PLUGIN"
```

### Step 2: Test SSH Connection
```bash
# Test connection to production server
ssh -i ~/.ssh/rack_nerd -p 1588 acmealli@fiber22-r.iaasdns.com "pwd && ls -la public_html/gtmsetupservice.com/wp-content/plugins/"
```

### Step 3: Deploy Main Plugin File
```bash
# Deploy main PHP file
scp -i ~/.ssh/rack_nerd -P 1588 \
  /Volumes/Samsung/mo/local-sites/gtmsetupservicecom/app/public/wp-content/plugins/gtm-head-injection/gtm-head-injection.php \
  acmealli@fiber22-r.iaasdns.com:~/public_html/gtmsetupservice.com/wp-content/plugins/gtm-head-injection/gtm-head-injection.php
```

### Step 4: Deploy Additional Files (if needed)
```bash
# Deploy README files
scp -i ~/.ssh/rack_nerd -P 1588 \
  /Volumes/Samsung/mo/local-sites/gtmsetupservicecom/app/public/wp-content/plugins/gtm-head-injection/README.md \
  acmealli@fiber22-r.iaasdns.com:~/public_html/gtmsetupservice.com/wp-content/plugins/gtm-head-injection/README.md

scp -i ~/.ssh/rack_nerd -P 1588 \
  /Volumes/Samsung/mo/local-sites/gtmsetupservicecom/app/public/wp-content/plugins/gtm-head-injection/readme.txt \
  acmealli@fiber22-r.iaasdns.com:~/public_html/gtmsetupservice.com/wp-content/plugins/gtm-head-injection/readme.txt
```

### Step 5: Verify Deployment
```bash
# Check deployed files
ssh -i ~/.ssh/rack_nerd -p 1588 acmealli@fiber22-r.iaasdns.com \
  "cd ~/public_html/gtmsetupservice.com/wp-content/plugins/gtm-head-injection && ls -la && head -15 gtm-head-injection.php"
```

## 🔧 Automated SCP Deploy Script

Create `/Volumes/Samsung/mo/prod/projects/gtmsetupservice.com/scripts/scp-deploy-production.sh`:

```bash
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
```

## 🛠️ Common SCP Commands

### Deploy Single File
```bash
scp -i ~/.ssh/rack_nerd -P 1588 localfile.php acmealli@fiber22-r.iaasdns.com:~/public_html/gtmsetupservice.com/wp-content/plugins/plugin-name/localfile.php
```

### Deploy Multiple Files
```bash
scp -i ~/.ssh/rack_nerd -P 1588 file1.php file2.txt acmealli@fiber22-r.iaasdns.com:~/public_html/gtmsetupservice.com/wp-content/plugins/plugin-name/
```

### Deploy Entire Directory (not supported on this server)
```bash
# This doesn't work on jailshell - use individual file transfers
# scp -r -i ~/.ssh/rack_nerd -P 1588 local-dir/ user@server:/remote-dir/
```

## ⚠️ Important Notes

### Server Limitations
- **No rsync**: Rackspace jailshell doesn't have rsync command
- **No recursive directory copy**: Must transfer files individually
- **Limited shell access**: Basic commands only

### Security Best Practices
- Always use SSH key authentication (never passwords)
- Verify file transfers completed successfully
- Test SSH connection before attempting file transfers
- Keep SSH keys secure and backed up

### File Permissions
- Deployed files automatically get correct permissions (644 for files)
- No manual chmod needed on Rackspace shared hosting
- WordPress handles plugin file permissions automatically

## 🔄 Update Workflow

### For Plugin Updates:
1. **Modify local plugin**
2. **Test locally**
3. **Commit to Git**
4. **Push to GitHub**
5. **Deploy to production via SCP**
6. **Verify in production WordPress**

### Quick Update Command:
```bash
# Single command for main plugin file updates
scp -i ~/.ssh/rack_nerd -P 1588 \
  /Volumes/Samsung/mo/local-sites/gtmsetupservicecom/app/public/wp-content/plugins/gtm-head-injection/gtm-head-injection.php \
  acmealli@fiber22-r.iaasdns.com:~/public_html/gtmsetupservice.com/wp-content/plugins/gtm-head-injection/gtm-head-injection.php && \
echo "✅ Plugin updated on production!"
```

## 📊 Deployment Verification Checklist

After SCP deployment:
- [ ] Files copied without errors
- [ ] SSH connection successful  
- [ ] Plugin files present on server
- [ ] File sizes match local versions
- [ ] WordPress recognizes plugin
- [ ] Plugin settings accessible
- [ ] No PHP errors in WordPress
- [ ] Functionality works as expected

---

**This SCP deployment procedure is now documented for repeatable production deployments to GTMSetupService.com Rackspace server.**