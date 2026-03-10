---
name: gmail-watcher
description: |
  Gmail monitoring skill for AI Employee. Watches for new important emails
  and creates action files in Needs_Action folder for AI processing.
  
  Use when: You want to automatically process incoming Gmail messages.
  Features: OAuth2 authentication, keyword filtering, duplicate prevention.
  Credentials: credentials.json already configured.
---

# Gmail Watcher Skill

Monitor Gmail and create action files for new important emails.

## ✅ Setup Complete

Your `credentials.json` is already configured in the watchers folder.

## Quick Start

### First Run - Authenticate

```bash
cd AI_Employee_Vault/code
python watchers/gmail_watcher.py ../
```

**What happens:**
1. Browser opens automatically
2. Sign in with your Google account
3. Grant Gmail API permissions
4. `token.json` is created automatically
5. Watcher starts monitoring

### Start Monitoring

```bash
# Default: Check every 120 seconds
python watchers/gmail_watcher.py ../

# Custom interval: Check every 60 seconds
python watchers/gmail_watcher.py ../ 60
```

### Run in Background

**Windows:**
```bash
start /B python watchers/gmail_watcher.py ../
```

## Configuration

### Filter Keywords

Emails containing these keywords are flagged as important:

```python
KEYWORDS = ['urgent', 'asap', 'invoice', 'payment', 'important']
```

Edit in `watchers/gmail_watcher.py` to customize.

### Check Interval

Default: 120 seconds (2 minutes)

```bash
# Check every 30 seconds
python watchers/gmail_watcher.py ../ 30
```

## Output

Action files created in `Needs_Action/`:

```markdown
---
type: email
from: client@example.com
subject: Invoice Payment Required
received: 2026-02-28T10:30:00Z
priority: high
status: pending
---

# Email Received

## Header Information
- **From:** client@example.com
- **Subject:** Invoice Payment Required
- **Received:** 2026-02-28T10:30:00
- **Priority:** high

## Email Content
[Email snippet...]

## Suggested Actions
- [ ] Read full email in Gmail
- [ ] Reply to sender
- [ ] Forward to relevant party
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Token expired | Delete `token.json` and re-run |
| No emails detected | Check if emails are unread |
| API quota exceeded | Wait 24 hours |

## Security Notes

- `token.json` contains authentication tokens
- Never share credentials.json or token.json
- Tokens are stored in `watchers/` folder
- Rotate credentials monthly

## Related Skills

- [whatsapp-watcher](whatsapp-watcher.md) - WhatsApp monitoring
- [linkedin-watcher](linkedin-watcher.md) - LinkedIn monitoring
- [email-mcp](email-mcp.md) - Send emails
