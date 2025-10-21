# Cross-Repo Deployment Migration Guide

This guide details the migration from single-repo deployment to cross-repo deployment for all three Jekyll sites.

## Architecture Overview

### Before Migration
```
gtmsetupservice/business-in-a-box (serves gtmsetupservice.com via Pages)
├── sites/gtmsetupservice.com/
├── sites/locallyknown.pro/
├── sites/ifixshopify.com/
└── .github/workflows/deploy-gtmsetupservice.yml (DELETED)

gtmsetupservice/gtmsetupservice.com (ARCHIVED - will be reactivated)
gtmsetupservice/locallyknown.pro (Pages LEGACY mode)
gtmsetupservice/ifixshopify.com (Pages LEGACY mode)
```

### After Migration
```
Development Workspace (business-in-a-box):
├── sites/gtmsetupservice.com/     ← Edit here
├── sites/locallyknown.pro/        ← Edit here
├── sites/ifixshopify.com/         ← Edit here
├── .github/workflows/
│   ├── sync-gtmsetupservice.yml   ← NEW: Auto-sync to gtmsetupservice.com
│   ├── sync-locallyknown-pro.yml  ← NEW: Auto-sync to locallyknown.pro
│   └── sync-ifixshopify.yml       ← NEW: Auto-sync to ifixshopify.com
└── deployment-workflows/          ← Templates for target repos
    ├── deploy-gtmsetupservice.yml
    ├── deploy-locallyknown-pro.yml
    └── deploy-ifixshopify.yml

Target Deployment Repositories:
gtmsetupservice/gtmsetupservice.com
├── .github/workflows/deploy.yml   → Deploys to https://gtmsetupservice.com
└── (Synced content from business-in-a-box)

gtmsetupservice/locallyknown.pro
├── .github/workflows/deploy.yml   → Deploys to https://locallyknown.pro
└── (Synced content from business-in-a-box)

gtmsetupservice/ifixshopify.com
├── .github/workflows/deploy.yml   → Deploys to https://ifixshopify.com
└── (Synced content from business-in-a-box)
```

## Isolation Guarantee

Each sync workflow uses path-based filtering to prevent cross-posting:

```yaml
# sync-gtmsetupservice.yml
on:
  push:
    paths:
      - "sites/gtmsetupservice.com/**"  # ONLY triggers for this directory

# sync-locallyknown-pro.yml
on:
  push:
    paths:
      - "sites/locallyknown.pro/**"     # ONLY triggers for this directory

# sync-ifixshopify.yml
on:
  push:
    paths:
      - "sites/ifixshopify.com/**"      # ONLY triggers for this directory
```

**Result**: Changes to `sites/gtmsetupservice.com/` will NEVER trigger syncs to locallyknown.pro or ifixshopify.com.

## Migration Steps

### Phase 1: GitHub Repository Setup

1. **Unarchive gtmsetupservice.com repository**
   - Go to https://github.com/gtmsetupservice/gtmsetupservice.com/settings
   - Scroll to "Danger Zone"
   - Click "Unarchive this repository"

2. **Disable Pages on business-in-a-box**
   - Go to https://github.com/gtmsetupservice/business-in-a-box/settings/pages
   - Click "Unpublish site"
   - This frees the gtmsetupservice.com custom domain

3. **Clear old content from gtmsetupservice.com repo**
   ```bash
   git clone https://github.com/gtmsetupservice/gtmsetupservice.com.git
   cd gtmsetupservice.com

   # Remove all old content (keep .git)
   find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +

   git add -A
   git commit -m "Clear old content for fresh sync"
   git push origin main
   ```

### Phase 2: Create Personal Access Token (PAT)

