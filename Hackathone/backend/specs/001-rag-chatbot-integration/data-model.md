# Data Model: RAG Chatbot Integration for Docusaurus Book

**Feature**: 001-rag-chatbot-integration
**Date**: 2025-12-30
**Purpose**: Define entities, attributes, relationships, and state management for the chatbot UI

---

## Overview

This document defines the data model for the chatbot UI integration. Since the RAG backend already has well-defined entities (`Query`, `ContextChunk`, `Response`, `RAGAgent`), this document focuses on frontend state management and the API contract layer.

**Key Principles**:
- Session-scoped data only (no persistence across browser sessions)
- State managed in React components via hooks
- API layer bridges frontend state to backend entities
- Immutable updates for predictability

---

## Frontend State Entities

### 1. ChatMessage

Represents a single message in the chat interface (user message or AI response).

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier for the message (UUID format) |
| `role` | enum | Yes | Message sender: `'user'` or `'assistant'` |
| `content` | string | Yes | Message text content |
| `timestamp` | ISO8601 | Yes | When the message was created |
| `highlightedContext` | string | No | Original highlighted text if this was a highlight-to-answer query (user messages only) |
| `isStreaming` | boolean | No | Whether the message is currently streaming (assistant messages only) |
| `error` | string | No | Error message if the message failed |

**Example**:
```javascript
{
  id: "550e8400-e29b-41d4-a716-446655440000",
  role: "assistant",
  content: "ROS 2 is a robot operating system...",
  timestamp: "2025-12-30T10:30:00Z",
  isStreaming: false
}

{
  id: "660e8400-e29b-41d4-a716-446655440000",
  role: "user",
  content: "What is ROS 2?",
  timestamp: "2025-12-30T10:29:58Z",
  highlightedContext: "ROS 2 is a robotic middleware..."
}
```

**Validation Rules**:
- `id` must be a valid UUID
- `role` must be `'user'` or `'assistant'`
- `content` must be non-empty and <= 2000 characters (to prevent abuse)
- `timestamp` must be a valid ISO8601 datetime
- `highlightedContext` must be <= 500 characters (if present)

---

### 2. ChatSession

Represents the current chat session state. This is stored in React component state and does not persist across browser sessions.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `messages` | ChatMessage[] | Yes | Array of messages in the session |
| `isLoading` | boolean | Yes | Whether a message is currently being sent |
| `error` | string | No | Current error message (if any) |
| `isOpen` | boolean | Yes | Whether the chat panel is currently open |
| `unreadCount` | number | Yes | Number of unread messages (used for badge) |

**Example**:
```javascript
{
  messages: [
    {
      id: "660e8400-e29b-41d4-a716-446655440000",
      role: "user",
      content: "What is ROS 2?",
      timestamp: "2025-12-30T10:29:58Z"
    },
    {
      id: "550e8400-e29b-41d4-a716-446655440000",
      role: "assistant",
      content: "ROS 2 is a robot operating system...",
      timestamp: "2025-12-30T10:30:00Z"
    }
  ],
  isLoading: false,
  error: null,
  isOpen: true,
  unreadCount: 0
}
```

**Validation Rules**:
- `messages` array length <= 50 (to prevent memory issues)
- `unreadCount` must be >= 0 and <= `messages.length`

**State Transitions**:

```
[Initial] → [Sending Message] → [Received Response] → [Success]
     |              ↓                    ↓
     └────────→ [Error] ←───────────────┘
```

1. **Initial**: Chat panel closed, no messages
2. **Sending Message**: User submits a message, `isLoading = true`
3. **Received Response**: Backend responds, `isLoading = false`
4. **Success**: Message added to `messages` array, display response
5. **Error**: Backend error, display error message in chat

---

### 3. HighlightSelection

Represents the current text selection state for highlight-to-answer functionality.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | No | Selected text (null if no selection) |
| `buttonPosition` | Position | No | Position to show "Ask about this" button (x, y coordinates) |
| `isValid` | boolean | No | Whether the selection is valid (length between 5-500 characters) |

**Position**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `x` | number | Yes | X coordinate in pixels (relative to viewport) |
| `y` | number | Yes | Y coordinate in pixels (relative to viewport) |

