# Implementation Plan: RAG Chatbot Integration for Docusaurus Book

**Branch**: `001-rag-chatbot-integration` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-rag-chatbot-integration/spec.md`

## Summary

Integrate a RAG-powered chatbot into the existing Docusaurus book for physical AI and humanoid robotics content. The solution adds a chat UI widget that allows readers to ask questions and get contextual responses from the book content. The implementation places all UI-related files in `backend/ui_chatbot` and connects the frontend to the existing FastAPI RAG backend (agent_retriev.py + Qdrant). Key features include a floating chat widget, highlight-to-answer functionality, responsive design, and session-based chat history.

## Technical Context

**Language/Version**: Python 3.11+, JavaScript/React (via Docusaurus v3), CSS3
**Primary Dependencies**: FastAPI, Docusaurus 3.x, React 18+, qdrant-client, cohere, openai
**Storage**: Qdrant Cloud (existing), browser memory for session history
**Testing**: pytest (backend), React Testing Library (frontend), manual browser testing
**Target Platform**: Modern web browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+), desktop + mobile
**Project Type**: web (frontend + backend)
**Performance Goals**: API response <5s p95, initial widget load <500ms, minimal page load impact
**Constraints**: <500ms additional page load time, responsive design for mobile/desktop, no user authentication, session-scoped data only
**Scale/Scope**: Single book deployment, concurrent users handled by stateless design, no persistent storage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Technical Accuracy
- [x] Chatbot responses must use only book content from Qdrant (enforced by existing RAG backend)
- [x] All technical terminology must match ROS 2, Gazebo, NVIDIA Isaac, and VLA definitions in the book
- [x] Code examples in responses must reference real-world robotic principles from the book

### Clarity & Accessibility
- [x] Target intermediate-to-advanced AI/robotics learners (same as book audience)
- [x] Chat interface must maintain clarity in technical explanations
- [x] Chatbot must provide clear, actionable responses based on book content

### Architectural Consistency
- [x] Must maintain consistency with existing book structure (no modifications to book content)
- [x] Must preserve Docusaurus v3 build compatibility
- [x] Must not interfere with normal reading experience

### Quality Standards
- [x] All robotics definitions in responses must follow the book's content
- [x] Chat interface must be responsive and accessible
- [x] Code samples and technical explanations must be validated against the book

### Technical Constraints Compliance
- [x] Must compile as a Docusaurus v3 documentation website
- [x] Sidebar and navigation must remain functional
- [x] Page load time impact must be <500ms (SC-010)
- [x] Code samples compatible with target platforms (ROS 2 Humble, Isaac Sim)

### Content Constraints Compliance
- [x] Tone: instructional, expert, technical—but accessible
- [x] Must align with course structure and module progression
- [x] Must help students build the final "Autonomous Humanoid" project

**Constitution Check Status**: PASSED - All gates satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-chatbot-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── api.yaml         # OpenAPI specification for chat endpoint
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── ui_chatbot/                    # NEW: All UI-related files
│   ├── api.py                     # NEW: FastAPI chat endpoint (calls agent_retriev.py)
│   ├── components/                 # NEW: React components
│   │   ├── ChatWidget.jsx         # Floating chat icon widget
│   │   ├── ChatPanel.jsx          # Main chat interface panel
│   │   ├── MessageList.jsx        # Display messages in chat
│   │   ├── MessageInput.jsx       # User input field
│   │   └── HighlightButton.jsx    # Floating "Ask about this" button
│   ├── hooks/                     # NEW: Custom React hooks
│   │   ├── useChat.js            # Chat state management
│   │   └── useHighlight.js       # Text selection handling
│   ├── services/                   # NEW: API communication
│   │   └── chatService.js        # Backend API client
│   ├── styles/                     # NEW: CSS styles
│   │   ├── chatWidget.css         # Widget icon styling
│   │   ├── chatPanel.css          # Panel styling
│   │   └── responsive.css         # Mobile/desktop breakpoints
│   ├── utils/                      # NEW: Helper functions
│   │   ├── constants.js          # Configuration (API URL, etc.)
│   │   └── formatters.js          # Message/time formatting
│   └── README.md                  # Documentation for UI components
├── agent_retriev.py               # EXISTING: RAG agent (unchanged)
├── qdrant_data.py                 # EXISTING: Qdrant utilities (unchanged)
└── main.py                        # EXISTING: Content embedding pipeline (unchanged)

book-docusaurus/                    # EXISTING: Docusaurus book (no content changes)
├── src/
│   ├── components/
│   │   └── HomepageFeatures/      # EXISTING: Existing components
│   ├── css/
│   │   └── custom.css             # EXISTING: Custom styles
│   └── pages/
│       └── index.js               # EXISTING: Homepage
├── docs/                          # EXISTING: Book content Markdown files
├── docusaurus.config.js           # EXISTING: Docusaurus config
└── package.json                   # EXISTING: Dependencies
```