1. **Generate GitHub PAT**
   - Go to https://github.com/settings/tokens/new
   - Token name: "Cross-Repo Sync for business-in-a-box"
   - Expiration: No expiration (or 1 year)
   - Scopes: Select `repo` (full control of private repositories)
   - Click "Generate token"
   - **IMPORTANT**: Copy the token immediately (you won't see it again)

2. **Add PAT to business-in-a-box repository secrets**
   - Go to https://github.com/gtmsetupservice/business-in-a-box/settings/secrets/actions
   - Click "New repository secret"
   - Name: `GH_PAT`
   - Value: Paste the PAT you just created
   - Click "Add secret"

### Phase 3: Deploy Workflows to Target Repositories

For each target repository, copy the deployment workflow:

#### gtmsetupservice.com
```bash
# Clone the repo
git clone https://github.com/gtmsetupservice/gtmsetupservice.com.git
cd gtmsetupservice.com

# Create .github/workflows directory
mkdir -p .github/workflows

# Copy deployment workflow from business-in-a-box
cp ../business-in-a-box/deployment-workflows/deploy-gtmsetupservice.yml .github/workflows/deploy.yml

# Commit and push
git add .github/workflows/deploy.yml
git commit -m "Add GitHub Pages deployment workflow"
git push origin main
```

#### locallyknown.pro
```bash
# Clone the repo
git clone https://github.com/gtmsetupservice/locallyknown.pro.git
cd locallyknown.pro

# Create .github/workflows directory (if it doesn't exist)
mkdir -p .github/workflows

# Copy deployment workflow from business-in-a-box
cp ../business-in-a-box/deployment-workflows/deploy-locallyknown-pro.yml .github/workflows/deploy.yml

# Commit and push
git add .github/workflows/deploy.yml
git commit -m "Add GitHub Pages deployment workflow"
git push origin main
```

#### ifixshopify.com
```bash
# Clone the repo
git clone https://github.com/gtmsetupservice/ifixshopify.com.git
cd ifixshopify.com

# Create .github/workflows directory (if it doesn't exist)
mkdir -p .github/workflows

# Copy deployment workflow from business-in-a-box
cp ../business-in-a-box/deployment-workflows/deploy-ifixshopify.yml .github/workflows/deploy.yml

# Commit and push
git add .github/workflows/deploy.yml
git commit -m "Add GitHub Pages deployment workflow"
git push origin main
```

### Phase 4: Configure GitHub Pages

For each target repository, configure Pages:

#### gtmsetupservice.com
1. Go to https://github.com/gtmsetupservice/gtmsetupservice.com/settings/pages
2. Source: "GitHub Actions"
3. Custom domain: `gtmsetupservice.com`
4. Enforce HTTPS: ✓ (checked)

#### locallyknown.pro
1. Go to https://github.com/gtmsetupservice/locallyknown.pro/settings/pages
2. Source: "GitHub Actions"
3. Custom domain: `locallyknown.pro`
4. Enforce HTTPS: ✓ (checked)

#### ifixshopify.com
1. Go to https://github.com/gtmsetupservice/ifixshopify.com/settings/pages
2. Source: "GitHub Actions"
3. Custom domain: `ifixshopify.com`
4. Enforce HTTPS: ✓ (checked)

### Phase 5: Initial Sync

Trigger the sync workflows manually to populate the target repositories:

1. **Sync gtmsetupservice.com**
   - Go to https://github.com/gtmsetupservice/business-in-a-box/actions/workflows/sync-gtmsetupservice.yml
   - Click "Run workflow"
   - Wait for completion

2. **Sync locallyknown.pro**
   - Go to https://github.com/gtmsetupservice/business-in-a-box/actions/workflows/sync-locallyknown-pro.yml
   - Click "Run workflow"
   - Wait for completion

3. **Sync ifixshopify.com**
   - Go to https://github.com/gtmsetupservice/business-in-a-box/actions/workflows/sync-ifixshopify.yml
   - Click "Run workflow"
   - Wait for completion

### Phase 6: Verify Deployments

Check that all three sites deployed successfully:

1. **gtmsetupservice.com**
   - Go to https://github.com/gtmsetupservice/gtmsetupservice.com/actions
   - Verify "Deploy to GitHub Pages" workflow ran successfully
   - Visit https://gtmsetupservice.com (may take 5-10 minutes for DNS)

2. **locallyknown.pro**
   - Go to https://github.com/gtmsetupservice/locallyknown.pro/actions
   - Verify "Deploy to GitHub Pages" workflow ran successfully
   - Visit https://locallyknown.pro

3. **ifixshopify.com**
   - Go to https://github.com/gtmsetupservice/ifixshopify.com/actions
   - Verify "Deploy to GitHub Pages" workflow ran successfully
   - Visit https://ifixshopify.com

## Testing Isolation (No Cross-Posting)

After migration, test that workflows are properly isolated:

### Test 1: Edit gtmsetupservice.com
```bash
cd business-in-a-box

# Make a test change
echo "Test change" >> sites/gtmsetupservice.com/test.txt

git add sites/gtmsetupservice.com/test.txt
git commit -m "Test gtmsetupservice.com isolation"
git push origin main

# Expected: Only sync-gtmsetupservice.yml runs
# Check: https://github.com/gtmsetupservice/business-in-a-box/actions
```

### Test 2: Edit locallyknown.pro
```bash
# Make a test change
echo "Test change" >> sites/locallyknown.pro/test.txt

git add sites/locallyknown.pro/test.txt
git commit -m "Test locallyknown.pro isolation"
git push origin main

# Expected: Only sync-locallyknown-pro.yml runs
```

### Test 3: Edit ifixshopify.com
```bash
# Make a test change
echo "Test change" >> sites/ifixshopify.com/test.txt

git add sites/ifixshopify.com/test.txt
git commit -m "Test ifixshopify.com isolation"
git push origin main

# Expected: Only sync-ifixshopify.yml runs
```

## Workflow Behavior

### Automatic Sync (On Push)
When you push changes to business-in-a-box:
1. GitHub detects which subdirectory changed
2. Only the corresponding sync workflow triggers
3. Content syncs to the target repository
4. Target repository's deployment workflow triggers
5. Site deploys to GitHub Pages

### Manual Sync
You can manually trigger any sync workflow:
- https://github.com/gtmsetupservice/business-in-a-box/actions/workflows/sync-gtmsetupservice.yml
- https://github.com/gtmsetupservice/business-in-a-box/actions/workflows/sync-locallyknown-pro.yml
- https://github.com/gtmsetupservice/business-in-a-box/actions/workflows/sync-ifixshopify.yml

## Development Workflow

### Editing Content
```bash
cd business-in-a-box

# Edit any site
vim sites/gtmsetupservice.com/_posts/new-post.md
vim sites/locallyknown.pro/index.md
vim sites/ifixshopify.com/about.md

# Commit and push (triggers automatic sync)
git add .
git commit -m "Update content"
git push origin main
```

### Viewing Sync Status
Check sync workflow runs:
- https://github.com/gtmsetupservice/business-in-a-box/actions

Check deployment status:
- https://github.com/gtmsetupservice/gtmsetupservice.com/actions
- https://github.com/gtmsetupservice/locallyknown.pro/actions
- https://github.com/gtmsetupservice/ifixshopify.com/actions

### Troubleshooting

**Sync fails with "Resource not accessible by integration"**
- Check that GH_PAT secret is set correctly in business-in-a-box
- Verify PAT has `repo` scope
- Regenerate PAT if expired

**Deployment fails with "No uploaded artifact found"**
- Check that sync completed successfully
- Verify deployment workflow exists in target repo
- Check that Pages is enabled with "GitHub Actions" source

**Wrong site content appears on domain**
- Verify only ONE repository has the custom domain configured
- Check DNS CNAME record points to `gtmsetupservice.github.io`
- Wait 5-10 minutes for DNS propagation

**Sync triggers for wrong subdirectory**
- Verify workflow path filters are correct
- Check git diff shows changes only in intended subdirectory
- Review GitHub Actions run logs to see which files changed

## Rollback Plan

If issues occur, you can rollback:

1. **Re-enable Pages on business-in-a-box**
   - Settings > Pages > Source: "GitHub Actions"
   - Add old deploy-gtmsetupservice.yml workflow back

2. **Disable Pages on target repos**
   - Each target repo: Settings > Pages > "Unpublish site"

3. **Remove sync workflows**
   ```bash
   cd business-in-a-box
   git rm .github/workflows/sync-*.yml
   git commit -m "Rollback to single-repo deployment"
   git push origin main
   ```

## Maintenance

### Updating Deployment Workflows
If you need to update the deployment configuration:

1. Edit the template in `deployment-workflows/`
2. Copy to each target repository
3. Commit and push to target repos

### Monitoring
Regularly check:
- Sync workflow success rate
- Deployment workflow success rate
- Site uptime (https://uptimerobot.com or similar)
- SSL certificate validity

## Summary

After migration:
- ✅ Edit all sites in `business-in-a-box/sites/`
- ✅ Push to main → automatic sync → automatic deployment
- ✅ Each site isolated (no cross-posting)
- ✅ Each site serves on its own custom domain
- ✅ All sites use modern GitHub Actions workflows
- ✅ Clean separation: development (business-in-a-box) vs. deployment (target repos)
