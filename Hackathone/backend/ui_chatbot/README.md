# Chatbot UI Components for Docusaurus Book

This directory contains all UI-related files for the RAG chatbot integration into the Physical AI & Humanoid Robotics Docusaurus book.

## Directory Structure

```
ui_chatbot/
├── api.py                     # FastAPI chat endpoint (calls agent_retriev.py)
├── components/                 # React components
│   ├── ChatWidget.jsx         # Root component - manages all sub-components
│   ├── ChatWidgetIcon.jsx     # Floating chat icon with unread badge
│   ├── ChatPanel.jsx          # Main chat interface panel
│   ├── MessageList.jsx        # Display messages in chat
│   ├── MessageInput.jsx       # User input field with character counter
│   └── HighlightButton.jsx    # Floating "Ask about this" button
├── hooks/                     # Custom React hooks
│   ├── useChat.js            # Chat state management
│   └── useHighlight.js       # Text selection handling
├── services/                   # API communication
│   └── chatService.js        # Backend API client
├── styles/                     # CSS styles
│   ├── chatWidget.css         # Widget icon styling
│   ├── chatPanel.css          # Panel styling
│   └── responsive.css         # Mobile/desktop breakpoints & theming
├── utils/                      # Helper functions
│   ├── constants.js          # Configuration (API URL, timeouts, breakpoints)
│   └── formatters.js          # Message/time formatting
├── requirements.txt            # Python dependencies
├── package.json                # JavaScript dependencies
├── .env.example                # Environment variables template
└── README.md                  # This file
```

## Components Overview

### ChatWidget.jsx (Root Component)
The main component that manages the chat widget state and renders all sub-components.

### ChatWidgetIcon.jsx
Floating icon button that opens/closes the chat panel. Displays unread message badge.

### ChatPanel.jsx
Main chat interface containing:
- MessageList: Displays all messages
- MessageInput: User input field
- ChatControls: Clear chat and close buttons
- Loading indicator and error display

### MessageList.jsx
Displays chat messages with proper styling for user, assistant, and system messages.

### MessageInput.jsx
Text input component with character counter and submit button.

### HighlightButton.jsx
Floating button that appears when text is selected on the page for "Ask about this" functionality.

## Hooks

### useChat.js
Custom hook for managing chat state:
- `sendMessage(query, highlightedText)`: Send message to backend
- `clearChat()`: Clear all messages
- `toggleChat()`: Open/close chat panel
- State: `messages`, `isLoading`, `error`, `isOpen`, `unreadCount`

### useHighlight.js
Custom hook for text selection:
- Detects text selection on the page
- Validates selection (5-500 characters)
- Calculates button position
- Manages highlight state

## Services

### chatService.js
API client for communicating with backend:
- `sendMessage(query, highlightedText)`: POST /chat endpoint
- Includes timeout handling and error management

## Styles

### chatWidget.css
Styles for floating chat widget icon and badge.

### chatPanel.css
Styles for chat panel, messages, input area, and controls.

### responsive.css
Breakpoint-specific styles:
- Mobile (< 768px): Full-screen overlay
- Tablet (768px-1199px): Side panel
- Desktop (>= 1200px): Side panel

Includes CSS variables for theming with Docusaurus colors.

## Utils

### constants.js
Configuration values:
- `API_URL`: Backend API URL (from BACKEND_URL env)
- `API_TIMEOUT`: Request timeout (10 seconds)
- `MIN_QUERY_LENGTH`, `MAX_QUERY_LENGTH`: Query validation
- `MIN_HIGHLIGHT_LENGTH`, `MAX_HIGHLIGHT_LENGTH`: Highlight validation
- `MAX_MESSAGES_PER_SESSION`: FIFO message limit (50)
- Device detection helpers: `isMobile()`, `isTablet()`, `isDesktop()`

### formatters.js
Utility functions:
- `formatMessage(content)`: Format message content (line breaks)
- `formatTimestamp(timestamp)`: Format ISO timestamp to readable time
- `formatDateTime(timestamp)`: Format to date and time
- `sanitizeText(text)`: Basic XSS prevention
- `formatErrorMessage(error)`: User-friendly error messages
- `formatUserName(role)`: Map role to display name