**Structure Decision**: Selected web application structure with clear separation:
- `backend/ui_chatbot/` contains all new chatbot UI files (as specified by user)
- `book-docusaurus/` remains unchanged (book is already built)
- React components in `ui_chatbot/components/` will be imported by Docusaurus via client code injection
- Backend API endpoint at `ui_chatbot/api.py` bridges frontend to existing `agent_retriev.py`
- No modifications to book content Markdown files

## Complexity Tracking

> **No complexity violations - Constitution Check passed**

## Phase 0: Outline & Research

### Technical Decisions & Research

| Decision | Rationale | Alternatives Considered |
|-----------|-----------|-------------------------|
| **FastAPI for chat endpoint** | Existing backend uses FastAPI; consistent architecture; async support; automatic OpenAPI docs | Flask (simpler, but existing codebase uses FastAPI), Express.js (would require separate Node.js backend) |
| **React components in ui_chatbot folder** | User specified single folder for UI files; keeps code organized; easier to maintain; clear separation of concerns | Components in book-docusaurus/src/components (violates user requirement to keep in backend folder) |
| **Client code injection for Docusaurus** | Docusaurus supports client code; non-invasive to book structure; standard pattern for custom widgets | Swizzling theme components (more invasive, harder to maintain), Theme customization (overkill for single widget) |
| **Fetch API for backend communication** | Native browser API; no additional dependencies; simple Promise-based; works well with async/await | Axios (more features, but unnecessary dependency), GraphQL overkill (REST is sufficient) |
| **Browser memory for chat history** | Session-scoped only (per spec); no persistence required across sessions; simplifies implementation | LocalStorage (persists across sessions - out of scope), IndexedDB (overkill for simple chat history), SessionStorage (similar to memory state) |
| **CSS variables for theming** | Easy to match Docusaurus theme; responsive design support; maintainable | Inline styles (hard to maintain), CSS-in-JS (adds build complexity) |
| **React hooks for state management** | Modern React pattern; reusable logic; easy to test | Class components (outdated), Redux (overkill for simple state), Context API (sufficient but unnecessary for this scope) |
| **Floating icon for chat widget** | Non-intrusive to reading experience; standard pattern; easy to make responsive | Fixed sidebar (takes up screen space), Modal popup (less discoverable) |
| **Highlight-to-answer via Text Selection API** | Browser native API; works across modern browsers; captures selection context | Custom selection mechanism (complex, reinventing wheel), Context menu integration (more invasive) |
| **Responsive design with CSS Grid/Flexbox** | Modern CSS; native browser support; no dependencies needed | CSS frameworks (adds weight, unnecessary), Bootstrap (overkill for single widget) |

### Technology Stack Justification

**Backend Stack:**
- **Python 3.11+**: Matches existing backend codebase; FastAPI requires Python 3.7+
- **FastAPI**: Already used in project; async support; automatic API documentation; type hints
- **qdrant-client**: Already used in `agent_retriev.py`; existing Qdrant integration
- **cohere**: Already used for embeddings in existing codebase