**Example**:
```javascript
{
  text: "ROS 2 is a robotic middleware that provides communication between nodes.",
  buttonPosition: {
    x: 250,
    y: 400
  },
  isValid: true
}

// No selection
{
  text: null,
  buttonPosition: null,
  isValid: false
}
```

**Validation Rules**:
- `text` must be between 5 and 500 characters (if present) to be valid
- `buttonPosition` coordinates must be >= 0

**State Transitions**:

```
[No Selection] → [Text Selected] → [Valid Selection] → [Ask Clicked] → [Chat Opened]
     |                 ↓                     ↓
     └─────→ [Selection Cleared] ←─────────┘
```

1. **No Selection**: User hasn't selected text
2. **Text Selected**: User starts selecting text
3. **Valid Selection**: Selection completes, meets length criteria
4. **Ask Clicked**: User clicks "Ask about this" button
5. **Chat Opened**: Chat panel opens with highlighted text pre-populated

---

### 4. ChatUIState

Represents the overall UI state for the chat widget.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `chatSession` | ChatSession | Yes | Current chat session state |
| `highlightSelection` | HighlightSelection | Yes | Current text selection state |
| `isMobile` | boolean | Yes | Whether the current device is mobile (affects layout) |
| `theme` | enum | Yes | Current theme: `'light'` or `'dark'` (inherited from Docusaurus) |

**Example**:
```javascript
{
  chatSession: {
    messages: [...],
    isLoading: false,
    error: null,
    isOpen: true,
    unreadCount: 0
  },
  highlightSelection: {
    text: null,
    buttonPosition: null,
    isValid: false
  },
  isMobile: false,
  theme: "light"
}
```

---

## API Layer Entities

### 5. ChatRequest

Request body sent to the backend `/chat` endpoint.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | Yes | User's question or message |
| `highlighted_text` | string | No | Highlighted text context (if using highlight-to-answer) |
| `context` | object | No | Additional context about the page |

**context** attributes:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `page_url` | string | No | Current page URL |
| `page_title` | string | No | Current page title |

**Example**:
```javascript
{
  "query": "What is ROS 2?",
  "highlighted_text": "ROS 2 is a robotic middleware...",
  "context": {
    "page_url": "https://asmaakbar88.vercel.app/docs/module-1-ros2",
    "page_title": "Module 1: ROS 2"
  }
}
```

**Validation Rules**:
- `query` must be non-empty and <= 2000 characters
- `highlighted_text` must be <= 500 characters (if present)

---

### 6. ChatResponse

Response body received from the backend `/chat` endpoint.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `response_id` | string | Yes | Unique identifier for the response |
| `query_id` | string | Yes | Identifier for the query this responds to |
| `content` | string | Yes | AI-generated response text |
| `generation_time` | number | Yes | Time taken to generate response (in seconds) |
| `confidence_score` | number | Yes | Confidence score (0.0 to 1.0) |
| `timestamp` | ISO8601 | Yes | When the response was generated |

**Example**:
```javascript
{
  "response_id": "response_1703926200",
  "query_id": "query_1703926198",
  "content": "ROS 2 is a robot operating system that provides communication, scheduling, and resource management for robot applications...",
  "generation_time": 1.23,
  "confidence_score": 0.85,
  "timestamp": "2025-12-30T10:30:00Z"
}
```

**Validation Rules**:
- `response_id` must be a non-empty string
- `query_id` must be a non-empty string
- `content` must be non-empty
- `generation_time` must be >= 0
- `confidence_score` must be between 0.0 and 1.0
- `timestamp` must be a valid ISO8601 datetime

---

### 7. ErrorResponse

Error response from the backend.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `error` | string | Yes | Error type/category |
| `message` | string | Yes | Human-readable error message |
| `code` | string | Yes | Error code for programmatic handling |

**Example**:
```javascript
{
  "error": "ValidationError",
  "message": "Query must be at least 5 characters long",
  "code": "QUERY_TOO_SHORT"
}

{
  "error": "ServiceUnavailable",
  "message": "RAG backend is temporarily unavailable. Please try again later.",
  "code": "SERVICE_UNAVAILABLE"
}

{
  "error": "Timeout",
  "message": "Request timed out. Please try again.",
  "code": "TIMEOUT"
}
```

---

## Entity Relationships

