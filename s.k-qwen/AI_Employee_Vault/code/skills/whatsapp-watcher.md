---
name: whatsapp-watcher
description: |
  WhatsApp Web monitoring skill for AI Employee. Watches for new messages
  containing important keywords and creates action files for AI processing.
  
  Use when: You want to automatically process WhatsApp messages.
  Features: Persistent session, keyword filtering, QR code authentication.
  
  ⚠️ WARNING: Be aware of WhatsApp's Terms of Service when using automation.
---

# WhatsApp Watcher Skill

Monitor WhatsApp Web and create action files for important messages.

## ⚠️ Important Warning

**Before using this skill:**
- Review WhatsApp's Terms of Service
- Automation may violate WhatsApp's policies
- Use at your own risk
- Consider using WhatsApp Business API for production

## Quick Start

### Step 1: Install Playwright

```bash
cd AI_Employee_Vault/code
pip install playwright
playwright install  # Install browser binaries
```

### Step 2: First Run - Authenticate

```bash
python watchers/whatsapp_watcher.py ../
```

**What happens:**
1. Browser opens (visible mode)
2. QR code displayed on screen
3. Scan with WhatsApp mobile app:
   - Open WhatsApp on phone
   - Settings → Linked Devices
   - Link a Device
   - Scan QR code
4. Session saved for future runs

### Step 3: Start Monitoring

```bash
# Default: Check every 30 seconds
python watchers/whatsapp_watcher.py ../

# Custom interval: Check every 60 seconds
python watchers/whatsapp_watcher.py ../ 60
```

### Run in Background

**Windows:**
```bash
start /B python watchers/whatsapp_watcher.py ../
```

## Configuration

### Filter Keywords

Messages containing these keywords are flagged:

```python
KEYWORDS = ['urgent', 'asap', 'invoice', 'payment', 'help',
            'important', 'deadline', 'call', 'meeting', 'money']
```

Edit in `watchers/whatsapp_watcher.py` to customize.

### Session Path

Default: `AI_Employee_Vault/code/watchers/whatsapp_session/`

## Output

Action files created in `Needs_Action/`:

```markdown
---
type: whatsapp_message
from: +1234567890
received: 2026-02-28T10:30:00Z
priority: high
keywords: urgent, invoice
---

# WhatsApp Message Received

## Message Information
- **From:** +1234567890
- **Received:** 2026-02-28T10:30:00
- **Priority:** high
- **Keywords:** urgent, invoice

## Message Content
[Message text...]

## Suggested Actions
- [ ] Open WhatsApp and read full message
- [ ] Reply to sender
- [ ] Take appropriate action
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| QR code not showing | Clear session folder and re-authenticate |
| Session expired | Re-run authentication |
| No messages detected | Check keyword filters |
| Browser crashes | Update: `pip install -U playwright` |

## Session Management

### Clear Session

```bash
rm -rf watchers/whatsapp_session/
python watchers/whatsapp_watcher.py ../
```

### Backup Session

```bash
# Copy session folder to backup location
cp -r watchers/whatsapp_session/ /backup/location/
```

## Security Notes

- Session data contains authentication tokens
- Never share `whatsapp_session/` folder
- Store session data securely
- Regularly re-authenticate for security

## Related Skills

- [gmail-watcher](gmail-watcher.md) - Gmail monitoring
- [linkedin-watcher](linkedin-watcher.md) - LinkedIn monitoring
- [orchestrator](orchestrator.md) - Task processing