**Frontend Stack:**
- **React 18+**: Docusaurus uses React; modern hooks API; component reusability
- **JavaScript ES6+**: Modern browser support; async/await; Docusaurus default
- **CSS3 with Grid/Flexbox**: Responsive design; native browser support; matches Docusaurus theme system

**Integration Patterns:**
- **REST API**: POST endpoint for chat queries; JSON request/response; standard HTTP status codes
- **CORS**: Required for cross-origin requests from Docusaurus to backend; standard configuration
- **Client Code Injection**: Docusaurus clientModules to inject React components; non-invasive to book structure

### Performance Considerations

- **API Response Time**: Backend must return responses within 5 seconds (SC-001); RAG backend already optimized
- **Page Load Impact**: Chat widget must add <500ms to page load (SC-010); lazy load components if needed
- **Concurrent Requests**: Stateless design; no user sessions required; handle via FastAPI async
- **Bundle Size**: React components kept minimal; code splitting if needed for large dependencies
- **Caching**: Browser-side caching of responses not required (session-scoped only)

### Security Considerations

- **CORS Configuration**: Backend must allow requests from Docusaurus domain
- **Input Validation**: Sanitize user input before sending to RAG backend; prevent injection attacks
- **Rate Limiting**: Consider rate limiting on backend endpoint to prevent abuse
- **Error Messages**: Display user-friendly errors; don't leak internal details
- **HTTPS**: Required for secure API communication (assumption from spec)

### Accessibility Considerations

- **ARIA Labels**: All interactive elements must have proper ARIA labels for screen readers
- **Keyboard Navigation**: Full keyboard support (Tab, Enter, Escape)
- **Focus Management**: Proper focus management when chat opens/closes
- **Color Contrast**: Meet WCAG AA standards; respect user's color preferences
- **Responsive Design**: Works on desktop, tablet, and mobile devices

---

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for detailed entity definitions, relationships, and state transitions.

### API Contracts

See [contracts/api.yaml](./contracts/api.yaml) for OpenAPI specification of the chat endpoint.

### Quickstart Guide

See [quickstart.md](./quickstart.md) for getting started with development and testing.

### Agent Context Update

Updated Docusaurus React component patterns to agent context (if applicable).

---

## Phase 2: Implementation Planning

*This section will be populated by `/sp.tasks` command - NOT created by `/sp.plan`*

## Notes

### Architecture Decision Records (ADRs)

No ADRs required for this feature - decisions follow standard patterns and project conventions.

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Backend unavailability | User-friendly error messages; graceful degradation |
| Slow API responses | Loading indicators; timeout handling; clear error messaging |
| Browser compatibility issues | Test on target browsers; use standard APIs; fallbacks where needed |
| Highlight text capture edge cases | Handle edge cases; validate selection before sending; user feedback |
| Mobile responsiveness issues | Responsive CSS design; touch-optimized interactions; mobile testing |

### Success Metrics Alignment

- **SC-001** (5s response time): Backend endpoint optimized; async operations; proper error handling
- **SC-002** (90% first-attempt success): Clear UI cues; intuitive highlight-to-answer flow; helpful error messages
- **SC-003** (cross-device functionality): Responsive design; mobile testing; accessibility validation
- **SC-004** (85% relevant answers): Existing RAG backend already provides book-grounded responses
- **SC-005** (100% page visibility): Client code injection ensures widget on all pages
- **SC-006** (4/5+ satisfaction): Clean UI design; responsive interactions; helpful error handling
- **SC-007** (<2s error messages): Fast error detection; user-friendly messages; clear action steps
- **SC-008** (chat history preservation): React state management; session-scoped storage
- **SC-009** (98% highlight capture): Text Selection API testing; edge case handling
- **SC-010** (<500ms page load impact): Lazy loading; minimal dependencies; efficient rendering
