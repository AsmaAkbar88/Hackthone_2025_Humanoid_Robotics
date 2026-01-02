# Research Document: RAG Chatbot Integration for Docusaurus Book

**Feature**: 001-rag-chatbot-integration
**Date**: 2025-12-30
**Purpose**: Document research findings and technical decisions for implementing the chatbot UI integration

## Overview

This document consolidates research findings for integrating a RAG-powered chatbot into the existing Docusaurus book. All research focuses on practical implementation patterns that align with project constraints and user requirements.

---

## 1. Docusaurus Client Code Integration

### Research Question: How to inject React components into all pages of a Docusaurus site without modifying content?

**Decision**: Use Docusaurus `clientModules` configuration

**Rationale**:
- Docusaurus 3.x supports `clientModules` in the `theme` preset configuration
- Client modules are injected into every page automatically
- Non-invasive to existing book content and structure
- React components can access Docusaurus context (theme, location, etc.)
- Standard pattern for adding custom UI elements

**Implementation Pattern**:
```javascript
// docusaurus.config.js
{
  theme: {
    customCss: './src/css/custom.css',
    clientModules: [
      // Import chat widget to inject on all pages
      require.resolve('../backend/ui_chatbot/index.js'),
    ],
  },
}
```

**Alternatives Considered**:
- **Swizzling theme components**: Invasive to Docusaurus theme; harder to maintain; requires theme updates
- **Wrapping Layout component**: Requires swizzling root layout; more complex setup
- **Inline script injection**: Not idiomatic for Docusaurus; harder to manage React state

**References**:
- Docusaurus Documentation: https://docusaurus.io/docs/client-modules
- Client Module Example: https://docusaurus.io/docs/using-client-components

---

## 2. React Component Structure for Chat Widget

### Research Question: What is the best component structure for a floating chat widget with responsive behavior?

**Decision**: Component hierarchy with state management in parent, specialized children for specific UI elements

**Rationale**:
- Separation of concerns: widget, panel, messages, input, and highlight button as distinct components
- State management in parent (ChatWidget) for easy testing and reuse
- Props-based communication for clear data flow
- Custom hooks for reusable logic (useChat, useHighlight)

**Component Structure**:
```
ChatWidget (root component)
├── ChatWidgetIcon (floating button)
├── ChatPanel (main interface)
│   ├── MessageList (display messages)
│   ├── MessageInput (user input)
│   └── ChatControls (clear chat, close button)
└── HighlightButton (floating "Ask about this")
```

**Custom Hooks**:
- `useChat()`: Manages chat state (messages, loading, error), handles API calls
- `useHighlight()`: Manages text selection, shows/hides highlight button

**Alternatives Considered**:
- **Single monolithic component**: Harder to test, less maintainable, code bloat
- **Context API for state**: Overkill for simple chat state, unnecessary complexity
- **Redux/Zustand**: Too much complexity for session-scoped state

**References**:
- React Hooks: https://react.dev/reference/react
- Docusaurus React Components: https://docusaurus.io/docs/using-themes#global-components

---

## 3. Backend API Endpoint Design

### Research Question: What is the appropriate API design for the chat endpoint?

**Decision**: RESTful POST endpoint with JSON request/response

**Rationale**:
- Simple and standard pattern for chat APIs
- Existing backend uses FastAPI (REST framework)
- JSON format is flexible and widely supported
- POST method is appropriate for sending data and receiving responses
- No authentication required (per spec), simplifies design

**Endpoint Specification**:
```
POST /chat
Content-Type: application/json

Request Body:
{
  "query": "string (required)",
  "highlighted_text": "string (optional)",
  "context": {
    "page_url": "string (optional)",
    "page_title": "string (optional)"
  }
}

Response:
{
  "response_id": "string",
  "query_id": "string",
  "content": "string",
  "generation_time": "float (seconds)",
  "confidence_score": "float (0-1)",
  "timestamp": "ISO8601"
}

Error Response (4xx/5xx):
{
  "error": "string",
  "message": "string",
  "code": "string"
}
```

**Alternatives Considered**:
- **GraphQL**: Overkill for single endpoint; adds complexity without benefit
- **WebSocket**: Unnecessary for request/response pattern; over-engineering
- **Server-Sent Events (SSE)**: No streaming requirement; unnecessary complexity

**References**:
- FastAPI Documentation: https://fastapi.tiangolo.com/
- REST API Best Practices: https://restfulapi.net/

---

## 4. Integration with Existing RAG Backend

### Research Question: How to connect the new API endpoint to the existing `agent_retriev.py`?

**Decision**: Create a new FastAPI endpoint that imports and calls the `RAGAgent` class

