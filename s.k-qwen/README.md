# AI Employee - Silver Tier

> **Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.**

Fully functional AI assistant with Gmail, WhatsApp, and LinkedIn watchers, MCP servers, approval workflows, and scheduled tasks.

**Credentials:** `credentials.json` already configured for Gmail.

---

## 📋 Silver Tier Deliverables (Complete)

- [x] All Bronze Tier features
- [x] **Gmail Watcher** - Monitors important emails (credentials configured ✅)
- [x] **WhatsApp Watcher** - Monitors messages with keywords
- [x] **LinkedIn Watcher** - Monitors notifications and opportunities
- [x] **LinkedIn MCP** - Auto-post to LinkedIn
- [x] **Email MCP** - Send emails via Gmail API
- [x] **Human-in-the-Loop approval workflow**
- [x] **Plan.md generation** in Orchestrator
- [x] **Scheduler** - Daily/weekly briefings
- [x] **Skill documentation** for all components

---

## 📁 Vault Structure

```
AI_Employee_Vault/
├── Dashboard.md              # Main status dashboard
├── Company_Handbook.md       # Rules of engagement
├── Business_Goals.md         # Objectives and metrics
├── code/                     # All Python/Node.js code
│   ├── orchestrator.py       # Master process + Plan generation
│   ├── scheduler.py          # Scheduled tasks
│   ├── verify_bronze.py      # Verification script
│   ├── requirements.txt      # Python dependencies
│   ├── skills/               # Skill documentation
│   │   ├── gmail-watcher.md
│   │   ├── whatsapp-watcher.md
│   │   ├── linkedin-watcher.md
│   │   ├── email-mcp.md
│   │   ├── linkedin-mcp.md
│   │   ├── orchestrator.md
│   │   └── scheduler.md
│   ├── watchers/
│   │   ├── base_watcher.py
│   │   ├── filesystem_watcher.py
│   │   ├── gmail_watcher.py   ✅ credentials.json configured
│   │   ├── whatsapp_watcher.py
│   │   └── linkedin_watcher.py
│   └── mcp/
│       ├── email-mcp.js
│       ├── linkedin-mcp.js
│       └── package.json
├── Inbox/                    # Drop files here
├── Needs_Action/             # Tasks pending processing
├── Plans/                    # AI-generated plans
├── Pending_Approval/         # Awaiting human approval
├── Approved/                 # Approved actions
├── Rejected/                 # Rejected actions
├── Done/                     # Completed tasks
├── Logs/                     # Operation logs
├── Briefings/                # Daily/weekly briefings
├── Accounting/               # Financial records
└── Invoices/                 # Invoice files
```

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.13+**
2. **Node.js 18+** (for MCP servers)
3. **Claude Code**: `npm install -g @anthropic/claude-code`

### Step 1: Install Dependencies

```bash
cd AI_Employee_Vault/code
pip install -r requirements.txt
playwright install  # For WhatsApp and LinkedIn

cd mcp
npm install
```

### Step 2: Verify Setup

```bash
python verify_bronze.py
```

### Step 3: Authenticate Services

**Gmail** (credentials.json already configured):
```bash
cd AI_Employee_Vault/code
python watchers/gmail_watcher.py ../
# Browser opens - sign in with Google
```

**WhatsApp**:
```bash
python watchers/whatsapp_watcher.py ../
# Scan QR code with WhatsApp mobile app
```

**LinkedIn**:
```bash
python watchers/linkedin_watcher.py ../
# Log in to LinkedIn
```

**MCP Servers**:
```bash
cd AI_Employee_Vault/code/mcp
npm run auth:email
npm run auth:linkedin
```

### Step 4: Run the AI Employee

**Terminal 1 - Watchers:**
```bash
cd AI_Employee_Vault/code

# File System Watcher
python watchers/filesystem_watcher.py ../

# Gmail Watcher
python watchers/gmail_watcher.py ../

# WhatsApp Watcher
python watchers/whatsapp_watcher.py ../

# LinkedIn Watcher
python watchers/linkedin_watcher.py ../
```

**Terminal 2 - Orchestrator:**
```bash
cd AI_Employee_Vault/code
python orchestrator.py ../
```

**Terminal 3 - Scheduler:**
```bash
cd AI_Employee_Vault/code

# Daily briefing at 8 AM
python scheduler.py ../ daily_briefing --hour 8

# Weekly briefing on Monday
python scheduler.py ../ weekly_briefing --day monday
```

---

## 📝 Usage Examples

### Example 1: Process Email

