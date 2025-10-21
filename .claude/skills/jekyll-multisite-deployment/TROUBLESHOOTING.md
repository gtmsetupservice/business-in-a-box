# Troubleshooting Jekyll Multi-Site Deployment

## Sync Issues

### Sync workflow didn't trigger
**Symptoms**: Pushed to main but no sync workflow ran

**Causes**:
- Changes were pushed to staging instead of main
- Files changed outside `sites/SITENAME/` directories
- Workflow file itself has syntax errors

**Solutions**:
1. Verify you pushed to main: `git branch --show-current`
2. Check which files changed: `git diff origin/main`
3. Review workflow runs: https://github.com/gtmsetupservice/business-in-a-box/actions
4. Manually trigger workflow if needed (Actions tab → Select workflow → Run workflow)

### Sync failed with authentication error
**Symptoms**: "Resource not accessible by integration" or "Authentication failed"

**Causes**:
- `GH_PAT` secret missing or invalid
- PAT lacks required permissions
- PAT has expired

**Solutions**:
1. Verify secret exists: Repository Settings → Secrets → Actions → GH_PAT
2. Generate new PAT: https://github.com/settings/tokens/new
   - Required scope: `repo` (full control)
3. Update secret with new PAT value

### Sync completed but target repo unchanged
**Symptoms**: Workflow shows success but target repository has no new commits

**Causes**:
- No actual file changes detected
- `.gitignore` blocking files
- Sync script logic issue

**Solutions**:
1. Check workflow logs for "No changes to sync" message
2. Verify files exist in source: `ls -la sites/SITENAME/`
3. Check target repo last commit: `gh repo view gtmsetupservice/SITENAME --json pushedAt`

## Deployment Issues

### Deployment failed on target repository
**Symptoms**: Sync succeeded but deployment workflow failed

**Causes**:
- Missing `Gemfile.lock`
- Invalid YAML in `_config.yml`
- Missing deployment workflow
- GitHub Pages not configured

**Solutions**:
1. Check target repo Actions tab for error details
2. Verify deployment workflow exists: `.github/workflows/deploy.yml`
3. Validate Jekyll config: `cd sites/SITENAME && bundle exec jekyll doctor`
4. Ensure Gemfile.lock is committed: `git add sites/SITENAME/Gemfile.lock`
5. Verify Pages enabled: Repository Settings → Pages → Source: "GitHub Actions"

### Site shows old content
**Symptoms**: Deployment succeeded but site shows outdated content

**Causes**:
- Browser cache
- CDN propagation delay
- Wrong repository serving domain

**Solutions**:
1. Hard refresh browser: Cmd+Shift+R (Mac) / Ctrl+Shift+R (Windows)
2. Wait 5-10 minutes for CDN propagation
3. Verify correct repo has custom domain: Settings → Pages → Custom domain
4. Check DNS: `dig SITENAME.com` should show GitHub Pages IPs

### Wrong site content on domain
**Symptoms**: gtmsetupservice.com shows locallyknown.pro content (or vice versa)

**Causes**:
- Multiple repos configured with same custom domain
- DNS CNAME pointing to wrong repository

**Solutions**:
1. Verify only ONE repo has the custom domain:
   - gtmsetupservice.com → only in gtmsetupservice/gtmsetupservice.com
   - locallyknown.pro → only in gtmsetupservice/locallyknown.pro
   - ifixshopify.com → only in gtmsetupservice/ifixshopify.com
2. Remove domain from incorrect repos: Settings → Pages → Custom domain → Remove
3. Verify DNS CNAME: `dig CNAME gtmsetupservice.com`

## Cross-Posting Issues

### Multiple sites deployed when editing one
**Symptoms**: Changed gtmsetupservice.com but all three sites deployed

**Causes**:
- Files changed outside intended `sites/SITENAME/` directory
- Workflow path filters incorrect
- Manual workflow trigger instead of push

**Solutions**:
1. Check which files actually changed: `git diff HEAD~1`
2. Verify workflow path filters in `.github/workflows/sync-*.yml`:
   ```yaml
   on:
     push:
       paths:
         - "sites/gtmsetupservice.com/**"  # Should be site-specific
   ```
3. Review git commit to ensure only one site's files changed

