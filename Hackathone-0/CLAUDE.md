# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains the implementation for a "Digital FTE" (Full-Time Equivalent) - an autonomous AI employee that proactively manages personal and business affairs. The architecture uses Claude Code as the reasoning engine, Obsidian as the memory/dashboard, Python watchers for monitoring, and MCP servers for external actions.

## Architecture

The system follows a Perception → Reasoning → Action pattern:

1. **Perception (Watchers)**: Lightweight Python scripts monitor Gmail, WhatsApp, filesystems, and other inputs
2. **Reasoning (Claude Code)**: Processes inputs and creates plans using the Obsidian vault as memory
3. **Action (MCP Servers)**: Model Context Protocol servers handle external actions like sending emails, web automation, etc.

## Key Components

### Watcher System
- BaseWatcher class provides template for all watcher implementations
- GmailWatcher monitors for unread/important emails
- WhatsAppWatcher uses Playwright for web automation
- FileSystemWatcher monitors file drops and changes

### MCP (Model Context Protocol) Servers
- Built-in filesystem MCP for vault operations
- Browser MCP for web automation (Playwright-based)
- Email MCP for Gmail integration
- Calendar MCP for scheduling
- Custom MCP servers can be added for specific integrations

### Ralph Wiggum Loop
- Persistence mechanism that keeps Claude working until tasks are complete
- Uses Stop hooks to intercept Claude's exit and re-inject prompts if tasks aren't done
- Two completion strategies: promise-based or file-movement based

## Common Commands

### Setting up the environment
```bash
# Install dependencies
pip install -r requirements.txt
npm install @anthropic/browser-mcp
```

### Starting the Playwright MCP Server
```bash
# Start server (shared browser context required for state maintenance)
npx @playwright/mcp@latest --port 8808 --shared-browser-context &

# Or use helper script
bash scripts/start-server.sh

# Stop server
bash scripts/stop-server.sh
```

### Running Watchers
```bash
# Each watcher runs as a separate process
python gmail_watcher.py
python whatsapp_watcher.py
python filesystem_watcher.py
```

### Working with MCP Client
```bash
# Navigate to a URL
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_navigate -p '{"url": "https://example.com"}'

# Get page snapshot for element references
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_snapshot -p '{}'

# Click an element (use ref from snapshot)
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_click -p '{"element": "Submit button", "ref": "e42"}'

# Type text into an element
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_type -p '{"element": "Search input", "ref": "e15", "text": "hello world", "submit": true}'
```

## Development Workflow

### File Structure
- `/Needs_Action` - Files created by watchers for Claude to process
- `/In_Progress/<agent>` - Files claimed by specific agents
- `/Pending_Approval` - Sensitive actions requiring human approval
- `/Done` - Completed tasks
- `/Briefings` - Generated CEO briefings and reports
- `/Logs` - Audit logs of all AI actions

### Security & Approval Patterns
- Sensitive actions (payments > $100, new contacts, etc.) require human approval
- Approval requests are written as markdown files in `/Pending_Approval`
- Claude creates approval files instead of executing sensitive actions directly
- Use DRY_RUN mode during development to log intended actions without execution

### Obsidian Integration
- Dashboard.md - Real-time summary of key metrics
- Company_Handbook.md - Rules of engagement and business policies
- Business_Goals.md - Quarterly objectives and metrics to track

## Important Configuration

### Claude Code MCP Configuration
```json
{
  "servers": [
    {
      "name": "email",
      "command": "node",
      "args": ["/path/to/email-mcp/index.js"],
      "env": {
        "GMAIL_CREDENTIALS": "/path/to/credentials.json"
      }
    },
    {
      "name": "browser",
      "command": "npx",
      "args": ["@anthropic/browser-mcp"],
      "env": {
        "HEADLESS": "true"
      }
    }
  ]
}
```

### Environment Variables
Never commit credentials. Use .env file (added to .gitignore):
```bash
# .env
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
BANK_API_TOKEN=your_token
WHATSAPP_SESSION_PATH=/secure/path/session
DRY_RUN=true  # Set to false for production
```

## Error Handling & Recovery

- Implement exponential backoff retry logic for transient failures
- Use watchdog processes to monitor and restart critical components
- Log all actions with timestamp, action type, parameters, and approval status
- System should degrade gracefully when components fail