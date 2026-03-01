# QWEN.md - Project Context

## Project Overview

This directory (`s.k-qwen`) is a **Qwen Skill Package** for browser automation, part of the larger **Hackathon 2025: Humanoid Robotics / Personal AI Employee** initiative. It provides an integrated skill for automating web browsing tasks using the **Playwright MCP (Model Context Protocol)** server.

The skill enables AI agents to:
- Navigate websites and fill forms
- Click elements and interact with UI components
- Take screenshots and extract data
- Perform complex multi-step browser automation

This is one building block of a larger "Digital FTE" (Full-Time Equivalent) system—an autonomous AI employee that manages personal and business affairs 24/7.

---

## Directory Structure

```
s.k-qwen/
├── hackathone-0.md              # Main hackathon blueprint (1200+ lines)
├── QWEN.md                      # This file - project context
└── .qwen/
    └── skills/
        └── browsing-with-playwright/
            ├── SKILL.md                     # Skill documentation & quick reference
            ├── references/
            │   └── playwright-tools.md      # Complete MCP tool schema reference
            └── scripts/
                ├── mcp-client.py            # Universal MCP client (HTTP + stdio)
                ├── start-server.sh          # Start Playwright MCP server
                ├── stop-server.sh           # Stop server gracefully
                └── verify.py                # Server health check
```

---

## Key Files

| File | Purpose |
|------|---------|
| `hackathone-0.md` | Comprehensive hackathon guide for building a "Personal AI Employee" with Claude Code + Obsidian + MCP servers |
| `SKILL.md` | Quick-start guide for browser automation skill |
| `mcp-client.py` | Universal MCP client supporting HTTP and stdio transports |
| `playwright-tools.md` | Reference documentation for all 22 Playwright MCP tools |

---

## Building and Running

### Prerequisites

- **Node.js** v24+ LTS
- **Python** 3.13+
- **Playwright** browsers installed

### Server Lifecycle

#### Start the Playwright MCP Server
```bash
# Using helper script (recommended)
bash scripts/start-server.sh

# Or manually
npx @playwright/mcp@latest --port 8808 --shared-browser-context &
```

#### Verify Server is Running
```bash
python scripts/verify.py
# Expected: ✓ Playwright MCP server running
```

#### Stop the Server
```bash
# Using helper script (closes browser first)
bash scripts/stop-server.sh

# Or manually
python scripts/mcp-client.py call -u http://localhost:8808 -t browser_close -p '{}'
pkill -f "@playwright/mcp"
```

---

## Usage Examples

### Basic Navigation
```bash
# Navigate to URL
python scripts/mcp-client.py call -u http://localhost:8808 -t browser_navigate \
  -p '{"url": "https://example.com"}'

# Get page snapshot (accessibility tree with element refs)
python scripts/mcp-client.py call -u http://localhost:8808 -t browser_snapshot -p '{}'
```

### Form Interaction
```bash
# Type into input field
python scripts/mcp-client.py call -u http://localhost:8808 -t browser_type \
  -p '{"element": "Search input", "ref": "e15", "text": "hello world", "submit": true}'

# Fill multiple form fields
python scripts/mcp-client.py call -u http://localhost:8808 -t browser_fill_form \
  -p '{"fields": [{"ref": "e10", "value": "john@example.com"}, {"ref": "e12", "value": "password123"}]}'
```

### Complex Multi-Step Operations
```bash
# Run atomic Playwright code
python scripts/mcp-client.py call -u http://localhost:8808 -t browser_run_code \
  -p '{"code": "async (page) => { await page.goto(\"https://example.com\"); await page.click(\"text=Learn more\"); return await page.title(); }"}'
```

### List Available Tools
```bash
python scripts/mcp-client.py list -u http://localhost:8808
```

---

## Available MCP Tools (22 total)

| Category | Tools |
|----------|-------|
| **Navigation** | `browser_navigate`, `browser_navigate_back`, `browser_tabs` |
| **Snapshot** | `browser_snapshot`, `browser_take_screenshot` |
| **Interaction** | `browser_click`, `browser_type`, `browser_fill_form`, `browser_hover`, `browser_drag` |
| **Forms** | `browser_select_option`, `browser_file_upload`, `browser_press_key` |
| **Wait/Condition** | `browser_wait_for`, `browser_handle_dialog` |
| **Advanced** | `browser_evaluate`, `browser_run_code`, `browser_console_messages`, `browser_network_requests` |
| **Utility** | `browser_close`, `browser_resize`, `browser_install` |

See `references/playwright-tools.md` for complete schema documentation.

---

## Development Conventions

### Coding Style
- Python scripts use type hints and docstrings
- Shell scripts follow POSIX conventions
- MCP client supports both HTTP and stdio transports

### Testing Practices
- Use `verify.py` to check server health before operations
- Handle errors gracefully with proper exit codes
- Server lifecycle scripts manage PID files for clean restarts

### Important Notes
- The `--shared-browser-context` flag is **required** to maintain browser state across multiple calls
- Always stop the server gracefully using `stop-server.sh` (closes browser first)
- Element references (`ref`) come from `browser_snapshot` output

---

## Integration with Larger Hackathon

This skill is part of the **Personal AI Employee** architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    Personal AI Employee                      │
├─────────────────────────────────────────────────────────────┤
│  Perception (Watchers)  →  Reasoning (Claude Code)  →  Action │
│  - Gmail Watcher        →  - Read tasks           →  MCP Servers │
│  - WhatsApp Watcher     →  - Create plans         →  - Browser (this skill) │
│  - File Watcher         →  - Ralph Wiggum loop    →  - Email │
│                         →                         →  - Odoo (accounting) │
└─────────────────────────────────────────────────────────────┘
```

**Related Documentation:**
- `hackathone-0.md` - Full architectural blueprint
- Tiered deliverables: Bronze → Silver → Gold → Platinum
- "Monday Morning CEO Briefing" feature for autonomous business audits

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server not responding | Run `bash scripts/stop-server.sh && bash scripts/start-server.sh` |
| Element not found | Run `browser_snapshot` first to get current refs |
| Click fails | Try `browser_hover` first, then click |
| Verification fails | Check process: `pgrep -f "@playwright/mcp"` |

---

## Resources

- [Playwright MCP Repository](https://github.com/microsoft/playwright-mcp)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Claude Code Documentation](https://claude.com/product/claude-code)
- [Hackathon Zoom Meetings](https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1) - Wednesdays 10:00 PM
