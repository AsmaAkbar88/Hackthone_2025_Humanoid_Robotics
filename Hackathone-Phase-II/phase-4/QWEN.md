# gemini Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-08

## Active Technologies

- Python 3.11 (backend), TypeScript/React 19 (frontend) + FastAPI, OpenAI Agents SDK, MCP SDK, SQLModel, Neon PostgreSQL, Next.js, ChatKit (006-ai-chatbot-interface)

## Project Structure

```text
backend/
frontend/
tests/
```

## Commands

cd src; pytest; ruff check .

## Code Style

Python 3.11 (backend), TypeScript/React 19 (frontend): Follow standard conventions

## Recent Changes

- 006-ai-chatbot-interface: Added Python 3.11 (backend), TypeScript/React 19 (frontend) + FastAPI, OpenAI Agents SDK, MCP SDK, SQLModel, Neon PostgreSQL, Next.js, ChatKit

<!-- MANUAL ADDITIONS START -->
## Project Completion Status

✅ **Project completed successfully!**

### Key Accomplishments:
- Fixed frontend loading issue that was causing 15-minute delays
- Backend server is now running properly on port 8000
- Implemented timeout mechanism in AuthContext to prevent indefinite loading
- Added LoadingSpinner component for better UX
- Updated main branch with all changes

### Issue Resolution:
The frontend was hanging due to the backend server not running and the authentication context waiting indefinitely for a response. This has been resolved by:
1. Starting the backend server
2. Adding a 5-second timeout to the authentication check
3. Improving error handling

<!-- MANUAL ADDITIONS END -->
