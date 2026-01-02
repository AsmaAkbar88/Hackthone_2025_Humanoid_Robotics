# Tasks: Fix RAG Book App Blank Screen

**Feature**: Fix RAG Book App Blank Screen
**Branch**: `005-fix-rag-blank-screen`
**Created**: 2026-01-01
**Status**: Ready for Implementation

---

## Summary

- **Total Tasks**: 8
- **User Stories**: 2 (US1 - View Book Content, US2 - Access Chatbot Overlay)
- **Parallel Opportunities**: Tasks T002, T003, T004 can run in parallel (different files, no dependencies)
- **MVP Scope**: Tasks T001-T004 (fixes blank screen and chatbot visibility)

---

## Dependencies

```
Phase 1 (Setup) → Phase 2 (Fix clientModules.js) → Phase 3 (Fix ChatWidget) → Phase 4 (Add CSS) → Phase 5 (Verify plugin)
                    ↑
                    └── T001 blocks T002
```

---

## Phase 1: Setup

- [x] T001 Read clientModules.js to understand current structure in book-docusaurus/src/clientModules.js

---

## Phase 2: Fix clientModules.js

**Goal**: Remove duplicate export default and fix invalid import path

**Independent Test**: File saves without syntax errors, no duplicate export warnings

- [x] T002 [US1] Fix duplicate export default in book-docusaurus/src/clientModules.js
- [x] T003 [US1] Fix import path from ../backend/ui_chatbot/components/ChatWidget to ./components/chatbot/ChatWidget in book-docusaurus/src/clientModules.js

---

## Phase 3: Fix ChatWidget CSS Import

**Goal**: Correct CSS import path in ChatWidget component

**Independent Test**: ChatWidget.jsx loads without import errors

- [x] T004 [P] [US2] Read ChatWidget.jsx to identify CSS import in book-docusaurus/src/components/chatbot/ChatWidget.jsx
- [x] T005 [P] [US2] Fix CSS import path from ./chatWidget.css to ../../css/chatbot.css in book-docusaurus/src/components/chatbot/ChatWidget.jsx

---

## Phase 4: Add Chatbot CSS Styles

**Goal**: Add missing CSS styles for chatbot components

**Independent Test**: chatbot.css contains styles for widget, button, and panel

- [x] T006 [P] [US2] Read static/css/chatbot.css to get full styles in book-docusaurus/static/css/chatbot.css
- [x] T007 [P] [US2] Copy styles to src/css/chatbot.css in book-docusaurus/src/css/chatbot.css

---

## Phase 5: Verify Plugin CSS Linking

**Goal**: Ensure static CSS is properly linked in plugin

**Independent Test**: npm run build completes without CSS errors

- [x] T008 [US2] Verify plugin-chatbot.js links to correct CSS path in book-docusaurus/src/plugin-chatbot.js

---

## Implementation Strategy

### MVP (Minimum Viable Product)
- Complete Tasks T001-T004
- This fixes the blank screen issue
- Chatbot becomes visible but may lack full styling

### Incremental Delivery
- T005: Fixes chatbot CSS loading
- T006-T007: Adds full chatbot styling
- T008: Verifies CSS linking for production build

### Parallel Execution
- T002, T003 can run after T001
- T004-T005 can run in parallel with T002-T003 (different files)
- T006-T007 can run in parallel with each other
- T008 depends on T006-T007 (needs CSS files ready)

---

## Independent Test Criteria

### User Story 1 - View Book Content
- [ ] Homepage renders with title "Physical AI & Humanoid Robotics Book"
- [ ] Tagline "Comprehensive Guide to Physical AI Systems" is visible
- [ ] Navigation sidebar appears on intro page
- [ ] No JavaScript console errors on page load

### User Story 2 - Access Chatbot Overlay
- [ ] Floating chat button visible in bottom-right corner
- [ ] Chat panel opens when button is clicked
- [ ] Chat input field and welcome message display
- [ ] Chatbot CSS styles apply correctly (button, panel, messages)

---

## Verification Commands

```bash
# Build the Docusaurus site
cd book-docusaurus && npm run build

# Start development server
cd book-docusaurus && npm start

# Verify backend connectivity
curl http://localhost:8000/health
```