## Integration with Docusaurus

The chat widget is injected into all Docusaurus pages via client modules:

```javascript
// In book-docusaurus/docusaurus.config.js
{
  theme: {
    clientModules: [
      require.resolve('../backend/ui_chatbot/index.js'),
    ],
  },
}
```

## Environment Variables

Create `.env` file in the backend directory:

```bash
# Backend API URL (for frontend to call)
# Local development:
BACKEND_URL=http://localhost:8000

# Or for production:
# BACKEND_URL=https://your-production-backend.com

# API Timeout (in milliseconds)
API_TIMEOUT=10000
```

## Development

### Backend Development

```bash
cd backend/ui_chatbot

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Test endpoint
curl http://localhost:8000/health
```

### Frontend Development

```bash
cd book-docusaurus

# Start Docusaurus development server
npm run start

# Open http://localhost:3000
```

## Deployment

### Local Development

1. **Start Backend API**:
   ```bash
   cd backend
   pip install -r ui_chatbot/requirements.txt
   python -m uvicorn ui_chatbot.api:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start Frontend**:
   ```bash
   cd book-docusaurus
   npm install  # First time only
   npm run start
   ```

3. **Test Locally**:
   - Open http://localhost:3000
   - Click floating chat icon
   - Type a question (e.g., "What is ROS 2?")
   - Verify AI response arrives

### Production Deployment

#### Option 1: Deploy Backend to Cloud Provider

**Using Render.com**:
1. Push code to GitHub
2. Connect GitHub repo to Render
3. Set environment variables in Render dashboard:
   ```
   BACKEND_URL=https://your-app.onrender.com
   COHERE_API_KEY=your_cohere_key
   OPENROUTER_API_KEY=your_openrouter_key
   QDRANT_URL=your_qdrant_url
   ```
4. Deploy - Render builds and starts the service
5. Update Docusaurus config to use production URL

**Using Railway.app**:
1. Connect GitHub repo to Railway
2. Set environment variables in Railway dashboard
3. Deploy - Railway builds and deploys
4. Get Railway URL and update Docusaurus config

#### Option 2: Deploy to Vercel (Frontend)

The Docusaurus book is already deployed to Vercel at https://asmaakbar88.vercel.app.

To update with production backend:

1. Deploy backend to Render/Railway/your provider
2. Get production backend URL (e.g., https://chatbot-api.onrender.com)
3. Update `book-docusaurus/docusaurus.config.js`:
   ```javascript
   // No need to change - BACKEND_URL is environment variable
   // Backend URL is configured in backend/.env or provider dashboard
   ```

4. Deploy changes to Vercel:
   ```bash
   cd book-docusaurus
   git add .
   git commit -m "Update production backend URL"
   git push origin main
   ```
   Vercel will auto-deploy on push.

### Environment Variables Summary

| Variable | Local | Production | Description |
|----------|--------|-------------|-------------|
| BACKEND_URL | `http://localhost:8000` | `https://your-backend.com` | Backend API URL |
| API_TIMEOUT | `10000` | `10000` | Request timeout in ms |
| COHERE_API_KEY | Set in `.env` | Set in provider dashboard | Cohere API key |
| OPENROUTER_API_KEY | Set in `.env` | Set in provider dashboard | OpenRouter API key |
| QDRANT_URL | Set in `.env` | Set in provider dashboard | Qdrant instance URL |

## API Endpoints

### POST /chat
Submit a query to get AI-generated response from book content.

**Request**:
```json
{
  "query": "What is ROS 2?",
  "highlighted_text": "ROS 2 is a robotic middleware...",
  "context": {
    "page_url": "https://asmaakbar88.vercel.app/docs/module-1-ros2",
    "page_title": "Module 1: ROS 2"
  }
}
```