```
ChatUIState
├── ChatSession
│   └── ChatMessage[]
│       ├── User Message
│       │   └── highlightedContext (HighlightSelection.text)
│       └── Assistant Message
│           └── (maps to ChatResponse)
├── HighlightSelection
│   ├── text
│   └── buttonPosition
├── isMobile
└── theme

API Layer:
ChatRequest → Backend → ChatResponse / ErrorResponse
```

**Relationships**:
- `ChatSession` contains an array of `ChatMessage` objects
- User `ChatMessage` objects may reference `HighlightSelection.text` for context
- `ChatResponse` from the backend maps to an assistant `ChatMessage` in the session
- `ChatRequest` sent to the backend includes `query` and optional `highlighted_text`

---

## State Management Strategy

### Component State Hierarchy

```
ChatWidget (root)
├── State: ChatUIState
├── useChat() hook
│   ├── Manages ChatSession
│   └── Handles API calls
├── useHighlight() hook
│   └── Manages HighlightSelection
├── ChatWidgetIcon
│   └── Displays floating icon with unread badge
├── ChatPanel
│   ├── MessageList (displays ChatMessage[])
│   ├── MessageInput (creates new user ChatMessage)
│   └── ChatControls (clear chat, close)
└── HighlightButton
    └── Displays "Ask about this" button when selection is valid
```

### State Updates

**Sending a Message**:
1. User types message and clicks send
2. `useChat` hook creates new `ChatMessage` with `role: 'user'`
3. Add user message to `ChatSession.messages`
4. Set `ChatSession.isLoading = true`
5. Send `ChatRequest` to backend `/chat` endpoint
6. On success: Create assistant `ChatMessage` from `ChatResponse`, add to `messages`
7. On error: Add error message to chat or set `ChatSession.error`
8. Set `ChatSession.isLoading = false`

**Highlight-to-Answer**:
1. User selects text on page
2. `useHighlight` hook detects selection via Text Selection API
3. Update `HighlightSelection` with text and button position
4. Show floating "Ask about this" button
5. User clicks button
6. Open chat panel (`ChatSession.isOpen = true`)
7. Pre-populate input or context with highlighted text
8. When user sends message, include `highlighted_text` in `ChatRequest`

**Clearing Chat**:
1. User clicks "Clear Chat" button
2. Reset `ChatSession.messages = []`
3. Reset `ChatSession.error = null`
4. Reset `ChatSession.unreadCount = 0`

**Closing/Opening Chat**:
1. User clicks floating icon or close button
2. Toggle `ChatSession.isOpen`
3. If opening and closed: Set `unreadCount = 0`

---

## Data Flow Diagrams

### Send Message Flow

```
User Input
   ↓
MessageInput Component
   ↓
useChat.sendMessage(text)
   ↓
1. Create user ChatMessage
2. Update ChatSession.messages
3. Set isLoading = true
   ↓
chatService.sendMessage(text)
   ↓
POST /api/chat (ChatRequest)
   ↓
Backend (agent_retriev.py)
   ↓
POST /api/chat (ChatResponse / ErrorResponse)
   ↓
4. Create assistant ChatMessage
5. Update ChatSession.messages
6. Set isLoading = false
   ↓
UI Updates (MessageList re-renders)
```

### Highlight-to-Answer Flow

```
User Selects Text
   ↓
useHighlight (event listener)
   ↓
1. Get window.getSelection()
2. Validate selection (5-500 chars)
3. Update HighlightSelection
   ↓
HighlightButton renders at buttonPosition
   ↓
User clicks "Ask about this"
   ↓
1. Open ChatPanel
2. Pre-populate with highlighted text
   ↓
User sends question
   ↓
ChatRequest includes highlighted_text
   ↓
Backend generates response with context
```

---

## Backend Entity Mapping

### Frontend to Backend Mapping

| Frontend Entity | Backend Entity | Notes |
|-----------------|----------------|-------|
| `ChatRequest` | `Query` (agent_retriev.py) | Frontend request maps to backend Query object |
| `ChatResponse` | `Response` (agent_retriev.py) | Backend Response maps to frontend ChatResponse |
| `ChatMessage` (user) | `Query.text` | User message content becomes query text |
| `ChatMessage` (assistant) | `Response.content` | Assistant message content comes from response |
| `highlighted_text` | Query enhancement | Highlighted text is prepended to query as context |
| `context.page_url` | Metadata | Not used in current backend, but available |