1. Gmail Watcher detects important email → creates `Needs_Action/EMAIL_*.md`
2. Orchestrator processes with Claude Code
3. Creates plan in `Plans/`
4. If reply needed → creates `Pending_Approval/APPROVAL_*.md`
5. Human approves → Email MCP sends reply

### Example 2: WhatsApp Message

1. WhatsApp Watcher detects message with keyword → creates action file
2. Orchestrator analyzes and creates plan
3. Moves to `Done/` when complete

### Example 3: Post to LinkedIn

1. AI creates draft post
2. Creates `Pending_Approval/LINKEDIN_Post.md`
3. Human moves to `Approved/`
4. LinkedIn MCP posts automatically

### Example 4: Daily Briefing

```bash
python scheduler.py ../ daily_briefing
# Output: Briefings/Daily_Briefing_2026-02-28.md
```

---

## 🔧 Commands Reference

| Command | Purpose |
|---------|---------|
| `python watchers/filesystem_watcher.py ../` | Start file monitoring |
| `python watchers/gmail_watcher.py ../` | Start Gmail monitoring |
| `python watchers/whatsapp_watcher.py ../` | Start WhatsApp monitoring |
| `python watchers/linkedin_watcher.py ../` | Start LinkedIn monitoring |
| `python orchestrator.py ../` | Start task processing |
| `python scheduler.py ../ daily_briefing` | Generate daily briefing |
| `python scheduler.py ../ weekly_briefing` | Generate weekly briefing |
| `cd mcp && npm run start:email` | Start Email MCP |
| `cd mcp && npm run start:linkedin` | Start LinkedIn MCP |
| `python verify_bronze.py` | Verify setup |

---

## 📊 Folder Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    SILVER TIER FLOW                         │
└─────────────────────────────────────────────────────────────┘

1. Watchers detect events
   ├── Gmail → new important email
   ├── WhatsApp → message with keywords
   ├── LinkedIn → business opportunity
   └── File System → new file in Inbox
   ↓
2. Action files created in Needs_Action/
   ↓
3. Orchestrator processes
   ├── Simple task → Claude processes → Done/
   ├── Complex task → Creates Plan/ → Done/
   └── Sensitive action → Pending_Approval/
                              ↓
                    Human reviews
                              ↓
              ┌───────────────┴───────────────┐
              ↓                               ↓
         Approved/                        Rejected/
              ↓                               ↓
         Execute action                  Cancel task
              ↓                               ↓
           Done/                          Done/
```

---

## 🛠 Troubleshooting

**Claude Code not found:**
```bash
npm install -g @anthropic/claude-code
```

**Gmail authentication failed:**
- `credentials.json` is already configured
- Delete `token.json` and re-authenticate
- Check Gmail API is enabled

**WhatsApp/LinkedIn QR code not showing:**
- Delete session folder and re-authenticate
- Re-run watcher with visible browser

**Playwright errors:**
```bash
pip install -U playwright
playwright install
```

**MCP server not connecting:**
```bash
cd mcp && npm install
npm run check:email
npm run check:linkedin
```

---

## 📚 Skill Documentation

| Skill | Description |
|-------|-------------|
| [gmail-watcher](code/skills/gmail-watcher.md) | Gmail monitoring (credentials ✅) |
| [whatsapp-watcher](code/skills/whatsapp-watcher.md) | WhatsApp monitoring |
| [linkedin-watcher](code/skills/linkedin-watcher.md) | LinkedIn monitoring |
| [email-mcp](code/skills/email-mcp.md) | Send emails |
| [linkedin-mcp](code/skills/linkedin-mcp.md) | Post to LinkedIn |
| [orchestrator](code/skills/orchestrator.md) | Task processing + Plans |
| [scheduler](code/skills/scheduler.md) | Scheduled tasks |

---

## 🔐 Security

- ✅ `credentials.json` stored securely in `watchers/`
- ✅ Never commit tokens or session data
- ✅ Use environment variables for API keys
- ✅ Review `/Pending_Approval/` before approving
- ✅ Audit logs in `/Logs/`
- ✅ Rotate credentials monthly

---

## 📈 Next Steps (Gold Tier)

After mastering Silver Tier, add:
- [ ] Odoo integration (accounting)
- [ ] Facebook/Instagram integration
- [ ] Twitter (X) integration
- [ ] CEO Briefing automation
- [ ] Ralph Wiggum loop for persistence
- [ ] Error recovery and graceful degradation

---

*AI Employee v0.2 - Silver Tier Complete ✅*

**All watchers configured and ready to run!**
