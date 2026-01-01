# Quickstart Guide: RAG Chatbot Integration for Docusaurus Book

**Feature**: 001-rag-chatbot-integration
**Date**: 2025-12-30
**Purpose**: Quick reference for setting up and running the chatbot feature

---

## Overview

This guide provides step-by-step instructions for setting up the RAG chatbot integration for the Docusaurus book. The chatbot allows readers to ask questions about the book content and receive contextual responses.

---

## Prerequisites

### Required Tools

- **Python 3.11+**: For running the FastAPI backend
- **Node.js 18+**: For Docusaurus build and development
- **npm or yarn**: For managing Docusaurus dependencies
- **Git**: For version control

### Environment Variables

Ensure the following environment variables are set in `backend/.env`:

```bash
# Qdrant Cloud
QDRANT_URL=https://your-qdrant-instance.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key

# Cohere (for embeddings)
COHERE_API_KEY=your-cohere-api-key

# OpenRouter / OpenAI (for AI generation)
OPENROUTER_API_KEY=your-openrouter-api-key

# Optional: Qdrant collection name
QDRANT_COLLECTION=new_rag_embedding
```

---

## Quick Setup (5 Minutes)

### Step 1: Verify Backend Setup

```bash
cd backend

# Verify .env file exists
ls -la .env

# Test RAG agent connection
python -c "from agent_retriev import RAGAgent; agent = RAGAgent(); print('Connected!')"
```

### Step 2: Start the Chat API Server

```bash
cd backend/ui_chatbot

# Start FastAPI server (auto-reloads on code changes)
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000

# You should see:
# INFO: Uvicorn running on http://0.0.0.0:8000
# INFO: Started reloader process
# INFO: Started server process
```

### Step 3: Test the API

Open a new terminal and test the chat endpoint:

```bash
# Test health check
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS 2?"}'
```

### Step 4: Start Docusaurus Development Server

```bash
cd ../book-docusaurus

# Install dependencies (first time only)
npm install

# Start development server
npm run start

# Open http://localhost:3000 in your browser
```

### Step 5: Test the Chat Widget

1. Open http://localhost:3000 in your browser
2. You should see a floating chat icon in the bottom-right corner
3. Click the icon to open the chat panel
4. Type a question like "What is ROS 2?" and press Enter
5. Wait for the response (should arrive within 5 seconds)

---

## Project Structure

```
backend/
├── ui_chatbot/              # NEW: Chatbot UI components
│   ├── api.py               # FastAPI chat endpoint
│   ├── components/           # React components
│   ├── hooks/               # Custom React hooks
│   ├── services/             # API client
│   ├── styles/               # CSS styles
│   └── utils/               # Helper functions
├── agent_retriev.py         # EXISTING: RAG agent
├── qdrant_data.py            # EXISTING: Qdrant utilities
└── main.py                   # EXISTING: Content embedding pipeline

book-docusaurus/              # EXISTING: Docusaurus book
├── src/
│   ├── components/
│   ├── css/
│   └── pages/
├── docs/
└── docusaurus.config.js
```

---

## Configuration

### API URL Configuration

Edit `backend/ui_chatbot/utils/constants.js`:

```javascript
export const API_URL = process.env.BACKEND_URL || 'http://localhost:8000';
export const API_TIMEOUT = 10000; // 10 seconds
```

For production, set `BACKEND_URL` environment variable:

```bash
export BACKEND_URL=https://your-production-backend.com
```

### Docusaurus Configuration

To inject the chat widget into all pages, update `book-docusaurus/docusaurus.config.js`:

```javascript
{
  theme: {
    customCss: './src/css/custom.css',
    clientModules: [
      // Inject chat widget on all pages
      require.resolve('../backend/ui_chatbot/index.js'),
    ],
  },
}
```

### CORS Configuration

Ensure the FastAPI backend allows requests from the Docusaurus domain. Edit `backend/ui_chatbot/api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Local development
        "https://asmaakbar88.vercel.app",  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Development Workflow

### 1. Working on Backend API

```bash
# Terminal 1: Start API server
cd backend/ui_chatbot
python -m uvicorn api:app --reload

# Terminal 2: Run tests
cd backend
pytest ui_chatbot/tests/
```

### 2. Working on Frontend Components

```bash
# Terminal 1: Start Docusaurus dev server
cd book-docusaurus
npm run start

# Terminal 2: Run component tests (if configured)
cd book-docusaurus
npm test
```

### 3. Testing End-to-End

```bash
# 1. Start backend API (Terminal 1)
cd backend/ui_chatbot
python -m uvicorn api:app --reload

