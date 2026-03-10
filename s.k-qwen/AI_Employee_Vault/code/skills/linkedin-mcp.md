---
name: linkedin-mcp
description: |
  LinkedIn MCP Server for AI Employee. Post updates to LinkedIn automatically
  or create drafts for review. Integrates with Claude Code for automated posting.
  
  Use when: You need to post to LinkedIn from your AI Employee.
  Features: Browser automation, draft support, visibility controls.
  
  ⚠️ WARNING: Be aware of LinkedIn's Terms of Service.
---

# LinkedIn MCP Server

Post to LinkedIn via browser automation.

## ⚠️ Important Warning

- Review LinkedIn's Terms of Service
- Automation may violate LinkedIn's policies
- Use at your own risk

## Setup

### Step 1: Install Dependencies

```bash
cd AI_Employee_Vault/code/mcp
npm install
```

### Step 2: Authenticate

```bash
npm run auth:linkedin
```

**What happens:**
1. Browser opens
2. Log in to LinkedIn
3. Session saved for future uses

### Step 3: Configure Claude Code

Add to `~/.config/claude-code/mcp.json`:

```json
{
  "servers": [
    {
      "name": "linkedin",
      "command": "node",
      "args": ["/path/to/code/mcp/linkedin-mcp.js"],
      "env": {
        "LINKEDIN_SESSION_PATH": "/path/to/linkedin_session",
        "DRY_RUN": "false"
      }
    }
  ]
}
```

## Usage

### Start Server

```bash
npm run start:linkedin
```

### Check Status

```bash
npm run check:linkedin
```

## Available Tools

### `post_to_linkedin`

Post an update to LinkedIn.

**Parameters:**
- `content` (required): Post content (max 3000 characters)
- `imageUrl`: Optional image URL
- `visibility`: PUBLIC or CONNECTIONS (default: PUBLIC)

**Example:**
```json
{
  "content": "Excited to announce our new AI Employee feature!",
  "visibility": "PUBLIC"
}
```

### `create_linkedin_draft`

Create a draft post for review (safe operation).

**Parameters:**
- `content` (required): Draft content

**Example:**
```json
{
  "content": "Working on something exciting..."
}
```

### `get_linkedin_posts`

Get recent posts and analytics.

**Parameters:**
- `limit`: Number of posts (default: 5)

## Human-in-the-Loop Pattern

For safe posting, use this workflow:

1. **AI creates draft:**
   ```
   Claude → create_linkedin_draft → Draft saved
   ```

2. **AI creates approval request:**
   ```
   /Pending_Approval/LINKEDIN_Post_Draft.md
   ```

3. **Human reviews and approves:**
   - Move file to `/Approved/`

4. **Orchestrator posts:**
   ```
   Approved → post_to_linkedin → Posted
   ```

## Dry Run Mode

For testing:

```bash
DRY_RUN=true npm run start:linkedin
```

Posts will be logged but not created.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Not authenticated | Run `npm run auth:linkedin` |
| Post failed | Check session, re-authenticate |
| Browser error | Update playwright |

## Related Skills

- [linkedin-watcher](linkedin-watcher.md) - LinkedIn monitoring
- [email-mcp](email-mcp.md) - Email sending
- [orchestrator](orchestrator.md) - Task processing
