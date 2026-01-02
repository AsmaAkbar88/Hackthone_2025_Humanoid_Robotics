# Feature Specification: Fix RAG Book App Blank Screen

**Feature Branch**: `005-fix-rag-blank-screen`
**Created**: 2026-01-01
**Status**: Draft
**Input**: "Project: RAG Book App (blank screen). Folders to analyze: frontend book-docusaurus (Next.js + SpeckitPlus), backend (FastAPI + RAG + Qdrant). Core problems: 1. Book UI not showing (blank screen), 2. Chatbot UI not displaying on top of book frontend. Goals: Read both folders, identify root causes (API URL, env, CORS, hydration, scripts, client-only code), fix errors directly with diff format, ensure book renders and chatbot overlays correctly."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Book Content (Priority: P1)

As a reader, I want to access the Physical AI & Humanoid Robotics book content without encountering a blank screen, so that I can learn about robotics topics.

**Why this priority**: This is the core functionality - without visible content, the entire application is non-functional.

**Independent Test**: Can be tested by opening the Docusaurus site in a browser and verifying that:
- Homepage loads with title, tagline, and navigation
- Documentation pages (intro.md, modules) are accessible
- No console errors appear during page load

**Acceptance Scenarios**:

1. **Given** the user navigates to the book homepage, **When** the page loads, **Then** the title "Physical AI & Humanoid Robotics Book" and tagline should be visible.
2. **Given** the user clicks "Start Reading" button, **When** the intro page loads, **Then** the module navigation sidebar should appear.
3. **Given** the user selects a module from sidebar, **When** the page loads, **Then** the module content should be displayed without errors.

---

### User Story 2 - Access Chatbot Overlay (Priority: P1)

As a reader, I want to see and interact with a chatbot widget overlaid on the book pages, so that I can ask questions about the content.

**Why this priority**: The chatbot is a key value-add feature for the RAG-enabled book application.

**Independent Test**: Can be tested by:
- Opening browser DevTools console to verify no React/component errors
- Looking for chatbot floating button in bottom-right corner
- Clicking the button to verify chat panel opens
- Sending a test message to verify API connectivity

**Acceptance Scenarios**:

1. **Given** the user is on any book page, **When** the page loads, **Then** a floating chat button should be visible in the bottom-right corner.
2. **Given** the user clicks the chat button, **When** the panel opens, **Then** a chat input field and welcome message should be displayed.
3. **Given** the user sends a message, **When** the backend is running, **Then** a response from the RAG system should appear.

---

### User Story 3 - API Connectivity (Priority: P2)

As a user interacting with the chatbot, I want the backend API to be accessible, so that my questions can be answered using the RAG knowledge base.

**Why this priority**: Without API connectivity, the chatbot UI would be visible but non-functional.

**Independent Test**: Can be tested by:
- Starting the FastAPI backend
- Sending a test message via the chatbot
- Verifying response is received (or appropriate error shown)

**Acceptance Scenarios**:

1. **Given** the backend is running at `http://localhost:8000`, **When** a user sends a message, **Then** the frontend should receive a response within 10 seconds.
2. **Given** the backend is not running, **When** a user sends a message, **Then** a user-friendly error message should be displayed.

---

## Root Cause Analysis

### Issue 1: Blank Screen (Frontend)

**Identified Problems**:

1. **clientConfig.js**: Duplicate `export default` definitions causing module export conflicts
2. **Incorrect dynamic import path**: References `../backend/ui_chatbot/components/ChatWidget` from frontend which is invalid
3. **CSS import mismatch**: Chatbot tries to import from `./chatWidget.css` but should use relative path from frontend

### Issue 2: Chatbot Not Displaying (Frontend)

**Identified Problems**:

1. **Chatbot CSS**: `src/css/chatbot.css` is nearly empty (only contains `#chatbot-widget-root` placeholder)
2. **Static CSS**: `static/css/chatbot.css` exists but is not properly linked in the plugin
3. **Component rendering**: React components may fail silently if imports are broken

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Docusaurus site MUST render book content without blank screens
- **FR-002**: Chatbot widget MUST be visible as a floating button on all pages
- **FR-003**: Chatbot panel MUST open when button is clicked and display chat interface
- **FR-004**: Chatbot MUST communicate with backend API at configured URL
- **FR-005**: Chatbot CSS styles MUST apply correctly to all chatbot components

### Key Entities

- **ChatWidget**: Main React component for chatbot UI (location: `src/components/chatbot/`)
- **ChatService**: API communication layer (location: `src/services/chatService.js`)
- **ChatbotPlugin**: Docusaurus plugin for injecting chatbot (location: `src/plugin-chatbot.js`)
- **ChatbotClientModule**: Client module for React initialization (location: `src/chatbot-client.js`)

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Homepage renders within 5 seconds of page load with all content visible
- **SC-002**: No JavaScript console errors appear on page load
- **SC-003**: Chatbot floating button is visible on all pages immediately after page load
- **SC-004**: Chatbot panel opens within 500ms of button click
- **SC-005**: API requests complete within 10 seconds when backend is available
- **SC-006**: Book navigation works correctly - clicking sidebar items navigates to correct pages

---

## Technical Issues to Fix

### 1. clientConfig.js (book-docusaurus/src/clientModules.js)

**Current Issues**:
- Duplicate export default function definitions
- Invalid dynamic import path to backend

**Required Fixes**:
- Remove duplicate export
- Fix import path to use frontend components only

### 2. chatbot-client.js (book-docusaurus/src/chatbot-client.js)

**Current Issues**:
- Imports from `./components/chatbot/ChatWidget` which may not exist in correct location

**Required Fixes**:
- Verify import path is correct relative to file location
- Ensure ChatWidget.jsx exists and exports properly

### 3. Chatbot CSS (book-docusaurus/src/css/chatbot.css)

**Current Issues**:
- File contains minimal/empty styles

**Required Fixes**:
- Add missing CSS styles for chatbot components
- Ensure proper z-index for overlay positioning

### 4. Static CSS (book-docusaurus/static/css/chatbot.css)

**Current Issues**:
- May have styles but not properly linked

**Required Fixes**:
- Verify plugin correctly references static CSS file
- Ensure stylesheet is loaded in page head

---

## Assumptions

- Backend FastAPI server runs on `http://localhost:8000` for local development
- Docusaurus development server runs on `http://localhost:3000`
- Chatbot components are intended to be in `frontend/book-docusaurus/src/components/chatbot/`
- Backend components are in `backend/ui_chatbot/` for shared use

---

## Out of Scope

- Backend API functionality testing (beyond ensuring frontend can connect)
- Qdrant vector database configuration
- RAG embedding pipeline
- Production deployment configuration
