---
name: Jekyll Multi-Site Deployment
description: Manage three Jekyll sites (gtmsetupservice.com, locallyknown.pro, ifixshopify.com) with staging/main branch workflow and cross-repo deployment. Use when editing site content, deploying changes, or managing Jekyll site files.
---

# Jekyll Multi-Site Deployment

This skill manages the workflow for three Jekyll sites in this monorepo with cross-repo deployment to individual GitHub repositories.

## Site Structure

### Development Files (Local)
All development work happens in `sites/` subdirectories:

- `sites/gtmsetupservice.com/` - GTM Setup Service site
- `sites/locallyknown.pro/` - Locally Known Pro site
- `sites/ifixshopify.com/` - I Fix Shopify site

### Production Repositories (Remote)
Each site deploys to its own GitHub repository:

- `gtmsetupservice/gtmsetupservice.com` → https://gtmsetupservice.com
- `gtmsetupservice/locallyknown.pro` → https://locallyknown.pro
- `gtmsetupservice/ifixshopify.com` → https://ifixshopify.com

## Branch Workflow

### Branches
- `staging` - Development and testing branch
- `main` - Production branch (triggers automatic deployment)

### Standard Workflow

1. **Make changes in staging**
   ```bash
   git checkout staging
   # Edit files in sites/SITENAME/
   git add sites/SITENAME/
   git commit -m "Description"
   git push origin staging
   ```

2. **Test changes** (if staging environment available)

3. **Merge to main for deployment**
   ```bash
   git checkout main
   git merge staging
   git push origin main
   ```

4. **Automatic deployment happens**:
   - GitHub Actions detects which site changed
   - Sync workflow copies content to target repository
   - Target repository deploys to GitHub Pages

## Sync Mechanism

Workflows in `.github/workflows/` handle automatic syncing:

- `sync-gtmsetupservice.yml` - Syncs `sites/gtmsetupservice.com/` → `gtmsetupservice/gtmsetupservice.com`
- `sync-locallyknown-pro.yml` - Syncs `sites/locallyknown.pro/` → `gtmsetupservice/locallyknown.pro`
- `sync-ifixshopify.yml` - Syncs `sites/ifixshopify.com/` → `gtmsetupservice/ifixshopify.com`

**Path isolation**: Each workflow only triggers when files in its specific `sites/SITENAME/` directory change. No cross-posting occurs.

## Common Tasks

### Editing Blog Posts
```bash
git checkout staging
vim sites/gtmsetupservice.com/_posts/2025-10-21-new-post.md
git add sites/gtmsetupservice.com/_posts/
git commit -m "Add new blog post"
git push origin staging

# After review, deploy to production
git checkout main
git merge staging
git push origin main
```

### Updating Site Configuration
```bash
git checkout staging
vim sites/locallyknown.pro/_config.yml
git add sites/locallyknown.pro/_config.yml
git commit -m "Update site configuration"
git push origin staging

# After testing, deploy
git checkout main
git merge staging
git push origin main
```

### Adding New Pages
```bash
git checkout staging
vim sites/ifixshopify.com/services.md
git add sites/ifixshopify.com/
git commit -m "Add services page"
git push origin staging

# After review, deploy
git checkout main
git merge staging
git push origin main
```

## Verification

### Check Sync Status
Monitor workflows: https://github.com/gtmsetupservice/business-in-a-box/actions

### Check Deployment Status
- https://github.com/gtmsetupservice/gtmsetupservice.com/actions
- https://github.com/gtmsetupservice/locallyknown.pro/actions
- https://github.com/gtmsetupservice/ifixshopify.com/actions

### Verify Live Sites
After deployment (2-5 minutes):
- https://gtmsetupservice.com
- https://locallyknown.pro
- https://ifixshopify.com

## Key Principles

1. **Always work in staging first** - Never commit directly to main
2. **Only main triggers deployment** - Staging pushes do not deploy
3. **Path-based isolation** - Editing one site only deploys that site
4. **Automatic sync** - No manual deployment steps needed

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.
