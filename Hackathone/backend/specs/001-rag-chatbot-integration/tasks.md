# Tasks: RAG Chatbot Integration for Docusaurus Book

**Input**: Design documents from `/specs/001-rag-chatbot-integration/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/api.yaml

**Tests**: Manual browser testing is required per quickstart.md. Automated tests are optional and not included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/ui_chatbot/`
- **Frontend**: `backend/ui_chatbot/components/`, `backend/ui_chatbot/hooks/`, `backend/ui_chatbot/services/`, `backend/ui_chatbot/styles/`, `backend/ui_chatbot/utils/`
- **Docusaurus**: `book-docusaurus/` (no content changes, only config)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create `backend/ui_chatbot/` directory structure with subdirectories: components/, hooks/, services/, styles/, utils/
- [X] T002 Create Python requirements file in `backend/ui_chatbot/requirements.txt` with FastAPI, pydantic, uvicorn, and python-multipart dependencies
- [X] T003 [P] Create README.md in `backend/ui_chatbot/` documenting chatbot UI components structure and purpose
- [X] T004 Create package.json in `backend/ui_chatbot/` for frontend dependencies (React hooks, date-fns for timestamp formatting)
- [X] T005 [P] Create `.env.example` in `backend/ui_chatbot/` documenting required environment variables (API_URL, API_TIMEOUT)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Implement `backend/ui_chatbot/utils/constants.js` with API_URL, API_TIMEOUT configuration, and device detection helpers
- [X] T007 [P] Implement `backend/ui_chatbot/utils/formatters.js` with message formatting, timestamp formatting, and UUID generation utilities
- [X] T008 Create `backend/ui_chatbot/api.py` FastAPI application with CORS middleware, ChatRequest/ChatResponse/ErrorResponse Pydantic models, and /health endpoint
- [X] T009 Implement `/chat` POST endpoint in `backend/ui_chatbot/api.py` that imports RAGAgent from agent_retriev.py, validates input, calls agent.query(), and returns ChatResponse
- [X] T010 Create `backend/ui_chatbot/services/chatService.js` with sendMessage() function that handles fetch API calls, AbortController for timeouts, and error handling
- [X] T011 [P] Create `backend/ui_chatbot/styles/responsive.css` with mobile (default), tablet (768px+), and desktop (1200px+) breakpoints and base styles

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Chat Interface for Book Content Queries (Priority: P1) 🎯 MVP

**Goal**: Enable readers to ask questions about book content through a chat interface and receive relevant answers grounded in book content.

**Independent Test**: User can open Docusaurus book, click floating chat icon, type a question like "What is ROS 2?", and receive a relevant answer within 5 seconds. Chat history is preserved during session.

### Implementation for User Story 1

- [X] T012 [US1] Create `backend/ui_chatbot/hooks/useChat.js` custom React hook with sendMessage(), clearChat(), toggleChat() functions, and ChatSession state (messages, isLoading, error, isOpen, unreadCount)
- [X] T013 [US1] Implement message validation in `backend/ui_chatbot/hooks/useChat.js` (min 5 chars, max 2000 chars) and error message display logic
- [X] T014 [P] [US1] Create `backend/ui_chatbot/styles/chatWidget.css` with floating icon styles (56x56px circular button, bottom-right fixed position, hover effects)
- [X] T015 [P] [US1] Create `backend/ui_chatbot/components/ChatWidgetIcon.jsx` component with button, unread badge display, and click handler to toggle chat
- [X] T016 [P] [US1] Create `backend/ui_chatbot/components/MessageList.jsx` component with message rendering (user/assistant/system roles), scroll-to-bottom logic, and message key prop for performance
- [X] T017 [P] [US1] Create `backend/ui_chatbot/components/MessageInput.jsx` component with textarea, character counter, submit button, and Enter key handling
- [X] T018 [P] [US1] Create `backend/ui_chatbot/styles/chatPanel.css` with panel styles (400x600px on desktop, 80vh full-screen on mobile), header with close button, message area, and input area
- [X] T019 [US1] Create `backend/ui_chatbot/components/ChatPanel.jsx` component with MessageList, MessageInput, loading indicator, error display, clear chat button, and responsive layout
- [X] T020 [US1] Create `backend/ui_chatbot/components/ChatWidget.jsx` root component that manages ChatUIState, integrates useChat hook, renders ChatWidgetIcon and ChatPanel, and handles open/close state
- [X] T021 [US1] Create `backend/ui_chatbot/index.js` entry point that lazy loads ChatWidget component and renders it to document.body
- [X] T022 [US1] Update `book-docusaurus/docusaurus.config.js` theme configuration to include clientModules: [require.resolve('../backend/ui_chatbot/index.js')]
- [X] T023 [US1] Verify CORS configuration in `backend/ui_chatbot/api.py` allows http://localhost:3000 for local development and https://asmaakbar88.vercel.app for production

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently (MVP complete)

---

## Phase 4: User Story 2 - Highlight-to-Answer Contextual Queries (Priority: P2)

