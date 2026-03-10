---
name: email-mcp
description: |
  Email MCP Server for AI Employee. Send, draft, and search emails via Gmail API.
  Integrates with Claude Code for automated email operations with human approval.
  
  Use when: You need to send emails or create drafts from your AI Employee.
  Features: OAuth2 authentication, draft mode, dry-run support.
---

# Email MCP Server

Send and manage emails via Gmail API with MCP protocol.

## Setup

### 1. Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create/select project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `credentials.json`

### 2. Install Dependencies

```bash
cd AI_Employee_Vault/code/mcp
npm install
```

### 3. Authenticate

```bash
cd AI_Employee_Vault/code/mcp
npm run auth
```

Follow the OAuth flow to authorize.

### 4. Configure Claude Code

Add to `~/.config/claude-code/mcp.json`:

```json
{
  "servers": [
    {
      "name": "email",
      "command": "node",
      "args": ["/path/to/AI_Employee_Vault/code/mcp/email-mcp.js"],
      "env": {
        "GMAIL_CREDENTIALS": "/path/to/credentials.json",
        "GMAIL_USER": "your-email@gmail.com",
        "DRY_RUN": "false"
      }
    }
  ]
}
```

## Usage

### Start Server

```bash
cd AI_Employee_Vault/code/mcp
npm start
```

### Check Status

```bash
npm run check
```

## Available Tools

### `send_email`

Send an email via Gmail.

**Parameters:**
- `to` (required): Recipient email address
- `subject` (required): Email subject
- `body` (required): Email body text
- `cc`: CC recipients
- `bcc`: BCC recipients
- `attachments`: Files to attach

**Example:**
```json
{
  "to": "client@example.com",
  "subject": "Invoice #123",
  "body": "Please find attached your invoice.",
  "cc": "accounting@example.com"
}
```

### `create_draft`

Create a draft email without sending (safe for review).

**Parameters:**
- `to` (required): Recipient email
- `subject` (required): Email subject
- `body` (required): Email body
- `cc`: CC recipients

**Example:**
```json
{
  "to": "client@example.com",
  "subject": "Proposal Draft",
  "body": "Here is the proposal we discussed..."
}
```

### `search_emails`

Search Gmail for emails matching a query.

**Parameters:**
- `query` (required): Gmail search query
- `maxResults`: Maximum results (default: 10)

**Example:**
```json
{
  "query": "from:boss is:unread",
  "maxResults": 5
}
```

## Dry Run Mode

For testing, set `DRY_RUN=true`:

```bash
DRY_RUN=true npm start
```

Emails will be logged but not sent.

## Human-in-the-Loop Pattern

For sensitive actions, use this workflow:

1. **AI creates draft:**
   ```
   Claude → create_draft → Draft saved in Gmail
   ```

2. **AI creates approval request:**
   ```
   /Pending_Approval/EMAIL_Send_to_Client.md
   ```

3. **Human reviews and approves:**
   - Move file to `/Approved/`

4. **Orchestrator sends email:**
   ```
   Approved → send_email → Email sent
   ```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Token expired | Run `npm run auth` to re-authenticate |
| 401 Unauthorized | Check credentials and token files |
| Email not sending | Check `DRY_RUN` environment variable |
| MCP connection failed | Verify path in Claude Code config |

## Security Notes

- Never commit `token.json` or `credentials.json`
- Use environment variables for sensitive data
- Enable 2FA on Google account
- Review sent emails regularly

## Related Skills

- [gmail-watcher](gmail-watcher.md) - Gmail monitoring
- [orchestrator](orchestrator.md) - Task processing
- [approval-workflow](approval-workflow.md) - HITL pattern