**Response**:
```json
{
  "response_id": "response_1703926200",
  "query_id": "query_1703926198",
  "content": "ROS 2 is a robot operating system...",
  "generation_time": 1.23,
  "confidence_score": 0.85,
  "timestamp": "2025-12-30T10:30:00Z"
}
```

### GET /health
Health check endpoint for monitoring dependencies (Qdrant, Cohere, OpenAI).

**Response**:
```json
{
  "status": "healthy",
  "details": {
    "qdrant": true,
    "openai": true,
    "cohere": true,
    "overall": true
  }
}
```

## Features

### User Story 1 - Chat Interface (P1 - MVP) ✅
- Floating chat widget visible on all pages
- Send messages and receive AI responses
- Session-based chat history
- Loading indicators and error handling
- Character counter and validation
- Clear chat functionality

### User Story 2 - Highlight-to-Answer (P2) ✅
- Select text on any page
- Click "Ask about this" button
- Chat opens with highlighted context
- Response references selected text
- Highlight validation (5-500 characters)

### User Story 3 - Accessibility & Responsive (P3) ✅
- Works on desktop, tablet, and mobile
- Full keyboard navigation (Tab, Enter, Escape)
- Screen reader announcements (aria-live regions)
- ARIA labels on all interactive elements
- Focus trap in modal
- Theme-aware (inherits Docusaurus colors)
- High contrast mode support
- Reduced motion support

## Accessibility Features

### Keyboard Navigation
- **Tab/Shift+Tab**: Navigate between interactive elements
- **Enter/Space**: Activate buttons
- **Escape**: Close chat or clear text selection
- **Ctrl/Cmd+/**: Toggle chat panel

### Screen Reader Support
- `aria-label`: Descriptive labels on all buttons/inputs
- `aria-live`: Announces new messages and loading states
- `aria-modal`: Modal dialog declaration
- `aria-expanded`: Chat panel state
- `role="dialog"`: Modal container
- `role="log"`: Message list
- `role="article"`: Individual messages

### Focus Management
- Focus moves to input when chat opens
- Focus returns to icon when chat closes
- Focus trap keeps focus within open panel
- Highlight button focuses when it appears

### Responsive Design
- Mobile (< 768px): Full-screen overlay, slide-up animation
- Tablet (768px-1199px): Side panel, 400px width
- Desktop (>= 1200px): Side panel, 450px width

### Theme Integration
Uses CSS variables from Docusaurus:
- `--ifm-background-surface-color`
- `--ifm-font-color-base`
- `--ifm-color-primary`
- `--ifm-border-color`
- `--ifm-code-background`
- `--ifm-alert-warning-bg-color`
- `--ifm-alert-danger-bg-color`

## Troubleshooting

### Chat widget not showing
- Check browser console for errors
- Verify `clientModules` is configured in docusaurus.config.js
- Check that `backend/ui_chatbot/index.js` exists

### API requests failing with CORS error
- Verify CORS middleware is configured in api.py
- Check that Docusaurus URL is in `allow_origins`
- Ensure backend server is running on correct port

### Chat responses timing out
- Check backend server logs for errors
- Verify `agent_retriev.py` can connect to Qdrant
- Check that COHERE_API_KEY and OPENROUTER_API_KEY are valid

### Highlight button not appearing
- Verify selection is 5-500 characters
- Check useHighlight hook is properly initialized
- Check HighlightButton component is rendered in ChatWidget

### Focus trap not working
- Verify ChatPanel has `role="dialog"` and `aria-modal="true"`
- Check focusable elements query includes all interactive elements
- Test with Tab and Shift+Tab navigation

## See Also

- [Feature Specification](../specs/001-rag-chatbot-integration/spec.md)
- [Implementation Plan](../specs/001-rag-chatbot-integration/plan.md)
- [Data Model](../specs/001-rag-chatbot-integration/data-model.md)
- [API Contract](../specs/001-rag-chatbot-integration/contracts/api.yaml)
- [Quickstart Guide](../specs/001-rag-chatbot-integration/quickstart.md)
- [Tasks](../specs/001-rag-chatbot-integration/tasks.md)