# 2. Start Docusaurus (Terminal 2)
cd ../book-docusaurus
npm run start

# 3. Test in browser at http://localhost:3000
#    - Test chat widget icon visibility
#    - Test sending messages
#    - Test highlight-to-answer
#    - Test responsive design (resize browser)
#    - Test keyboard navigation
#    - Test error handling (stop backend API)
```

---

## Common Tasks

### Adding a New Message Type

1. Update `data-model.md` with new message type
2. Update `api.yaml` with new API contract
3. Implement in `backend/ui_chatbot/api.py`
4. Update `backend/ui_chatbot/hooks/useChat.js`
5. Add UI component in `backend/ui_chatbot/components/`
6. Update styles in `backend/ui_chatbot/styles/`

### Styling the Chat Widget

Edit `backend/ui_chatbot/styles/chatWidget.css` for widget icon styling:

```css
.chat-widget-icon {
  background-color: var(--chat-primary, #3b82f6);
  width: 56px;
  height: 56px;
  border-radius: 50%;
  /* ... */
}
```

Edit `backend/ui_chatbot/styles/chatPanel.css` for panel styling:

```css
.chat-panel {
  background-color: var(--chat-bg, #ffffff);
  width: 400px;
  height: 600px;
  /* ... */
}
```

### Adding a New API Endpoint

1. Add endpoint to `backend/ui_chatbot/api.py`
2. Update `contracts/api.yaml` with OpenAPI spec
3. Update `backend/ui_chatbot/services/chatService.js` (if needed)
4. Update tests in `backend/ui_chatbot/tests/`

### Testing on Mobile

Use Chrome DevTools for mobile testing:

1. Open Chrome DevTools (F12)
2. Click device toolbar icon (or Ctrl+Shift+M)
3. Select device (iPhone 14, Pixel 7, etc.)
4. Test chat widget behavior

---

## Troubleshooting

### Chat widget not showing

**Symptom**: Floating chat icon doesn't appear on pages

**Solutions**:
1. Check browser console for errors (F12)
2. Verify `clientModules` is configured in `docusaurus.config.js`
3. Check that `backend/ui_chatbot/index.js` exists and exports properly
4. Clear browser cache and hard refresh (Ctrl+Shift+R)

### API requests failing with CORS error

**Symptom**: Console shows "Access to fetch at '...' has been blocked by CORS policy"

**Solutions**:
1. Verify CORS middleware is configured in `backend/ui_chatbot/api.py`
2. Check that Docusaurus URL is in `allow_origins`
3. Ensure backend server is running on correct port
4. Check browser network tab for preflight request status

### Chat responses timing out

**Symptom**: Messages stay in loading state indefinitely

**Solutions**:
1. Check backend server logs for errors
2. Verify `agent_retriev.py` can connect to Qdrant
3. Check that COHERE_API_KEY and OPENROUTER_API_KEY are valid
4. Increase timeout in `backend/ui_chatbot/utils/constants.js`
5. Test health endpoint: `curl http://localhost:8000/health`

### Highlight-to-answer not working

**Symptom**: "Ask about this" button doesn't appear when selecting text

**Solutions**:
1. Check browser console for selection API errors
2. Verify selection is between 5-500 characters
3. Check that `useHighlight` hook is properly initialized
4. Ensure event listeners are attached to document

### Chat not responsive on mobile

**Symptom**: Chat panel layout broken on mobile devices

**Solutions**:
1. Check `backend/ui_chatbot/styles/responsive.css` media queries
2. Verify breakpoints match device sizes
3. Test in browser DevTools device emulator
4. Check for missing CSS in compiled bundle

---

## Building for Production

### 1. Build Docusaurus Site

```bash
cd book-docusaurus

# Build production bundle
npm run build

# Output in `build/` directory
ls -la build/
```

### 2. Deploy Backend

```bash
cd backend

# Option A: Deploy to Vercel (recommended)
# - Set environment variables in Vercel dashboard
# - Deploy `ui_chatbot/` as a separate app

# Option B: Deploy to Railway, Render, or similar
# - Follow platform-specific deployment instructions
# - Set required environment variables

# Option C: Docker deployment
# - Use provided Dockerfile (if available)
# - Build and push to registry
```

### 3. Configure Production URLs

Update environment variables:

```bash
# Production backend URL
BACKEND_URL=https://your-production-backend.com

# Production Docusaurus URL (for CORS)
ALLOWED_ORIGINS=https://asmaakbar88.vercel.app
```

### 4. Test Production Deployment

```bash
# 1. Test health endpoint
curl https://your-production-backend.com/health

# 2. Test chat endpoint
curl -X POST https://your-production-backend.com/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS 2?"}'

# 3. Test in browser
#    - Open production URL
#    - Verify chat widget shows
#    - Test sending messages
```

---

## Performance Optimization

### Lazy Loading

The chat widget is lazy loaded to minimize initial page impact:

```javascript
// backend/ui_chatbot/index.js
import('./components/ChatWidget').then(({ default: ChatWidget }) => {
  // Render chat widget after page loads
});
```

### Code Splitting

For larger apps, consider code splitting:

```javascript
const ChatPanel = lazy(() => import('./components/ChatPanel'));

// Use with Suspense
<Suspense fallback={<Loading />}>
  <ChatPanel />
</Suspense>
```

### API Caching

Consider caching responses on the backend:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_response(query_hash):
    # Check cache before calling RAG agent
    pass
```

---

## Security Checklist

- [ ] CORS is configured to allow only trusted origins
- [ ] No sensitive data (API keys) is exposed in frontend code
- [ ] Input validation is enforced on both frontend and backend
- [ ] Rate limiting is configured on the backend (optional)
- [ ] HTTPS is used in production
- [ ] Error messages don't leak sensitive information

---

## Monitoring

### Health Checks

Monitor the backend health endpoint:

```bash
# Check health status
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "details": {
#     "qdrant": true,
#     "openai": true,
#     "cohere": true,
#     "overall": true
#   }
# }
```

### Logging

Logs are available in the backend console:

```bash
# Backend API logs
cd backend/ui_chatbot
python -m uvicorn api:app --reload

# RAG agent logs
cd backend
python agent_retriev.py
```

---

## API Documentation

### Interactive API Docs (Swagger UI)

When the backend is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide an interactive interface to test all API endpoints.

### OpenAPI Specification

The full OpenAPI specification is available at:

- **Raw YAML**: `specs/001-rag-chatbot-integration/contracts/api.yaml`
- **JSON**: http://localhost:8000/openapi.json

---

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest ui_chatbot/tests/test_api.py

# Run with coverage
pytest --cov=ui_chatbot --cov-report=html
```

### Frontend Tests

```bash
cd book-docusaurus

# Run component tests
npm test

# Run with watch mode
npm test -- --watch
```

### Manual Testing Checklist

- [ ] Chat widget appears on all pages
- [ ] Chat panel opens/closes correctly
- [ ] Messages can be sent and received
- [ ] Loading indicator shows during API calls
- [ ] Error messages display appropriately
- [ ] Highlight-to-Answer works
- [ ] Chat history is preserved
- [ ] Clear chat button works
- [ ] Responsive design on mobile/tablet/desktop
- [ ] Keyboard navigation works (Tab, Enter, Escape)
- [ ] Theme switching (light/dark) works
- [ ] CORS configuration works (no browser errors)

---

## Getting Help

### Documentation

- **Feature Spec**: `specs/001-rag-chatbot-integration/spec.md`
- **Implementation Plan**: `specs/001-rag-chatbot-integration/plan.md`
- **Research Document**: `specs/001-rag-chatbot-integration/research.md`
- **Data Model**: `specs/001-rag-chatbot-integration/data-model.md`
- **API Contract**: `specs/001-rag-chatbot-integration/contracts/api.yaml`

### Common Issues

See the [Troubleshooting](#troubleshooting) section above for common issues and solutions.

### Project Resources

- **Docusaurus Documentation**: https://docusaurus.io/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **React Documentation**: https://react.dev/
- **qdrant-client Documentation**: https://qdrant.tech/documentation/

---

## Next Steps

After completing this quickstart:

1. Review the [Implementation Plan](./plan.md) for detailed design decisions
2. Review the [Research Document](./research.md) for technical justifications
3. Review the [Data Model](./data-model.md) for entity definitions
4. Review the [API Contract](./contracts/api.yaml) for endpoint specifications
5. Proceed to task implementation (`/sp.tasks`)

---

## Summary

| Task | Command |
|------|---------|
| Start Backend | `cd backend/ui_chatbot && python -m uvicorn api:app --reload` |
| Start Docusaurus | `cd book-docusaurus && npm run start` |
| Test API | `curl http://localhost:8000/health` |
| Build Production | `cd book-docusaurus && npm run build` |
| Run Tests | `cd backend && pytest` |

---

**Good luck with your implementation! 🤖**
