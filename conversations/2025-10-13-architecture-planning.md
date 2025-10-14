# Architecture Planning Session - October 13, 2025

## Session Overview
Deep dive into Business-in-a-Box architecture, MCP Gateway integration, and multi-business directory structure planning.

---

## Part 1: Understanding the CLI.mjs File

### Discovery
- File location: `/Volumes/Samsung/mo/prod/projects/business-in-a-box/cli.mjs`
- Size: 375KB (71 lines with very long lines - one line is 65,429 characters)
- Type: Bundled/compiled JavaScript with Node.js shebang

### What It Is
A **Notion API MCP Server CLI tool** - bundled JavaScript that creates an MCP server to bridge Claude Code with Notion databases.

**Key Components:**
- Stream processing libraries (DelayedStream, CombinedStream)
- Form-data handling for multipart HTTP requests
- Comprehensive MIME type database
- HTTP client for API calls

**Expected Dependency:**
- Looks for OpenAPI spec at: `/Volumes/Samsung/mo/prod/projects/scripts/notion-openapi.json`
- Actual location: `/Volumes/Samsung/mo/infrastructure/claude-mcp/servers/notion-mcp/scripts/notion-openapi.json` (94KB)

**Database Access:**
Provides access to 5 Notion databases:
1. Projects (23abf6e5-4d3b-815a-8426-c45496d89c6d)
2. Tasks (23abf6e5-4d3b-8163-96c6-ea0a6a641ea2)
3. Notes (23bbf6e5-4d3b-81d1-beb5-e1016a65db65)
4. Videos (23cbf6e5-4d3b-8190-8664-cd3ed066e6d8)
5. Resources/PXM (23cbf6e5-4d3b-81a3-ab7e-d413450cd07b)

### The Problem
- **Not portable** - Hardcoded absolute paths
- **Single-purpose** - Compiled specifically for Notion MCP
- **Machine-specific** - Won't work when cloned to different machines
- **Not extensible** - Bundled nature prevents modification

---

## Part 2: Understanding MCP Gateway

### What is an MCP Gateway?
A **proxy server** that sits between Claude (any client) and your MCP servers. Functions like a reverse proxy or API gateway specifically for the MCP protocol.

### Without Gateway (Current State)
```
Claude Desktop → directly connects to → Notion MCP server (via config)
                → directly connects to → Filesystem MCP server (via config)
                → directly connects to → GitHub MCP server (via config)

Claude CLI Code → directly connects to → same servers? (separate config)

Different machine → ??? (needs new config, new paths)
```

### With Gateway
```
Claude Desktop     ┐
Claude CLI Code    ├─→ MCP Gateway (one endpoint) ─→ routes to ─→ Notion MCP
Any other client   ┘                                            ├─→ Filesystem MCP
                                                                 └─→ GitHub MCP
```

### What Gateway Does
1. **Single endpoint** - Claude only needs to know about ONE thing: the gateway
2. **Routing** - Gateway knows which MCP servers exist and routes requests
3. **Centralized config** - All MCP server connections defined in ONE place
4. **Client-agnostic** - Any MCP client can connect (Claude Desktop, CLI, custom tools)
5. **Location-independent** - Servers can be local, Docker, remote—gateway abstracts that

### Docker MCP Gateway (Official)
**Documentation:** https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/

