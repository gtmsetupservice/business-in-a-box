# Security Notice - Business-in-a-Box Template System

## ⚠️ IMPORTANT SECURITY INFORMATION

### Credential Management

**NEVER commit sensitive data to this repository:**
- API credentials
- Client information
- Database files with real data
- Environment files with secrets

### Required Setup Before Use

1. **Copy environment template:**
   ```bash
   cp .env.template .env
   ```

2. **Add your API credentials to .env:**
   ```bash
   DATA_FOR_SEO_USER=your_actual_username
   DATA_FOR_SEO_PASSWORD=your_actual_password
   ```

3. **Verify .env is in .gitignore:**
   ```bash
   cat .gitignore | grep .env
   ```

### Known Security Cleanup

**Scripts contain placeholder credentials that must be updated:**
- Several Python files in `/scripts/` directory contain hardcoded credentials
- These are from the original GTMSetupService system
- Before using, update these scripts to use environment variables
- Files affected: `comprehensive_niche_report.py`, `gtm_competition_analyzer.py`, and others

### Production Deployment Checklist

- [ ] Replace all hardcoded credentials with environment variables
- [ ] Verify .env file is not committed
- [ ] Remove any sample client data
- [ ] Test credential loading from environment
- [ ] Document required API access for team members

### Client Project Security

When creating client projects:
- Each client gets isolated project directory
- Client-specific data stays in project folder
- Use separate repositories for client work
- Never commit client data to template repository

### Emergency Response

If credentials are accidentally committed:
1. Immediately rotate all exposed credentials
2. Remove from git history using `git filter-branch` or BFG Repo-Cleaner
3. Force push to overwrite remote repository
4. Update all team members with new credentials

---
**Remember: This is a template system. Real client work should use separate, isolated repositories.**