**Rationale**:
- Existing `agent_retriev.py` has a well-defined `RAGAgent` class with `query()` method
- Reuse existing RAG logic without modifications
- Minimal code duplication
- Clean separation of API layer from business logic

**Integration Pattern**:
```python
# backend/ui_chatbot/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add parent directory to path to import agent_retriev
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent_retriev import RAGAgent

app = FastAPI(title="Docusaurus Book Chatbot API")

# Initialize RAG agent (single instance for efficiency)
rag_agent = RAGAgent()

class ChatRequest(BaseModel):
    query: str
    highlighted_text: Optional[str] = None
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    response_id: str
    query_id: str
    content: str
    generation_time: float
    confidence_score: float
    timestamp: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that queries the RAG backend with optional highlighted context.
    """
    try:
        # Combine query and highlighted text if provided
        enhanced_query = request.query
        if request.highlighted_text:
            enhanced_query = f"Context: {request.highlighted_text}\n\nQuestion: {request.query}"

        # Query RAG agent
        response = rag_agent.query(enhanced_query)

        return ChatResponse(
            response_id=response.response_id,
            query_id=response.query_id,
            content=response.content,
            generation_time=response.generation_time,
            confidence_score=response.confidence_score,
            timestamp=response.timestamp.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    status = rag_agent.health_check()
    return {"status": "healthy" if status["overall"] else "unhealthy", "details": status}
```

**Alternatives Considered**:
- **Modify agent_retriev.py directly**: Violates separation of concerns; harder to maintain
- **Copy RAG logic into api.py**: Code duplication; maintenance burden
- **Create separate microservice**: Unnecessary complexity for this scope

**References**:
- FastAPI Request Body: https://fastapi.tiangolo.com/tutorial/body/
- Pydantic Models: https://docs.pydantic.dev/latest/

---

## 5. Highlight-to-Answer Implementation

### Research Question: How to capture text selection and show a floating "Ask about this" button?

**Decision**: Use browser's Text Selection API with event listeners on document

**Rationale**:
- Native browser API (`window.getSelection()`) works across all modern browsers
- Event listeners (`mouseup`, `touchend`) detect selection completion
- Can get selection position for floating button placement
- No external dependencies required

**Implementation Pattern**:
```javascript
// backend/ui_chatbot/hooks/useHighlight.js
import { useState, useCallback, useEffect } from 'react';

export function useHighlight(onAsk) {
  const [selection, setSelection] = useState(null);
  const [buttonPosition, setButtonPosition] = useState({ x: 0, y: 0 });

  const handleSelection = useCallback(() => {
    const selection = window.getSelection();
    const text = selection.toString().trim();

    if (text.length > 5 && text.length < 500) { // Validate length
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();

      setSelection(text);
      setButtonPosition({
        x: rect.left + window.scrollX,
        y: rect.bottom + window.scrollY + 10
      });
    } else {
      setSelection(null);
    }
  }, []);

  useEffect(() => {
    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('touchend', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('touchend', handleSelection);
    };
  }, [handleSelection]);

  const clearSelection = useCallback(() => {
    setSelection(null);
    window.getSelection().removeAllRanges();
  }, []);

  const handleAsk = useCallback(() => {
    if (selection) {
      onAsk(selection);
      clearSelection();
    }
  }, [selection, onAsk, clearSelection]);

  return {
    selection,
    buttonPosition,
    handleAsk,
    clearSelection
  };
}
```

**Alternatives Considered**:
- **ContentEditable approach**: Overkill for simple text selection
- **Custom text selection UI**: Complex, reinventing the wheel
- **MutationObserver**: Unnecessary for this use case

**References**:
- Selection API: https://developer.mozilla.org/en-US/docs/Web/API/Selection
- Range API: https://developer.mozilla.org/en-US/docs/Web/API/Range

---

## 6. Responsive Design Strategy

### Research Question: How to ensure the chat widget works well on desktop, tablet, and mobile?

**Decision**: CSS Media Queries + Flexbox with breakpoint-based layouts

**Rationale**:
- Native CSS support; no dependencies required
- Flexbox provides flexible layouts for panel content
- Media queries enable breakpoint-specific styling
- Matches Docusaurus theme system approach

**Breakpoints**:
```css
/* Mobile (default) */
.chat-panel {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 80vh;
  border-radius: 16px 16px 0 0;
}

/* Tablet and Desktop */
@media (min-width: 768px) {
  .chat-panel {
    bottom: 80px;
    right: 20px;
    left: auto;
    width: 400px;
    height: 600px;
    border-radius: 12px;
  }
}

/* Large Desktop */
@media (min-width: 1200px) {
  .chat-panel {
    width: 450px;
    height: 650px;
  }
}
```