## Git Workflow Issues

### Accidentally committed to main
**Symptoms**: Pushed changes directly to main instead of staging

**Solutions**:
1. If not yet pushed:
   ```bash
   git reset --soft HEAD~1  # Undo commit, keep changes
   git checkout staging
   git add .
   git commit -m "Same message"
   ```

2. If already pushed:
   ```bash
   git checkout staging
   git cherry-pick COMMIT_HASH  # Copy commit to staging
   # Continue normal workflow from staging
   ```

### Merge conflict between staging and main
**Symptoms**: `git merge staging` shows conflicts

**Solutions**:
1. Identify conflicted files: `git status`
2. Open files and resolve conflicts manually
3. Mark as resolved: `git add FILENAME`
4. Complete merge: `git commit`
5. Push: `git push origin main`

### Lost changes after switching branches
**Symptoms**: Changes disappeared when switching branches

**Solutions**:
1. Check if changes were committed: `git log`
2. Check stash: `git stash list`
3. Recover from stash: `git stash pop`
4. Find lost commits: `git reflog`

## Prerequisites Issues

### Missing GH_PAT secret
**Symptoms**: Sync workflows fail immediately with authentication error

**Solutions**:
1. Go to https://github.com/settings/tokens/new
2. Token name: "Cross-Repo Sync"
3. Expiration: 1 year (or no expiration)
4. Scopes: Check `repo` (full control)
5. Generate token and copy immediately
6. Add to repository: Settings → Secrets → Actions → New secret
   - Name: `GH_PAT`
   - Value: Paste token

### Missing deployment workflow in target repo
**Symptoms**: Sync succeeds but no deployment happens

**Solutions**:
1. Check if workflow exists:
   ```bash
   gh api repos/gtmsetupservice/SITENAME/contents/.github/workflows/deploy.yml
   ```
2. If missing, copy from templates:
   ```bash
   cp deployment-workflows/deploy-SITENAME.yml .github/workflows/deploy.yml
   git add .github/workflows/deploy.yml
   git commit -m "Add deployment workflow"
   git push
   ```

### GitHub Pages not enabled
**Symptoms**: Deployment workflow succeeds but site returns 404

**Solutions**:
1. Go to target repository Settings → Pages
2. Source: Select "GitHub Actions"
3. Custom domain: Enter domain name (e.g., gtmsetupservice.com)
4. Enforce HTTPS: Check box
5. Wait 5 minutes for setup to complete

## Emergency Rollback

### Need to revert to previous version
**Symptoms**: Bad deployment, need to restore working version

**Solutions**:
1. Find last good commit:
   ```bash
   git log --oneline
   ```
2. Revert to that commit:
   ```bash
   git checkout staging
   git revert BAD_COMMIT_HASH
   git push origin staging

   git checkout main
   git merge staging
   git push origin main
   ```
3. Or restore specific files:
   ```bash
   git checkout GOOD_COMMIT_HASH -- sites/SITENAME/path/to/file
   git commit -m "Restore file from GOOD_COMMIT_HASH"
   git push origin main
   ```

## Getting Help

### Enable debug logging
Add `ACTIONS_STEP_DEBUG` secret with value `true` to get detailed workflow logs:
1. Repository Settings → Secrets → Actions
2. New secret: `ACTIONS_STEP_DEBUG` = `true`
3. Re-run workflow

### Check workflow logs
1. Go to https://github.com/gtmsetupservice/business-in-a-box/actions
2. Click on failed workflow run
3. Click on failed job
4. Expand failed step to see full error output

### Verify file structure
```bash
# Check source files exist
ls -la sites/gtmsetupservice.com/

# Check target repo received files
gh repo clone gtmsetupservice/gtmsetupservice.com /tmp/check
ls -la /tmp/check/
```

### Manual sync (emergency)
If automation fails, manually sync:
```bash
# Clone target repo
git clone https://github.com/gtmsetupservice/gtmsetupservice.com.git /tmp/manual-sync
cd /tmp/manual-sync

# Copy content
rm -rf * .!(git|github)
cp -r /path/to/business-in-a-box/sites/gtmsetupservice.com/* .

# Push
git add -A
git commit -m "Manual sync from business-in-a-box"
git push origin main
```
