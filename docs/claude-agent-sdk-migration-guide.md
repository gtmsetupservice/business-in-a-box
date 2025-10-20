# Claude Agent SDK Migration Guide

**Status**: Ready for implementation (no current SDK usage)
**Last Updated**: 2025-10-21
**Target SDK Version**: `@anthropic-ai/claude-agent-sdk@0.1.0` or `claude-agent-sdk@0.1.0`

---

## Overview

This guide documents how to migrate from Claude Code SDK to Claude Agent SDK for future automation scripts in this project. Currently, **no migration is required** as the project doesn't use the SDK yet.

## Key Changes (SDK v0.0.x → v0.1.0)

### Package Names

| Language | Old Package | New Package |
|----------|-------------|-------------|
| **TypeScript/JavaScript** | `@anthropic-ai/claude-code` | `@anthropic-ai/claude-agent-sdk` |
| **Python** | `claude-code-sdk` | `claude-agent-sdk` |

### Breaking Changes

1. **System Prompt No Longer Default**
   - Old: Used Claude Code's system prompt automatically
   - New: Empty system prompt by default
   - Must explicitly request: `systemPrompt: { type: "preset", preset: "claude_code" }`

2. **Settings Sources Not Loaded by Default**
   - Old: Automatically loaded from `~/.claude/settings.json`, `.claude/settings.json`, etc.
   - New: No filesystem settings loaded
   - Must explicitly specify: `settingSources: ["user", "project", "local"]`

3. **Python Type Rename**
   - Old: `ClaudeCodeOptions`
   - New: `ClaudeAgentOptions`

## When to Use the SDK in This Project

### Good Use Cases

1. **Agent Automation Scripts**
   - Prospecting agent automation (`agents/*.md`)
   - Content generation workflows
   - CRM data analysis

2. **Custom Tools**
   - Jekyll deployment automation (beyond the skill)
   - Form submission processing
   - Analytics data extraction

3. **MCP Server Integration**
   - Custom MCP servers for business logic
   - Tool coordination across multiple services

### Avoid SDK For

- Static site builds (use Jekyll directly)
- Simple shell scripts (use bash)
- One-off tasks (use CLI directly)

## Installation Guide

### TypeScript/JavaScript

```bash
# Install SDK
npm install @anthropic-ai/claude-agent-sdk

# Create tsconfig.json (if needed)
cat > tsconfig.json <<EOF
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "esModuleInterop": true,
    "strict": true,
    "skipLibCheck": true
  }
}
EOF
```

### Python

```bash
# Install SDK
pip install claude-agent-sdk

# Add to requirements.txt
echo "claude-agent-sdk>=0.1.0" >> requirements.txt
```

## Example: Prospecting Agent Automation

### TypeScript

```typescript
// scripts/automate-prospecting.ts
import { query, ClaudeAgentOptions } from "@anthropic-ai/claude-agent-sdk";

async function automateProspecting(agentFile: string) {
  const options: ClaudeAgentOptions = {
    model: "claude-sonnet-4-5",
    systemPrompt: {
      type: "preset",
      preset: "claude_code"  // Use Claude Code preset for file operations
    },
    settingSources: ["project"],  // Load project settings only
    permissionMode: "acceptEdits"
  };

  const result = await query({
    prompt: `Execute the prospecting workflow in ${agentFile}`,
    options
  });

  return result;
}

// Usage
automateProspecting("agents/gtm-sales-prospecting-agent.md");
```

### Python

```python
# scripts/automate_prospecting.py
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def automate_prospecting(agent_file: str):
    options = ClaudeAgentOptions(
        model="claude-sonnet-4-5",
        system_prompt={
            "type": "preset",
            "preset": "claude_code"  # Use Claude Code preset
        },
        setting_sources=["project"],  # Load project settings only
        permission_mode="acceptEdits"
    )

    async for message in query(
        prompt=f"Execute the prospecting workflow in {agent_file}",
        options=options
    ):
        print(message)

# Usage
asyncio.run(automate_prospecting("agents/gtm-sales-prospecting-agent.md"))
```

