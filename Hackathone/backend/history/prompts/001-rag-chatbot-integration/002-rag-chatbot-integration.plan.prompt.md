---
id: 002
title: RAG Chatbot Integration Plan
stage: plan
date: 2025-12-30
surface: agent
model: claude-sonnet-4.5-20250929
feature: 001-rag-chatbot-integration
branch: 001-rag-chatbot-integration
user: (local)
command: /sp.plan
labels: [planning, architecture, research]
links:
  spec: specs/001-rag-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-chatbot-integration/plan.md
  - specs/001-rag-chatbot-integration/research.md
  - specs/001-rag-chatbot-integration/data-model.md
  - specs/001-rag-chatbot-integration/contracts/api.yaml
  - specs/001-rag-chatbot-integration/quickstart.md
tests:
  - Constitution check (PASSED)
  - Technical context validation (PASSED)
---

## Prompt

Step 2 (Part-4)

## Goal
Plan the integration of the chatbot UI into the already created Docusaurus book.

## Focus
- The Docusaurus book (`book-docusaurus`) is already built and deployed.
- All UI-related files (JSX, Python, Markdown, or any other supporting files and folder) will be placed in a **single folder** named `ui_chatbot` inside the `backend` folder.
- Maintain a clean folder structure without scattering files across multiple locations.
- Frontend sends a POST request to `api.py` in `ui_chatbot`
- `api.py` calls `agent_retriev.py` to fetch relevant book content from Qdrant
- Create a reusable React component for the chat widget.
- Frontend displays the answer in the chat UI
- Connect the widget to the backend FastAPI endpoint.
- Test locally before deployment to ensure messages display correctly and UI is responsive
- Ensure floating icon styling, responsive window popup, and proper rendering of messages.

## Implementation (Planned)
- Folder `backend/ui_chatbot`: Place all UI-related files here, e.g., JSX components, helper Python scripts, or configuration files.
- Folder `book-docusaurus`: Keep as-is; the book is already built.
- Ensure that the UI component in `ui_chatbot` communicates with the backend `/chat` endpoint to fetch bot responses.

## Response snapshot

Created comprehensive implementation plan for RAG Chatbot integration:

**Plan File**: backend/specs/001-rag-chatbot-integration/plan.md

**Generated Artifacts (Phase 0 & 1)**:
- research.md: 12 research topics covering Docusaurus integration, React components, API design, backend integration, highlight-to-answer, responsive design, styling, error handling, accessibility, performance, CORS, and testing
- data-model.md: Complete data model with 7 entities (ChatMessage, ChatSession, HighlightSelection, ChatUIState, ChatRequest, ChatResponse, ErrorResponse), state transitions, relationships, and validation rules
- contracts/api.yaml: Full OpenAPI 3.0 specification for `/chat` and `/health` endpoints with request/response schemas and error handling
- quickstart.md: Comprehensive quickstart guide with 5-minute setup, configuration, development workflow, troubleshooting, and deployment instructions

**Key Architecture Decisions**:
1. Docusaurus clientModules for non-invasive widget injection
2. Hierarchical React component structure with custom hooks (useChat, useHighlight)
3. RESTful POST endpoint bridging frontend to existing RAG backend (agent_retriev.py)
4. Browser Text Selection API for highlight-to-answer functionality
5. CSS variables for theme integration with Docusaurus
6. Session-scoped state (no persistence across browser sessions)

**Constitution Check**: PASSED - All gates satisfied (technical accuracy, clarity, architectural consistency, quality standards, constraints compliance)

**Project Structure**: `backend/ui_chatbot/` contains all new files (components, hooks, services, styles, utils, api.py); `book-docusaurus/` remains unchanged

**Next Steps**: Run `/sp.tasks` to generate testable implementation tasks

## Outcome

- ✅ Impact: Created complete implementation plan with all Phase 0 (research) and Phase 1 (design) artifacts
- 🧪 Tests: Constitution check and technical validation (PASSED)
- 📁 Files: plan.md, research.md, data-model.md, contracts/api.yaml, quickstart.md
- 🔁 Next prompts: Run `/sp.tasks` to generate task breakdown
- 🧠 Reflection: Successfully researched and documented all technical decisions with rationale. All user requirements addressed with practical implementation patterns. Architecture decisions follow standard Docusaurus and React best practices.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution check - PASS, Technical context validation - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to task planning with `/sp.tasks`