**What It Is:**
- Official Docker tool (part of Docker Desktop's MCP Toolkit)
- Gateway service providing unified endpoint for multiple MCP servers
- Each MCP server runs in isolated Docker container
- Enterprise-ready with security, logging, and observability built-in

**Key Commands:**
```bash
docker mcp server enable notion        # Enables Notion MCP server
docker mcp server enable filesystem    # Enables filesystem MCP server
docker mcp client connect vscode       # Connects VS Code to gateway
docker mcp gateway run                 # Starts the gateway
```

**Installation:**
- Requires Docker Desktop with MCP Toolkit enabled
- CLI plugin goes in `~/.docker/cli-plugins/`
- Current installation verified: `docker mcp` v0.18.0 ✅

---

## Part 3: Current Infrastructure Analysis

### Directory Structure
```
/Volumes/Samsung/mo/
├── infrastructure/
│   └── claude-mcp/                    # Centralized MCP infrastructure
│       ├── servers/
│       │   ├── notion-mcp/
│       │   ├── google-apis-docs/
│       │   ├── postgres/
│       │   ├── youtube-api/
│       │   ├── reddit-api/
│       │   └── [6 more servers]
│       ├── configs/
│       │   └── active/
│       │       └── claude_desktop_config.json
│       ├── venv/                      # Python virtual environment
│       └── management scripts
└── prod/
    └── projects/
        └── business-in-a-box/
            ├── agents/
            ├── templates/
            ├── procedures/
            └── cli.mjs (the file we analyzed)
```

### Current Claude Desktop Config
```json
{
  "mcpServers": {
    "business-servers-remote": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-http-proxy@latest", "http://192.168.0.150:8089"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Volumes/Samsung/mo", "/Volumes/Samsung/mo/infrastructure/claude-mcp"]
    },
    "notion-mcp": {
      "command": "/Volumes/Samsung/mo/infrastructure/claude-mcp/servers/notion-mcp/bin/cli.mjs",
      "env": {
        "OPENAPI_MCP_HEADERS": "{\"Authorization\":\"Bearer ntn_...\",\"Notion-Version\":\"2022-06-28\"}"
      }
    },
    "google-apis-docs": {
      "command": "/Volumes/Samsung/mo/infrastructure/claude-mcp/venv/bin/python",
      "args": ["/Volumes/Samsung/mo/infrastructure/claude-mcp/servers/google-apis-docs/server.py"],
      "env": {}
    }
  }
}
```

### Current MCP Servers (11 total)
1. notion-mcp
2. google-apis-docs
3. google-trends
4. postgres
5. postgres-remote
6. youtube-api
7. reddit-api
8. sqlite-audiences
9. craw4ai-mcp-server
10. filesystem (via npm)
11. business-servers-remote (proxy)

### The Portability Problem
- All paths are absolute: `/Volumes/Samsung/mo/...`
- Infrastructure separate from projects
- Direct connection to MCP servers (no gateway)
- Cannot push to GitHub and pull down on another machine

---

## Part 4: Business Context

### Three Service Lines

**1. LocallyKnown.pro**
- **Price:** $1,995 setup
- **Deliverable:** Jekyll website on GitHub Pages
- **Features:**
  - 3-page site (Home, About, Contact)
  - Google My Business integration
  - Blog setup
  - SEO optimization
  - Free hosting via GitHub
- **Target:** Small local businesses
- **Goal:** $2,000 setup + $200/month ongoing

**2. GTMSetupService.com**
- **Pricing Tiers:**
  - Emergency fixes: $497 (24-hour)
  - Complete audit: $797 (48-72 hours)
  - Server-side setup: $1,297 (1 week)
  - Monthly monitoring: $197/month
- **Services:**
  - Google Tag Manager troubleshooting
  - GTM installation and configuration
  - Server-side GTM with Stape
  - Google Ads tracking
  - 4-layer diagnostic framework
- **Target:** E-commerce and businesses with tracking issues

**3. WordPress Support (ifixwpquickly.com)**
- **Model:** Monthly recurring revenue
- **Services:**
  - System monitoring
  - Backup management
  - Issue resolution
  - Preventative maintenance
- **Status:** Model still being defined

### Core Operations

**1. Prospecting**
- Currently: Reddit (via MCP server)
- Serves ALL 3 businesses
- Future: Need to expand channels

**2. Sales/Demonstrations**
- Need in-place demonstrations
- YouTube as sales channel

**3. Content Marketing**
- Blog posts to all 3 sites
- SEO content for Google crawling
- LLM-optimized content

**4. YouTube Content Production**
- 3 content streams needed:
  - GTM Setup tutorials
  - Jekyll + Google My Business integration
  - WordPress troubleshooting
- Must be economically automated
- One-man operation

**5. Service Delivery**
- Actual client work
- Templates and procedures needed
- Agent-assisted delivery

### Business Entity
- LLC: B&B Holdings
- Runs all 3 business lines
- Payment processing considerations (Stripe, PayPal, Square, Upwork)

---

## Part 5: Three Architecture Scenarios

### Scenario A: One Business-in-a-Box, Three Business Lines Inside

```
business-in-a-box/
├── shared/
│   ├── agents/
│   │   ├── prospecting-agent.md       # Serves all 3
│   │   ├── content-writer-agent.md    # Serves all 3
│   │   └── sales-agent.md             # Serves all 3
│   └── operations/
│       ├── reddit-prospecting/
│       └── youtube-content/
├── locallyknown-pro/
│   ├── agents/
│   │   ├── jekyll-developer-agent.md  # Specific to this service
│   │   └── seo-agent.md
│   ├── templates/
│   └── procedures/
├── gtm-setups/
│   ├── agents/
│   │   ├── gtm-diagnostics-agent.md   # Specific to this service
│   │   └── stape-setup-agent.md
│   ├── templates/
│   └── procedures/
└── wordpress-support/
    ├── agents/
    │   └── wp-monitoring-agent.md     # Specific to this service
    ├── templates/
    └── procedures/
```

**Pros:**
- Everything in one place
- Easy to share resources across businesses
- One repo to clone
- Simple mental model

**Cons:**
- Gets big and complex over time
- Hard to separate if you sell/spin off one business
- All or nothing (can't share just one business line)
- Tightly coupled

### Scenario B: Business-in-a-Box as Framework, Separate Business Line Repos

```
business-in-a-box/              # The TEMPLATE (public GitHub?)
├── agents/
│   ├── prospecting-agent-template.md
│   ├── content-writer-template.md
│   └── sales-agent-template.md
├── templates/
│   ├── service-delivery/
│   └── client-onboarding/
└── docs/
    └── how-to-instantiate.md

brad-operations/                # YOUR operational hub (private)
├── shared-agents/
│   ├── prospecting-agent.md    # Configured for YOU
│   └── content-writer.md
├── reddit-prospecting/
└── youtube-production/

locallyknown-pro/               # Separate repo
├── agents/ (uses brad-operations shared)
├── site/
└── client-projects/

gtm-setups/                     # Separate repo
├── agents/
├── site/
└── procedures/

wordpress-support/              # Separate repo
├── agents/
├── site/
└── monitoring/
```

**Pros:**
- Clean separation of concerns
- Can sell/share business-in-a-box template publicly
- Each business can have its own GitHub org
- Modular (can shut down one business without affecting others)
- Template is reusable by others

**Cons:**
- More repos to manage (4-5 repos)
- Shared resources need coordination
- More complex to set up initially
- Need to understand inter-repo dependencies

### Scenario C: Brad's Command Center + Business Modules

```
brad-command-center/            # YOUR operational headquarters
├── meta-agents/
│   ├── business-orchestrator.md    # "Check all businesses"
│   ├── prospecting-coordinator.md  # Reddit for all 3
│   └── content-scheduler.md        # YouTube for all 3
├── operations/
│   ├── reddit/
│   ├── youtube/
│   └── crm/
├── businesses/
│   ├── locallyknown -> ../locallyknown-pro/
│   ├── gtm -> ../gtm-setups/
│   └── wordpress -> ../wordpress-support/
└── mcp-gateway -> ~/mcp-gateway/

locallyknown-pro/               # Can be separate or submodule
gtm-setups/                     # Can be separate or submodule
wordpress-support/              # Can be separate or submodule

business-in-a-box/              # The TEMPLATE (separate, public)
```

**Pros:**
- Mirrors how you think ("me" → "businesses")
- Central command post for operations
- Business lines are modular
- Template is separate/shareable
- Orchestration layer for cross-business operations

**Cons:**
- Most complex conceptually
- Need to understand git submodules or symlinks
- More moving parts
- Steeper learning curve

---

## Part 6: Recommended MCP Architecture

### Two-Tier System

**Tier 1: System-Level MCP Gateway (Per Machine Setup)**

Location: `~/mcp-gateway/` or `/usr/local/mcp-gateway/`

Purpose: System-wide MCP infrastructure that runs on ANY machine

```
~/mcp-gateway/
├── docker-compose.yml           # All MCP servers as containers
├── .env.template                # Template for secrets
├── .env                         # YOUR secrets (gitignored)
├── servers/
│   ├── notion/
│   │   ├── Dockerfile
│   │   └── src/
│   ├── filesystem/              # Uses Docker catalog
│   ├── google-apis/
│   │   ├── Dockerfile
│   │   └── server.py
│   └── youtube-api/
│       ├── Dockerfile
│       └── server.py
├── setup.sh                     # One-time setup script
└── README.md                    # Setup instructions
```

**Setup Flow:**
```bash
# On ANY machine (once):
git clone https://github.com/you/mcp-gateway.git ~/mcp-gateway
cd ~/mcp-gateway
cp .env.template .env           # Add your API keys
./setup.sh                      # Installs docker mcp gateway
docker-compose up -d            # Starts all MCP servers

# Configure Claude (once per machine):
docker mcp client connect claude-desktop
docker mcp client connect claude-code
```

**Tier 2: Business Projects (Portable Business Logic)**

Location: Anywhere you clone them

```
business-in-a-box/
├── agents/                      # AI agent definitions
├── templates/                   # Business templates
├── procedures/                  # Workflows
├── scripts/                     # Helper scripts
├── crm/                         # Business data
├── .env.template                # Project-specific config
└── README.md                    # "Requires mcp-gateway setup"
```

**Usage Flow:**
```bash
# On ANY machine (assumes mcp-gateway already running):
git clone https://github.com/you/business-in-a-box.git
cd business-in-a-box
# Just start working - MCP already available system-wide
```

### Why This Architecture Works

**Separation of Concerns:**
- System-level (mcp-gateway): Infrastructure, MCP servers, Docker
- Project-level (business-in-a-box): Business logic, agents, workflows

**Portability:**
- mcp-gateway: One repo, works on any machine with Docker
- business-in-a-box: Pure business logic, no infrastructure dependencies

**GitHub-Friendly:**
- Both repos can be public/private
- Clone anywhere, setup once per machine
- business-in-a-box works immediately after gateway is setup

**Machine Independence:**
```
Google Studio:
  ~/mcp-gateway/         (running)
  ~/projects/business-in-a-box/

Laptop:
  ~/mcp-gateway/         (running, same repo)
  ~/projects/business-in-a-box/  (same repo)

Desktop:
  ~/mcp-gateway/         (running, same repo)
  ~/projects/business-in-a-box/  (same repo)
```

---

## Part 7: Key Insights from Discussion

### Brad's Mental Model
```
You (Brad)
├── Shared Operations (prospecting, content, etc.)
│   └── Prospecting agent (serves all 3 businesses)
└── Business-in-a-Box (framework)
    └── Business Lines
        ├── LocallyKnown.pro
        ├── GTMSetupService.com
        └── ifixwpquickly.com
```

### Critical Observation
> "Right now, the way it works is we prospect in Reddit, and that prospecting is actually covering all three of my lines of businesses. So that prospecting agent lives above the business itself."

**This reveals:** There's a shared operational layer that needs to exist independently of individual business lines.

### Brad's Vision
- Business-in-a-Box is a **framework/template** that can run any business
- Target audience: Online businesses and freelancers wanting to get work from YouTube
- Not just for Brad - potentially a product/template others can use
- Primary business entity: B&B Holdings LLC

### The Orchestration Question
> "Maybe I need an agent that runs under the me moniker—that is my personal agent that can go out and talk to the lines of business and find out what's going on."

This suggests a meta-level that coordinates businesses - a business orchestrator concept.

---

## Part 8: Critical Questions to Answer

### Question 1: Future State
**If someone on Reddit says "I want to use your Business-in-a-Box to run MY landscaping business," what do they get?**

Options:
- A. A template they customize?
- B. Your exact setup with all 3 businesses (they delete what they don't need)?
- C. Just the agent framework (they add their own business logic)?

### Question 2: Separation of Concerns
**If you shut down WordPress Support tomorrow, what happens?**

Options:
- A. Delete a folder, everything else works fine? (Scenario B or C)
- B. It's intertwined, you'd have to refactor? (Scenario A)

### Question 3: Daily Workflow
**When you open Claude CLI in the morning, where do you start?**

Options:
- A. In a "brad-operations" folder where you run everything? (Scenario C)
- B. In whichever business you're working on that day? (Scenario B)
- C. In business-in-a-box root and navigate to sub-folders? (Scenario A)

### Question 4: The Prospecting Agent (KEY QUESTION)
**You said the prospecting agent serves all 3 businesses. When it finds a Reddit lead, what happens?**

Options:
- A. It tags it with which business line and routes it? (Needs orchestration)
- B. You manually decide which business to pursue it under?
- C. It's the same prospect for all 3 (you offer all services)?

**THIS IS THE QUESTION WE NEED TO RESEARCH**

Understanding how the prospecting agent routes/tags/qualifies leads will inform the entire directory structure decision.

---

## Part 9: Payment Processing Context

### Current Situation
- LLC: B&B Holdings
- Three business lines under one entity
- Concerns about Stripe account freezes
- Exploring alternatives: PayPal, Square, Upwork

### Stripe with Multiple Business Lines
**Facts:**
- Yes, one Stripe account can handle multiple business lines (different products/sub-merchants)
- Account freezes typically caused by:
  - Sudden large transaction volume
  - Refund disputes
  - Terms of service violations
- Risk reduction strategies:
  - Clear business description in account
  - Gradual ramp-up of volume
  - Excellent customer service (minimize disputes)
- Alternative: Separate Stripe account per business line (more administration, cleaner separation)

### Upwork as Payment Processor
- Takes 10-20% fee
- Handles payment disputes
- Acts as "insurance" against payment issues
- Trade-off: Lower margins but lower risk

---

## Part 10: Next Steps

### Immediate Priority
Research Question 4 (Prospecting Agent Routing) to understand:
- How leads are qualified for different business lines
- Whether qualification happens automatically or manually
- If one prospect can be multi-service
- What CRM/routing infrastructure is needed

### Architecture Decision Flow
```
Answer Question 4
    ↓
Determines → Shared Operations Structure
    ↓
Influences → Business Line Separation Strategy
    ↓
Informs → Final Directory Structure Choice
    ↓
Enables → Implementation Plan
```

### Technical Prerequisites
1. MCP Gateway setup (system-level)
2. Docker environment configured
3. Current MCP servers containerized
4. Claude CLI configured to use gateway

### Business Prerequisites
1. Define lead qualification criteria per business line
2. Determine CRM structure
3. Map content creation workflows
4. Define client data handling (GitHub vs. local)

---

## Part 11: Outstanding Decisions

### Architecture Choice
- Scenario A: Monolithic business-in-a-box
- Scenario B: Framework + separate business repos
- Scenario C: Command center + business modules

**Depends on:** Answer to Question 4 (prospecting agent routing)

### Repository Strategy
- Single repo vs. multiple repos
- Public template vs. private operational
- Submodules vs. separate clones

### MCP Gateway Implementation
- Option A: Use Docker MCP Gateway (official)
- Option B: Custom gateway with Docker Compose

### Business Line Independence
- Tightly coupled vs. loosely coupled
- Shared vs. isolated resources
- Ability to spin off/sell individual lines

---

## Session Status
**Phase:** Architecture discovery and planning
**Next Action:** Research prospecting agent routing patterns (Question 4)
**Blocker:** Need to understand lead qualification workflow before finalizing directory structure
**Goal:** GitHub-portable business infrastructure that works across multiple machines

---

## Technical Environment Verified
- Docker: v28.4.0 ✅
- Docker MCP Plugin: v0.18.0 ✅
- Current MCP Infrastructure: `/Volumes/Samsung/mo/infrastructure/claude-mcp/` ✅
- Active MCP Servers: 11 servers ✅
- Claude Desktop Config: Active and functional ✅

## Key Takeaway
**MCP Gateway is the #1 priority.** Everything else (directory structure, business separation) flows from having a centralized, portable MCP infrastructure that "just works" on any machine.