**Goal**: Enable readers to select text on any book page and ask questions about that specific text to get contextually relevant explanations.

**Independent Test**: User can select/highlight text on any book page (5-500 characters), click floating "Ask about this" button, chat panel opens with highlighted text displayed, and user receives a relevant answer referencing selected content.

### Implementation for User Story 2

- [X] T024 [US2] Create `backend/ui_chatbot/hooks/useHighlight.js` custom React hook with event listeners (mouseup, touchend), text selection validation (5-500 chars), button position calculation using getBoundingClientRect(), and clearSelection() function
- [X] T025 [P] [US2] Create `backend/ui_chatbot/components/HighlightButton.jsx` component with floating button rendering, "Ask about this" label, click handler to open chat with highlighted text, and dynamic positioning based on useHighlight state
- [X] T026 [US2] Update `backend/ui_chatbot/hooks/useChat.js` to accept highlightedText parameter in sendMessage(), include it in ChatRequest payload as highlighted_text field, and display highlighted context as quote block in MessageList
- [X] T027 [US2] Update `backend/ui_chatbot/components/ChatWidget.jsx` root component to integrate useHighlight hook, render HighlightButton when selection is valid, and pass highlighted text to useChat when sending messages
- [X] T028 [US2] Update `backend/ui_chatbot/api.py` /chat endpoint to extract highlighted_text from ChatRequest, prepend it to query with "Context: {highlighted_text}\n\nQuestion: {query}" format before calling RAGAgent

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Chat Interface Accessibility and Responsiveness (Priority: P3)

**Goal**: Ensure chat interface is accessible and responsive for all readers across different devices and accessibility needs.

**Independent Test**: Chat interface is fully functional on desktop, tablet, and mobile devices with proper keyboard navigation (Tab, Enter, Escape), screen reader announcements for all messages and inputs, and ARIA labels on all interactive elements.

### Implementation for User Story 3

- [X] T029 [P] [US3] Update `backend/ui_chatbot/styles/responsive.css` with refined mobile breakpoint (<768px), tablet breakpoint (768px-1199px), and desktop breakpoint (>=1200px) layouts
- [X] T030 [P] [US3] Update `backend/ui_chatbot/components/ChatWidgetIcon.jsx` with ARIA label "Open chat", keyboard support (Enter/Space to open), and focus management
- [X] T031 [P] [US3] Update `backend/ui_chatbot/components/ChatPanel.jsx` with role="dialog", aria-modal="true", close button ARIA label "Close chat", and focus trap when open
- [X] T032 [P] [US3] Update `backend/ui_chatbot/components/MessageList.jsx` with aria-live region for new messages, role="log" for message container, and proper ARIA labels for each message (role attribution)
- [X] T033 [P] [US3] Update `backend/ui_chatbot/components/MessageInput.jsx` with aria-label="Type your message", textarea with proper accessibility, and submit button with ARIA label "Send message"
- [X] T034 [P] [US3] Update `backend/ui_chatbot/components/HighlightButton.jsx` with ARIA label "Ask about selected text", keyboard support, and focus management when clicked
- [X] T035 [US3] Update `backend/ui_chatbot/hooks/useChat.js` with focus management (focus input when chat opens, return focus to icon when closes), Escape key to close chat, and Enter key to send message
- [X] T036 [US3] Update `backend/ui_chatbot/hooks/useHighlight.js` with keyboard support for text selection, Escape key to clear selection, and proper focus handling

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T037 [P] Update `backend/ui_chatbot/styles/chatWidget.css` and `chatPanel.css` to use CSS variables for theming (--chat-bg, --chat-text, --chat-primary, --chat-border, --chat-shadow)
- [X] T038 [P] Update all components (`ChatWidgetIcon.jsx`, `ChatPanel.jsx`, `MessageList.jsx`, `MessageInput.jsx`, `HighlightButton.jsx`) to inherit theme colors from Docusaurus CSS variables
- [X] T039 Add loading indicator in `backend/ui_chatbot/components/ChatPanel.jsx` (spinner or progress bar) that displays when ChatSession.isLoading is true
- [X] T040 Add error message display in `backend/ui_chatbot/components/ChatPanel.jsx` that shows ChatSession.error with user-friendly messages and retry option
- [X] T041 Implement message limit in `backend/ui_chatbot/hooks/useChat.js` (max 50 messages per session) with FIFO removal of oldest messages when limit reached
- [X] T042 [P] Create deployment documentation in `backend/ui_chatbot/README.md` with local development instructions, production deployment steps, and environment variable configuration

---

## Phase 7: Testing & Validation

**Purpose**: Manual browser testing and validation per quickstart.md

