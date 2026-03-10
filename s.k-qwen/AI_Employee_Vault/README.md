# AI Employee - Bronze Tier

> **Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.**

Bronze Tier implementation of the Personal AI Employee hackathon. File-based task processing with Claude Code integration.

---

## 📋 Bronze Tier Deliverables (Complete)

- [x] Obsidian vault with `Dashboard.md`, `Company_Handbook.md`, `Business_Goals.md`
- [x] File System Watcher (monitors `/Inbox`)
- [x] Orchestrator (processes tasks via Claude Code)
- [x] Basic folder structure: `/Inbox`, `/Needs_Action`, `/Done`, `/Plans`, `/Pending_Approval`, `/Approved`, `/Rejected`
- [x] All code inside `AI_Employee_Vault/code/`

---

## 📁 Vault Structure

```
AI_Employee_Vault/
├── Dashboard.md              # Main status dashboard
├── Company_Handbook.md       # Rules of engagement
├── Business_Goals.md         # Objectives and metrics
├── code/                     # All Python code
│   ├── orchestrator.py       # Master process
│   ├── verify_bronze.py      # Verification script
│   ├── requirements.txt      # Python dependencies
│   └── watchers/
│       ├── base_watcher.py
│       └── filesystem_watcher.py
├── Inbox/                    # Drop files here
├── Needs_Action/             # Tasks pending processing
├── Plans/                    # AI-generated plans
├── Approved/                 # Human-approved actions
├── Pending_Approval/         # Awaiting human approval
├── Rejected/                 # Rejected actions
├── Done/                     # Completed tasks
├── Logs/                     # Operation logs
├── Accounting/               # Financial records
├── Briefings/                # CEO briefings
└── Invoices/                 # Invoice files
```

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.13+**
2. **Node.js v24+ LTS**
3. **Claude Code**: `npm install -g @anthropic/claude-code`
4. **Obsidian** (optional)

### Step 1: Install Dependencies

```bash
cd AI_Employee_Vault/code
pip install -r requirements.txt
```

### Step 2: Verify Setup

```bash
cd AI_Employee_Vault/code
python verify_bronze.py
```

### Step 3: Run the AI Employee

**Terminal 1 - Watcher:**
```bash
cd AI_Employee_Vault/code
python watchers/filesystem_watcher.py ../
```

**Terminal 2 - Orchestrator:**
```bash
cd AI_Employee_Vault/code
python orchestrator.py ../
```

### Step 4: Test It

Drop a file into `AI_Employee_Vault/Inbox/` and watch it get processed to `/Done/`.

---

## 📝 Usage Examples

### Example 1: Process a Document

1. Drop file: `Inbox/my_document.pdf`
2. Watcher detects → copies to `Needs_Action/`
3. Orchestrator processes → moves to `Done/`

### Example 2: Manual Task

Create file directly in `Needs_Action/`:

```markdown
---
type: manual_task
priority: high
---

# Task: Review Q1 Budget

Please review and categorize all expenses.
```

---

## 🔧 Commands Reference

| Command | Purpose |
|---------|---------|
| `python watchers/filesystem_watcher.py ../` | Start file monitoring |
| `python orchestrator.py ../` | Start task processing |
| `python verify_bronze.py` | Verify setup |

---

## 📊 Folder Workflow

```
Inbox → Needs_Action → [Claude Code] → Done
                              ↓
                    Pending_Approval → (you: Approved) → Done
                                                       → (you: Rejected) → Rejected
```

---

## 🛠 Troubleshooting

**Claude Code not found:**
```bash
npm install -g @anthropic/claude-code
```

**Watcher not detecting files:**
- Ensure file is not hidden (no `.` prefix)
- Check watcher logs in `/Logs/`

**Orchestrator errors:**
- Check logs: `type AI_Employee_Vault\Logs\orchestrator_*.log`

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| `Company_Handbook.md` | Rules of engagement |
| `Business_Goals.md` | Objectives and metrics |
| `Dashboard.md` | Real-time status |

---

## 🔐 Security

- Never store credentials in vault
- Use environment variables for API keys
- Review `/Pending_Approval/` before approving
- Audit logs in `/Logs/`

---

*AI Employee v0.1 - Bronze Tier Complete ✅*
