---
name: scheduler
description: |
  Scheduled task helper for AI Employee. Generate daily briefings, weekly CEO
  reports, and process pending tasks on a schedule.
  
  Use when: You want automated periodic reports and task processing.
  Features: Daily briefings, weekly CEO reports, cron-like scheduling.
---

# Scheduler

Scheduled task automation for AI Employee.

## Quick Start

```bash
cd AI_Employee_Vault/code
python scheduler.py ../ daily_briefing
```

## Usage

### Daily Briefing

Generate a daily summary of completed and pending tasks:

```bash
# Generate now
python scheduler.py ../ daily_briefing

# Generate for 8 AM
python scheduler.py ../ daily_briefing --hour 8
```

**Output:** `Briefings/Daily_Briefing_YYYY-MM-DD.md`

### Weekly CEO Briefing

Generate comprehensive weekly report:

```bash
# Generate now
python scheduler.py ../ weekly_briefing

# Generate for Monday 7 AM
python scheduler.py ../ weekly_briefing --day monday --hour 7
```

**Output:** `Briefings/Weekly_Briefing_YYYY-MM-DD.md`

### Process Pending Tasks

Process all tasks in Needs_Action folder:

```bash
python scheduler.py ../ process_pending
```

## Scheduled Tasks (Windows Task Scheduler)

### Daily Briefing at 8 AM

1. Open Task Scheduler
2. Create Basic Task
3. Name: "AI Employee Daily Briefing"
4. Trigger: Daily at 8:00 AM
5. Action: Start a program
6. Program: `python`
7. Arguments: `scheduler.py ../ daily_briefing`
8. Start in: `E:\Hackathon\Hackthone_2025_Humanoid_Robotics\s.k-qwen\AI_Employee_Vault\code`

### Weekly Briefing on Monday 7 AM

Same as above, but:
- Trigger: Weekly on Monday at 7:00 AM
- Arguments: `scheduler.py ../ weekly_briefing --day monday`

## Scheduled Tasks (Linux/Mac cron)

Edit crontab:
```bash
crontab -e
```

Add entries:
```cron
# Daily briefing at 8 AM
0 8 * * * cd /path/to/AI_Employee_Vault/code && python scheduler.py ../ daily_briefing

# Weekly briefing on Monday at 7 AM
0 7 * * MON cd /path/to/AI_Employee_Vault/code && python scheduler.py ../ weekly_briefing
```

## Output Formats

### Daily Briefing

```markdown
---
type: daily_briefing
date: 2026-02-28
generated: 2026-02-28T08:00:00Z
---

# Daily Briefing - Friday, February 28, 2026

## Summary
Generated at 08:00 AM

---

## Completed Tasks (Last 24 Hours)
- [ ] EMAIL_client_invoice.md (2026-02-27 14:30)
- [ ] FILE_DROP_report.pdf (2026-02-27 10:15)

---

## Pending Tasks
- [ ] WHATSAPP_urgent_message.md (2026-02-28 07:45)

---

## Today's Focus
*Add your focus areas for today.*
```

### Weekly CEO Briefing

```markdown
---
type: weekly_briefing
date: 2026-02-28
period_start: 2026-02-21
period_end: 2026-02-28
---

# Weekly CEO Briefing

## Executive Summary

| Metric | Value |
|--------|-------|
| Tasks Completed | 15 |
| Tasks Pending | 3 |
| Completion Rate | 83% |

---

## Proactive Suggestions

### Cost Optimization
- Notion: No activity in 45 days. Cost: $15/month.

### Upcoming Deadlines
- Project Alpha: March 15 (15 days)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No tasks in briefing | Check if Done folder has files |
| Scheduler not running | Verify cron/Task Scheduler config |
| Empty briefing | Ensure tasks were completed in date range |

## Related Skills

- [orchestrator](orchestrator.md) - Task processing
- [gmail-watcher](gmail-watcher.md) - Gmail monitoring
- [whatsapp-watcher](whatsapp-watcher.md) - WhatsApp monitoring