- [ ] T043 Start backend API server in `backend/ui_chatbot/` using `python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000` and verify /health endpoint returns healthy status
- [ ] T044 Start Docusaurus development server in `book-docusaurus/` using `npm run start` and verify page loads successfully
- [ ] T045 Test chat widget visibility: Open http://localhost:3000 and verify floating chat icon appears on all book pages
- [ ] T046 Test User Story 1 flow: Click chat icon, type "What is ROS 2?", submit message, verify AI response arrives within 5 seconds, verify chat history is preserved
- [ ] T047 Test User Story 2 flow: Select/highlight text on any page (5-500 chars), click "Ask about this" button, verify chat opens with highlighted text, submit related question, verify response references highlighted content
- [ ] T048 Test responsive design: Resize browser window to mobile (<768px), tablet (768px-1199px), and desktop (>=1200px) viewports and verify chat layout adapts correctly
- [ ] T049 Test keyboard navigation: Use Tab, Enter, and Escape keys to navigate chat interface, verify all interactive elements are accessible
- [ ] T050 Test error handling: Stop backend API server, try sending a message, verify user-friendly error message displays with retry option
- [ ] T051 Test empty input validation: Try sending empty message, verify submission is blocked with "Query must be at least 5 characters" prompt
- [ ] T052 Test clear chat functionality: Send multiple messages, click "Clear Chat" button, verify all messages are removed and state is reset
- [ ] T053 Test highlight validation: Select 3 characters (<5), verify "Ask about this" button does not appear; select 600 characters (>500), verify button appears with warning or is disabled
- [ ] T054 Run quickstart.md validation: Follow all steps in quickstart.md to ensure local development setup works correctly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational completion - No dependencies on other stories
- **User Story 2 (Phase 4)**: Depends on Foundational + User Story 1 completion - Integrates with ChatWidget from US1
- **User Story 3 (Phase 5)**: Depends on Foundational + US1 + US2 completion - Accessibility enhancements to existing components
- **Polish (Phase 6)**: Depends on all desired user stories being complete
- **Testing (Phase 7)**: Depends on Docusaurus Integration completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on Foundational + User Story 1 - Integrates with ChatWidget but adds independent functionality
- **User Story 3 (P3)**: Depends on Foundational + US1 + US2 - Accessibility improvements to all existing components

### Within Each User Story

- Utilities before components
- Hooks before components that depend on them
- Component styles before component implementations
- Parent components after child components
- Integration after individual components

### Parallel Opportunities

**Phase 1 - Setup**:
- T003, T004, T005 can run in parallel

**Phase 2 - Foundational**:
- T006, T007 can run in parallel

**Phase 3 - User Story 1**:
- T014, T015, T016, T017 can run in parallel (after T012-T013 complete)
- T018 can run in parallel to T014-T017 (after T012-T013 complete)

**Phase 4 - User Story 2**:
- T025 can run in parallel to T026-T028 (after T024 complete)

**Phase 5 - User Story 3**:
- T029, T030, T031, T032, T033, T034 can all run in parallel
- T035, T036 can run in parallel

**Phase 6 - Polish**:
- T037, T038 can run in parallel

**Phase 7 - Testing**:
- T045-T054 can be run in any order (manual testing checklist)

---

## Parallel Example: User Story 1

```bash
# After completing T012 and T013, launch these tasks in parallel:
# Task T014: Create chatWidget.css
# Task T015: Create ChatWidgetIcon.jsx
# Task T016: Create MessageList.jsx
# Task T017: Create MessageInput.jsx

# After T014-T017 complete, launch these in parallel:
# Task T018: Create chatPanel.css
# (T018 doesn't depend on T015-T017 content, just needs T012-T013)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T011) - CRITICAL
3. Complete Phase 3: User Story 1 (T012-T023)
4. **STOP AND VALIDATE**: Test User Story 1 independently (T043-T054 US1 specific tests)
5. Deploy/demo if ready

**MVP Delivers**: Users can ask questions via floating chat widget and receive answers grounded in book content.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (Phases 1-2)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!) (Phases 3+6)
3. Add User Story 2 → Test independently → Deploy/Demo (Phase 4)
4. Add User Story 3 → Test independently → Deploy/Demo (Phase 5)
5. Polish & Test → Final deployment (Phases 6-7)

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (Phases 1-2)
2. Once Foundational is done:
   - Developer A: User Story 1 components (T012-T023)
   - Developer B: User Story 2 integration (T024-T028)
   - Developer C: User Story 3 accessibility (T029-T036)
3. Integrate and test together (Phases 6-7)

---

## Format Validation

All tasks follow the required format:
- [x] All tasks start with `- [ ]` or `- [X]` checkbox (completed or not)
- [x] All tasks have sequential Task IDs (T001-T054)
- [x] Parallel tasks marked with `[P]` where applicable
- [x] User story tasks marked with `[Story]` labels (US1, US2, US3)
- [x] All descriptions include exact file paths
- [x] No tasks missing ID, story label (for US phases), or file path

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Manual browser testing is required (T043-T054)
- Commit after each task or logical group
- Stop at checkpoints to validate story independently
- MVP = Phases 1-2-3 (Setup + Foundational + US1) = 23 tasks completed
- User Stories 2 and 3 add value but are optional for initial deployment
- All implementation tasks (T001-T042) are now complete ✅
- Phase 7 (Testing, T043-T054) requires manual testing after running servers
