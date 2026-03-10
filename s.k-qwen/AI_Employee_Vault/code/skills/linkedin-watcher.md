---
name: linkedin-watcher
description: |
  LinkedIn monitoring skill for AI Employee. Watches for notifications,
  messages, and business opportunities. Creates action files for AI processing.
  
  Use when: You want to monitor LinkedIn for business opportunities.
  Features: Persistent session, business keyword filtering, auto-posting support.
  
  ⚠️ WARNING: Be aware of LinkedIn's Terms of Service when using automation.
---

# LinkedIn Watcher Skill

Monitor LinkedIn for notifications, messages, and business opportunities.

## ⚠️ Important Warning

**Before using this skill:**
- Review LinkedIn's Terms of Service
- Automation may violate LinkedIn's policies
- Use at your own risk
- Consider using LinkedIn API for production

## Quick Start

### Step 1: Install Playwright

```bash
cd AI_Employee_Vault/code
pip install playwright
playwright install  # Install browser binaries
```

### Step 2: First Run - Authenticate

```bash
python watchers/linkedin_watcher.py ../
```

**What happens:**
1. Browser opens (visible mode)
2. LinkedIn login page displayed
3. Log in with your credentials
4. Session saved for future runs
5. Watcher starts monitoring

### Step 3: Start Monitoring

```bash
# Default: Check every 300 seconds (5 minutes)
python watchers/linkedin_watcher.py ../

# Custom interval: Check every 60 seconds
python watchers/linkedin_watcher.py ../ 60
```

### Run in Background

**Windows:**
```bash
start /B python watchers/linkedin_watcher.py ../
```

## Configuration

### Business Keywords

Notifications containing these keywords are flagged:

```python
BUSINESS_KEYWORDS = [
    'hiring', 'opportunity', 'project', 'freelance', 'contract',
    'proposal', 'partnership', 'collaboration', 'investment'
]
```

Edit in `watchers/linkedin_watcher.py` to customize.

### Notification Types Monitored

- Messages
- Connection requests
- Job postings
- Post comments/likes
- Business opportunities

### Check Interval

Default: 300 seconds (5 minutes)

```bash
# Check every minute
python watchers/linkedin_watcher.py ../ 60
```

## Output

Action files created in `Needs_Action/`:

```markdown
---
type: linkedin_message
notification_type: message
received: 2026-02-28T10:30:00Z
priority: high
url: https://www.linkedin.com/messaging
---

# LinkedIn Notification

## Notification Information
- **Type:** message
- **From:** John Doe
- **Received:** 2026-02-28T10:30:00
- **Priority:** high

## Notification Content
[Notification text...]

## Suggested Actions
- [ ] Open LinkedIn and review notification
- [ ] Respond if needed
- [ ] Update CRM or contacts
```

## Auto-Posting to LinkedIn

Use the LinkedIn MCP server to post updates:

```bash
cd AI_Employee_Vault/code/mcp
npm install
npm run auth:linkedin  # Authenticate
npm run start:linkedin  # Start MCP server
```

### Post via Claude Code

```
Use linkedin-mcp to post: "Excited to announce our new AI Employee feature!"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Not logged in | Re-run with visible browser |
| Session expired | Clear session and re-authenticate |
| No notifications | Check if account has activity |
| Browser crashes | Update: `pip install -U playwright` |

## Session Management

### Clear Session

```bash
rm -rf watchers/linkedin_session/
python watchers/linkedin_watcher.py ../
```

### Backup Session

```bash
cp -r watchers/linkedin_session/ /backup/location/
```

## Security Notes

- Session data contains authentication tokens
- Never share `linkedin_session/` folder
- Use strong password and 2FA
- Regularly review LinkedIn security settings

## Related Skills

- [gmail-watcher](gmail-watcher.md) - Gmail monitoring
- [whatsapp-watcher](whatsapp-watcher.md) - WhatsApp monitoring
- [linkedin-mcp](linkedin-mcp.md) - Post to LinkedIn
