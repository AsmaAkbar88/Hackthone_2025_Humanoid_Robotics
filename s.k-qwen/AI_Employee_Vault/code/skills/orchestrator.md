---
name: orchestrator
description: |
  Master orchestrator process for AI Employee. Monitors Needs_Action folder,
  triggers Claude Code for task processing, manages approval workflow, and
  handles task completion.
  
  Use when: You want to automatically process tasks from watchers.
  Features: Claude Code integration, approval workflow, plan generation.
---

# Orchestrator

Master process that coordinates AI Employee operations.

## Quick Start

```bash
cd AI_Employee_Vault/code
python orchestrator.py ../
```

## Usage

### Basic Usage

```bash
# Default configuration
python orchestrator.py ../

# Custom Claude command
python orchestrator.py ../ --claude-command "claude --model claude-3-5-sonnet"

# Custom poll interval (60 seconds)
python orchestrator.py ../ --poll-interval 60
```

### Run in Background

**Windows:**
```bash
start /B python orchestrator.py ../
```

**Linux/Mac:**
```bash
python orchestrator.py ../ &
```

## Features

### 1. Task Processing

Automatically processes files in `Needs_Action/`:
- Reads task content
- Sends to Claude Code for analysis
- Creates plans in `Plans/`
- Moves completed tasks to `Done/`

### 2. Approval Workflow

Detects sensitive actions and creates approval requests:

**Triggers:**
- Send email/message
- Payment/transfer
- Delete/remove actions
- Subscription cancellations

**Flow:**
```
Needs_Action/task.md 
  → Pending_Approval/APPROVAL_task.md 
  → (Human: move to Approved/) 
  → Done/
```

### 3. Plan Generation

Creates structured plans for complex tasks:

```markdown
---
type: plan
source_task: task.md
created: 2026-02-28T10:00:00Z
status: in_progress
---

# Plan: Process Client Invoice

## Objective
Generate and send invoice to client

## Steps
- [ ] Identify client details
- [ ] Calculate amount
- [ ] Generate invoice PDF
- [ ] Send via email
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAUDE_COMMAND` | `claude` | Claude Code command |
| `VAULT_PATH` | Current | Vault path |

### Poll Interval

Default: 30 seconds

```bash
python orchestrator.py ../ --poll-interval 60
```

## Folder Structure

```
AI_Employee_Vault/
├── Needs_Action/      # Tasks to process
├── Plans/             # Generated plans
├── Pending_Approval/  # Awaiting approval
├── Approved/          # Approved actions
├── Rejected/          # Rejected actions
├── Done/              # Completed tasks
└── Logs/              # Operation logs
```

## Logs

### Orchestrator Log

Location: `Logs/orchestrator_YYYY-MM-DD.log`

```
2026-02-28 10:00:00 - Orchestrator - INFO - Processing task: EMAIL_client.md
2026-02-28 10:00:05 - Orchestrator - INFO - Claude output: Task analyzed...
2026-02-28 10:00:06 - Orchestrator - INFO - Created plan: PLAN_EMAIL_client.md
2026-02-28 10:00:07 - Orchestrator - INFO - Moved to Done: EMAIL_client.md
```

### Daily Operations Log

Location: `Logs/YYYY-MM-DD.json`

```json
[
  {
    "timestamp": "2026-02-28T10:00:00Z",
    "operation": "task_processed",
    "details": {"task": "EMAIL_client.md", "result": "success"}
  }
]
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Claude not found | `npm install -g @anthropic/claude-code` |
| Task not processing | Check logs in `Logs/` folder |
| Approval not working | Verify approval keywords in code |
| High CPU usage | Increase poll interval |

## Integration

### With Watchers

```bash
# Terminal 1: Start watcher
python watchers/filesystem_watcher.py ../

# Terminal 2: Start orchestrator
python orchestrator.py ../
```

### With Scheduler

```bash
# Daily briefing at 8 AM
python scheduler.py ../ daily_briefing --hour 8

# Weekly briefing on Monday
python scheduler.py ../ weekly_briefing --day monday
```

## Related Skills

- [gmail-watcher](gmail-watcher.md) - Gmail monitoring
- [whatsapp-watcher](whatsapp-watcher.md) - WhatsApp monitoring
- [scheduler](scheduler.md) - Scheduled tasks
- [email-mcp](email-mcp.md) - Send emails
