# Stage Movement Commands for Sales Process

## STAGE PROGRESSION WORKFLOW

### Stage 1: Discovery → Response Sent
**Command:** `move-to-response-sent [prospect_id]`

**Action:**
1. Move JSON file from `prospects/reddit/09/15/` to `prospects/funnel-stages/response-sent/`
2. Update `current_stage` to "response-sent"
3. Add progression entry with date and reddit post confirmation

**Trigger:** After posting layer diagnosis response on Reddit

---

### Stage 2: Response Sent → Warm Lead
**Command:** `move-to-warm-lead [prospect_id]`

**Action:**
1. Move JSON file from `response-sent/` to `warm-lead/`
2. Update `current_stage` to "warm-lead"
3. Add progression entry noting their engagement type

**Trigger:** When prospect responds with "How do I fix this?" or similar engagement

---

### Stage 3: Warm Lead → DM Active
**Command:** `move-to-dm-active [prospect_id]`

**Action:**
1. Move JSON file from `warm-lead/` to `dm-active/`
2. Update `current_stage` to "dm-active"
3. Add progression entry with DM initiation date

**Trigger:** After sending DM invitation and starting private conversation

---

### Stage 4: DM Active → Closed
**Command:** `close-prospect [prospect_id] [won/lost] [revenue] [notes]`

**Action:**
1. Move JSON file from `dm-active/` to `closed/`
2. Update `current_stage` to "closed"
3. Set outcome status, close_date, revenue, and notes

**Trigger:** When prospect either accepts service or definitively declines

---

## QUERY COMMANDS

### Find Prospects by Stage
```bash
# All prospects needing Reddit responses
ls prospects/reddit/09/15/*.json

# All prospects awaiting follow-up
ls prospects/funnel-stages/response-sent/*.json

# All warm leads ready for DM
ls prospects/funnel-stages/warm-lead/*.json

# All active DM conversations
ls prospects/funnel-stages/dm-active/*.json
```

### Find Prospects by Scope
```bash
# All in-scope prospects ready to service
grep -l '"in_scope": true' prospects/reddit/09/15/*.json
grep -l '"in_scope": true' prospects/funnel-stages/*/*.json

# All server-GTM expansion opportunities
grep -l '"expansion_opportunity": "server-gtm"' prospects/funnel-stages/closed/*.json
```

### Pipeline Value Calculation
```bash
# Total pipeline value (all active prospects)
grep '"estimated_price"' prospects/funnel-stages/{response-sent,warm-lead,dm-active}/*.json | awk -F: '{sum += $2} END {print "Total Pipeline: $" sum}'

# Closed revenue this month
grep '"revenue"' prospects/funnel-stages/closed/*.json | awk -F: '{sum += $2} END {print "Closed Revenue: $" sum}'
```

---

## EXAMPLE STAGE PROGRESSION

**Day 1 (Discovery):**
- File: `prospects/reddit/09/15/Yo485.json`
- Stage: "discovered"
- Action: Found 98% data loss issue

**Day 1 (Response Sent):**
- Command: `move-to-response-sent Yo485`
- File: `prospects/funnel-stages/response-sent/Yo485.json`
- Stage: "response-sent"
- Action: Posted Layer 1 diagnosis on Reddit

**Day 2 (Warm Lead):**
- Command: `move-to-warm-lead Yo485`
- File: `prospects/funnel-stages/warm-lead/Yo485.json`
- Stage: "warm-lead"
- Action: They replied "How do I fix this?"

**Day 2 (DM Active):**
- Command: `move-to-dm-active Yo485`
- File: `prospects/funnel-stages/dm-active/Yo485.json`
- Stage: "dm-active"
- Action: Started DM conversation

**Day 5 (Closed Won):**
- Command: `close-prospect Yo485 won 497 "Emergency fix completed same day"`
- File: `prospects/funnel-stages/closed/Yo485.json`
- Stage: "closed"
- Revenue: $497

---

## AGENT INTEGRATION

The GTM Sales Agent will use these commands:

1. **Daily prospecting:** Creates files in `prospects/reddit/09/15/`
2. **Response posting:** Uses `move-to-response-sent` command
3. **Engagement tracking:** Uses `move-to-warm-lead` when they respond
4. **DM management:** Uses `move-to-dm-active` for conversations
5. **Close tracking:** Uses `close-prospect` for final outcomes

Each command automatically updates the JSON progression array and current_stage field.