**Alternatives Considered**:
- **CSS Grid**: Useful for complex layouts, but Flexbox sufficient for this widget
- **CSS Frameworks (Bootstrap, Tailwind)**: Adds dependencies; unnecessary for single widget
- **JavaScript-based responsive logic**: Slower; less maintainable; harder to debug

**References**:
- CSS Media Queries: https://developer.mozilla.org/en-US/docs/Web/CSS/Media_Queries
- Flexbox: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout

---

## 7. Styling and Theming

### Research Question: How to ensure the chat widget matches the Docusaurus theme?

**Decision**: CSS Variables matching Docusaurus theme system

**Rationale**:
- Docusaurus uses CSS variables for theming (light/dark mode)
- Can inherit theme colors automatically
- Responsive to user's theme preference
- Easy to customize if needed

**Theming Pattern**:
```css
/* backend/ui_chatbot/styles/chatWidget.css */
.chat-widget {
  /* Inherit from Docusaurus theme variables */
  --chat-bg: var(--ifm-background-surface-color);
  --chat-text: var(--ifm-font-color-base);
  --chat-primary: var(--ifm-color-primary);
  --chat-border: var(--ifm-border-color);
  --chat-shadow: var(--ifm-global-shadow-lw);
}

/* Light/dark mode handled automatically by Docusaurus */
```

**Alternatives Considered**:
- **Hardcoded colors**: Doesn't respect user theme preference; maintenance burden
- **Inline styles**: Hard to maintain; no theme support
- **CSS-in-JS (styled-components, emotion)**: Adds complexity; build-time only

**References**:
- Docusaurus Theming: https://docusaurus.io/docs/styling-layout#styling-your-site-with-css
- CSS Variables: https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties

---

## 8. Error Handling and User Experience

### Research Question: How to handle backend errors gracefully and provide good UX?

**Decision**: Try-catch with user-friendly error messages, loading indicators, and retry logic

**Rationale**:
- Users should see helpful messages, not technical errors
- Loading indicators provide feedback during API calls
- Retry logic handles transient failures
- Timeout handling prevents indefinite waiting

**Error Handling Pattern**:
```javascript
// backend/ui_chatbot/services/chatService.js
export async function sendMessage(query, highlightedText = null) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000); // 10s timeout

  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        highlighted_text: highlightedText
      }),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to get response');
    }

    return await response.json();
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('Request timed out. Please try again.');
    }
    throw error;
  }
}
```

**Alternatives Considered**:
- **Silent failures**: Bad UX; user doesn't know what happened
- **Technical error messages**: Confusing for non-technical users
- **No retry logic**: Poor experience on transient network issues

**References**:
- Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- AbortController: https://developer.mozilla.org/en-US/docs/Web/API/AbortController

---

## 9. Accessibility Considerations

### Research Question: How to ensure the chat widget is accessible to all users?

**Decision**: ARIA attributes, keyboard navigation, and focus management

**Rationale**:
- ARIA labels provide context for screen readers
- Keyboard navigation enables use without mouse
- Focus management ensures proper tab order
- WCAG AA compliance for color contrast

**Accessibility Checklist**:
- [ ] All interactive elements have `aria-label` or visible text
- [ ] Chat panel has `role="dialog"` and `aria-modal="true"`
- [ ] Keyboard navigation: Tab, Enter, Escape keys supported
- [ ] Focus trap when chat panel is open
- [ ] Focus returns to trigger element when chat closes
- [ ] Loading indicators have `aria-live` region
- [ ] Error messages are announced to screen readers
- [ ] Color contrast meets WCAG AA (4.5:1 for normal text)
- [ ] Touch targets are at least 44x44 pixels

**References**:
- WAI-ARIA Practices: https://www.w3.org/WAI/ARIA/apg/
- Web Content Accessibility Guidelines (WCAG): https://www.w3.org/WAI/WCAG21/quickref/

---

## 10. Performance Optimization

### Research Question: How to ensure the chat widget doesn't significantly impact page load time?

**Decision**: Lazy loading, minimal dependencies, code splitting

**Rationale**:
- Chat widget is secondary functionality; shouldn't block initial page load
- Minimal dependencies reduce bundle size
- Lazy loading defers widget initialization until needed
- Code splitting allows separate caching of widget code

**Optimization Strategies**:
```javascript
// Lazy load chat widget
const loadChatWidget = () => {
  import('./components/ChatWidget').then(({ default: ChatWidget }) => {
    // Render chat widget after initial page load
  });
};

// Load after page is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadChatWidget);
} else {
  loadChatWidget();
}
```

**Alternatives Considered**:
- **Immediate loading**: Blocks initial render; larger bundle size
- **Server-side rendering**: Overkill for widget; adds complexity
- **Preloading**: Not needed for secondary feature