## Example: Content Generation Pipeline

### TypeScript

```typescript
// scripts/generate-blog-posts.ts
import { query } from "@anthropic-ai/claude-agent-sdk";

interface BlogPost {
  title: string;
  content: string;
  category: string;
}

async function generateBlogPosts(topics: string[]): Promise<BlogPost[]> {
  const posts: BlogPost[] = [];

  for (const topic of topics) {
    const result = await query({
      prompt: `Generate a GTM diagnostic blog post about: ${topic}

      Use the CRM database to validate urgency and business value.
      Follow the 4-layer diagnostic framework (Infrastructure, Implementation, Transmission, Processing).
      Include console snippets, real case studies, and business impact sections.

      Output as JSON: { title, content, category }`,
      options: {
        systemPrompt: "You are a GTM expert writing diagnostic content",
        settingSources: [],  // No filesystem settings needed
        permissionMode: "acceptEdits"
      }
    });

    // Parse result and add to posts
    posts.push(JSON.parse(result.content));
  }

  return posts;
}

// Usage
const topics = [
  "Server-side GTM timeout issues",
  "Consent Mode V2 debug mode not showing events",
  "GA4 receiving duplicate events from GTM"
];

generateBlogPosts(topics).then(posts => {
  console.log(`Generated ${posts.length} blog posts`);
});
```

## Example: MCP Server for CRM Integration

### TypeScript

```typescript
// mcp-servers/crm-intelligence.ts
import { createSdkMcpServer, tool } from "@anthropic-ai/claude-agent-sdk";
import { Client } from "pg";

// Create MCP server
const server = createSdkMcpServer();

// Tool: Analyze CRM data for content opportunities
const analyzeContentOpportunities = tool({
  name: "analyze_content_opportunities",
  description: "Analyze Reddit posts in CRM to identify high-value content topics",
  parameters: {
    type: "object",
    properties: {
      minUrgency: { type: "number", description: "Minimum urgency score (1-10)" },
      limit: { type: "number", description: "Max results to return" }
    },
    required: ["minUrgency"]
  },
  execute: async ({ minUrgency, limit = 10 }) => {
    const client = new Client({
      host: "localhost",
      port: 5432,
      user: "crm_admin",
      password: process.env.CRM_POSTGRES_PASSWORD,
      database: "crm"
    });

    await client.connect();

    const result = await client.query(`
      SELECT
        problem_category,
        COUNT(*) as frequency,
        MAX(title) as example_title,
        MAX(post_url) as example_url,
        MAX(urgency_level) as typical_urgency
      FROM reddit_posts
      WHERE urgency_level >= $1
        AND problem_category IS NOT NULL
      GROUP BY problem_category
      ORDER BY frequency DESC
      LIMIT $2
    `, [minUrgency, limit]);

    await client.end();

    return result.rows;
  }
});

// Register tool
server.registerTool(analyzeContentOpportunities);

// Start server
server.start({
  transportOptions: { type: "stdio" }
});
```

## Project-Specific Configuration

### Recommended Settings

Create `.claude/settings.json` for project-wide SDK configuration:

```json
{
  "sdk": {
    "defaultModel": "claude-sonnet-4-5",
    "defaultSystemPrompt": {
      "type": "preset",
      "preset": "claude_code"
    },
    "defaultSettingSources": ["project"],
    "defaultPermissionMode": "acceptEdits"
  },
  "mcpServers": {
    "crm-intelligence": {
      "command": "node",
      "args": ["mcp-servers/crm-intelligence.js"]
    }
  }
}
```

### Environment Variables

Add to `.env`:

```bash
# Claude API
ANTHROPIC_API_KEY=your_api_key_here

# SDK Configuration
CLAUDE_SDK_MODEL=claude-sonnet-4-5
CLAUDE_SDK_PERMISSION_MODE=acceptEdits
```