**Query Enhancement Pattern**:
```javascript
// Frontend creates enhanced query
const enhancedQuery = highlightedText
  ? `Context: ${highlightedText}\n\nQuestion: ${query}`
  : query;

// Backend receives this as Query.text
// RAG agent processes enhanced query with context
```

---

## Error States

### UI Error States

| Error Type | Display | User Action |
|------------|---------|-------------|
| Network Error | "Unable to connect. Please check your internet connection." | Retry |
| Timeout | "Request timed out. Please try again." | Retry |
| Backend Error (500) | "Service unavailable. Please try again later." | Retry |
| Validation Error (400) | "Query must be at least 5 characters long." | Enter valid input |
| Empty Selection | "Please select text to ask about." | Select text again |
| Selection Too Long | "Selected text is too long. Please select less than 500 characters." | Select shorter text |

**Error Display Pattern**:
```javascript
// Show error as system message in chat
{
  id: "error-message-id",
  role: "system", // Special role for errors
  content: error.message,
  timestamp: new Date().toISOString(),
  error: error.code
}
```

---

## Security Considerations

### Input Sanitization

- **User Query**: Sanitize before sending to backend (prevent XSS)
- **Highlighted Text**: Same sanitization as user query
- **Display**: Use React's automatic XSS escaping when rendering messages

### Content Security

- **Response Content**: Trust backend responses (RAG ensures book-grounded answers)
- **Length Limits**: Enforce limits to prevent DoS attacks (2000 chars query, 500 chars highlight)

### CORS

- Backend must only allow requests from trusted origins (Docusaurus domain)
- No credentials required (session-scoped only)

---

## Storage Strategy

### Browser Storage

**No Persistence**: All state is stored in React component state and cleared on page refresh or navigation.

**Rationale**:
- User requirement: Session-scoped only
- No authentication: No user-specific data to persist
- Privacy: No data sent to third-party storage services
- Simplicity: No need to manage storage lifecycle

**Alternative (Future)**:
If persistence is needed, consider:
- **SessionStorage**: Cleared when tab closes
- **LocalStorage**: Persists across sessions (opt-in)
- **IndexedDB**: For larger datasets (not needed here)

---

## Performance Considerations

### Message Array Size

- Limit to 50 messages per session to prevent memory issues
- If limit reached, remove oldest messages (FIFO)

### Rendering Performance

- Use React key prop for efficient list rendering
- Consider virtualization for very long message lists (not needed for 50 message limit)
- Lazy load images if AI responses include them

### API Caching

- No client-side caching (session-scoped only)
- Backend RAG agent may have caching (handled by agent_retriev.py)

---

## Testing Strategy

### Unit Tests

- `ChatMessage` validation
- `ChatSession` state transitions
- `HighlightSelection` validation
- `ChatRequest` / `ChatResponse` validation

### Integration Tests

- API layer (chatService) → Backend endpoint
- useChat hook → chatService → UI updates
- useHighlight hook → Selection API → UI updates

### Manual Tests

- Full user flows (send message, highlight-to-answer, clear chat)
- Cross-device testing (desktop, tablet, mobile)
- Accessibility testing (keyboard navigation, screen reader)

---

## Migration Strategy

**No Migration Required**: This is a new feature. No existing data needs to be migrated.

---

## Glossary

| Term | Definition |
|------|------------|
| **ChatMessage** | A single message in the chat interface (user or assistant) |
| **ChatSession** | The current state of the chat (messages, loading, error) |
| **HighlightSelection** | The currently selected text for highlight-to-answer |
| **ChatRequest** | API request sent to the backend |
| **ChatResponse** | API response received from the backend |
| **Session-scoped** | Data that exists only for the current browser session |
| **RAG** | Retrieval-Augmented Generation (using Qdrant + OpenAI) |
| **Qdrant** | Vector database for storing book embeddings |
---

## References

- React State Management: https://react.dev/learn/state-a-components-memory
- FastAPI Pydantic Models: https://docs.pydantic.dev/latest/
- agent_retriev.py: Backend RAG agent implementation
- Feature Spec: [spec.md](./spec.md)
- Research Document: [research.md](./research.md)