**References**:
- React Lazy: https://react.dev/reference/react/lazy
- Webpack Code Splitting: https://webpack.js.org/guides/code-splitting/

---

## 11. CORS Configuration

### Research Question: How to allow Docusaurus frontend to communicate with FastAPI backend?

**Decision**: Configure CORS middleware in FastAPI

**Rationale**:
- Browser security requires CORS for cross-origin requests
- FastAPI has built-in CORS middleware (`fastapi.middleware.cors`)
- Simple to configure; standard pattern

**CORS Configuration**:
```python
# backend/ui_chatbot/api.py
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Docusaurus Book Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://asmaakbar88.vercel.app",  # Production Docusaurus URL
        "http://localhost:3000",           # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Alternatives Considered**:
- **Same-origin deployment**: Not possible with current setup (Docusaurus on Vercel, backend separate)
- **Proxy through Docusaurus**: Complex; adds unnecessary routing
- **Disable CORS**: Not secure; browser will block requests

**References**:
- FastAPI CORS: https://fastapi.tiangolo.com/tutorial/cors/
- MDN CORS: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

---

## 12. Testing Strategy

### Research Question: How to test the chatbot UI and backend integration?

**Decision**: Unit tests for components, integration tests for API, manual browser testing

**Rationale**:
- React Testing Library for component testing
- pytest for backend testing
- Manual testing for full user flows (especially accessibility)
- End-to-end testing optional given scope

**Testing Plan**:
```javascript
// Component test example
// backend/ui_chatbot/components/__tests__/ChatWidget.test.js
import { render, screen, fireEvent } from '@testing-library/react';
import ChatWidget from '../ChatWidget';

test('opens chat panel when icon is clicked', () => {
  render(<ChatWidget />);
  const icon = screen.getByLabelText('Open chat');
  fireEvent.click(icon);
  expect(screen.getByRole('dialog')).toBeInTheDocument();
});
```

```python
# Backend test example
# backend/ui_chatbot/tests/test_api.py
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post("/chat", json={"query": "What is ROS 2?"})
    assert response.status_code == 200
    assert "response_id" in response.json()
```

**Alternatives Considered**:
- **End-to-end (Cypress/Playwright)**: Valuable but time-intensive for current scope
- **Snapshot testing**: Too brittle for UI; focuses on implementation details
- **No tests**: High risk of bugs; harder to refactor

**References**:
- React Testing Library: https://testing-library.com/react
- pytest: https://docs.pytest.org/

---

## Summary of Decisions

| Category | Decision | Key Benefits |
|----------|----------|--------------|
| **Docusaurus Integration** | Client code injection (`clientModules`) | Non-invasive, standard pattern |
| **Component Structure** | Hierarchical with custom hooks | Separation of concerns, testability |
| **API Design** | RESTful POST endpoint | Simple, standard, FastAPI-compatible |
| **Backend Integration** | Import `RAGAgent` class | Reuse existing logic, minimal duplication |
| **Highlight-to-Answer** | Text Selection API | Native browser support, no dependencies |
| **Responsive Design** | CSS Media Queries + Flexbox | Native support, matches Docusaurus |
| **Styling** | CSS Variables | Theme-aware, maintainable |
| **Error Handling** | Try-catch with user-friendly messages | Good UX, helpful feedback |
| **Accessibility** | ARIA + keyboard navigation | WCAG compliance, inclusive |
| **Performance** | Lazy loading, minimal dependencies | Fast page load, small bundle |
| **CORS** | FastAPI CORS middleware | Secure, standard pattern |
| **Testing** | Unit + integration + manual | Balance coverage and effort |

---

## Risks and Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Docusaurus version incompatibility | Low | High | Test with Docusaurus 3.x; use standard patterns |
| Browser compatibility issues | Medium | Medium | Test on target browsers; use standard APIs |
| Slow RAG response times | Medium | High | Optimize queries; set timeouts; provide loading feedback |
| CORS configuration issues | Low | High | Document CORS setup; test locally and production |
| Mobile UX issues | Medium | Medium | Responsive design; mobile testing |
| Accessibility issues | Medium | Medium | ARIA attributes; keyboard navigation; manual testing |
| State management complexity | Low | Medium | Keep state simple (session-scoped); avoid over-engineering |

---

## Next Steps

1. Create data model specification ([data-model.md](./data-model.md))
2. Create API contract specification ([contracts/api.yaml](./contracts/api.yaml))
3. Create quickstart guide ([quickstart.md](./quickstart.md))
4. Proceed to task planning (`/sp.tasks`)

---

## References

- Docusaurus Documentation: https://docusaurus.io/
- FastAPI Documentation: https://fastapi.tiangolo.com/
- React Documentation: https://react.dev/
- Web MDN: https://developer.mozilla.org/
- WAI-ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- Web Content Accessibility Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