## Testing Strategy

### Unit Tests

```typescript
// tests/sdk-integration.test.ts
import { query } from "@anthropic-ai/claude-agent-sdk";

describe("Agent SDK Integration", () => {
  it("should generate blog post with correct format", async () => {
    const result = await query({
      prompt: "Generate a minimal blog post about GTM testing",
      options: {
        systemPrompt: "Return JSON only",
        settingSources: []
      }
    });

    const post = JSON.parse(result.content);
    expect(post).toHaveProperty("title");
    expect(post).toHaveProperty("content");
  });
});
```

### Integration Tests

```bash
# Test CRM MCP server
echo '{"jsonrpc": "2.0", "method": "analyze_content_opportunities", "params": {"minUrgency": 8}, "id": 1}' | \
  node mcp-servers/crm-intelligence.js
```

## Deployment Considerations

### CI/CD Integration

```yaml
# .github/workflows/run-agent-automation.yml
name: Agent Automation

on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Monday 9am

jobs:
  automate-prospecting:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm install

      - name: Run prospecting automation
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          CRM_POSTGRES_PASSWORD: ${{ secrets.CRM_POSTGRES_PASSWORD }}
        run: node scripts/automate-prospecting.js
```

### Security Best Practices

1. **API Keys**: Use environment variables, never commit
2. **Permission Mode**: Use `"ask"` in production, `"acceptEdits"` only for trusted automation
3. **Setting Sources**: Avoid `"user"` in CI/CD (use `"project"` only)
4. **System Prompts**: Be explicit; don't rely on defaults

## Troubleshooting

### Issue: SDK not using project settings

**Cause**: Forgot to specify `settingSources`
**Solution**:
```typescript
options: {
  settingSources: ["project"]  // Explicitly load project settings
}
```

### Issue: Wrong system prompt behavior

**Cause**: Expected Claude Code prompt but got empty default
**Solution**:
```typescript
options: {
  systemPrompt: { type: "preset", preset: "claude_code" }
}
```

### Issue: MCP server not found

**Cause**: Server not registered in settings.json
**Solution**: Add server to `.claude/settings.json` → `mcpServers`

## Migration Checklist

When adding SDK to this project:

- [ ] Install correct package (`@anthropic-ai/claude-agent-sdk` or `claude-agent-sdk`)
- [ ] Update imports (no `@anthropic-ai/claude-code`)
- [ ] Specify `systemPrompt` explicitly if needed
- [ ] Specify `settingSources` explicitly
- [ ] Update Python types (`ClaudeCodeOptions` → `ClaudeAgentOptions`)
- [ ] Add `.env` entries for API keys
- [ ] Test with sample query
- [ ] Document any custom tools or MCP servers
- [ ] Add CI/CD workflow if automating

## Future Enhancements

Potential SDK use cases for this project:

1. **Weekly Prospecting Automation**
   - Run GTM prospecting agent weekly via GitHub Actions
   - Auto-populate CRM with new leads

2. **Content Pipeline**
   - Generate blog drafts from CRM data
   - Auto-create posts for high-urgency topics

3. **Analytics Intelligence**
   - Query GA4 data via MCP
   - Generate weekly performance reports

4. **Form Processing**
   - Intelligent lead qualification
   - Auto-routing to appropriate service agent

---

## References

- [Agent SDK Overview](https://docs.anthropic.com/en/api/agent-sdk/overview)
- [TypeScript SDK Reference](https://docs.anthropic.com/en/api/agent-sdk/typescript)
- [Python SDK Reference](https://docs.anthropic.com/en/api/agent-sdk/python)
- [MCP Integration Guide](https://docs.anthropic.com/en/api/agent-sdk/mcp)
- [Custom Tools Guide](https://docs.anthropic.com/en/api/agent-sdk/custom-tools)

---

**Note**: This project currently uses Claude Code CLI exclusively. SDK adoption should be considered for automation workflows that benefit from programmatic control.
