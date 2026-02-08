# Quickstart Guide: AI Chatbot Interface for Todo Application

## Overview
Quickstart guide for developers to understand and begin working with the AI Chatbot Interface feature.

## Prerequisites
- Python 3.11+ with pip
- Node.js 18+ with npm/yarn
- Neon PostgreSQL database account
- OpenAI API key
- MCP SDK installation

## Environment Setup

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in `.env`:
   ```
   DATABASE_URL=your_neon_postgresql_connection_string
   OPENAI_API_KEY=your_openai_api_key
   SECRET_KEY=your_secret_key_for_jwt
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. Run database migrations:
   ```bash
   python -m src.database.migrate
   ```

5. Start the backend server:
   ```bash
   python -m src.api.main
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install JavaScript dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables in `.env.local`:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXT_PUBLIC_OPENAI_API_KEY=your_openai_api_key
   ```

4. Start the frontend development server:
   ```bash
   npm run dev
   ```

## Key Components

### MCP Tools
The AI Chatbot uses Model Context Protocol (MCP) tools to perform actions:
- `add_task`: Creates a new task based on natural language input
- `list_tasks`: Retrieves user's tasks with filtering options
- `update_task`: Updates an existing task
- `delete_task`: Removes a task
- `complete_task`: Marks a task as completed

### Database Models
- `Conversation`: Stores conversation threads with user association
- `Message`: Stores individual messages within conversations
- Existing `Task` and `User` models remain unchanged

### API Endpoints
- `POST /api/{user_id}/chat`: Main endpoint for chat interactions
- `GET /api/{user_id}/conversations`: Retrieve user's conversation list
- `GET /api/{user_id}/conversations/{conversation_id}`: Get specific conversation history

## Development Workflow

### Adding New MCP Tools
1. Create the tool function in `backend/src/services/ai_service.py`
2. Register the tool with the MCP server
3. Update the contracts documentation

### Modifying Chat Interface
1. Update components in `frontend/src/components/chat/`
2. Modify the chat page in `frontend/src/app/chat/page.tsx`
3. Update the chat hook in `frontend/src/hooks/useChat.js`

### Testing the Feature
1. Create a user account through the UI or API
2. Start a new conversation in the chat interface
3. Use natural language commands like:
   - "Add a task to buy groceries"
   - "Show me my tasks"
   - "Mark task 1 as complete"
   - "Delete task 2"

## Common Tasks

### Running Tests
Backend tests:
```bash
cd backend
pytest tests/
```

Frontend tests:
```bash
cd frontend
npm run test
```

### Database Migrations
When adding new models (Conversation, Message):
```bash
cd backend
python -m src.database.migrate
```

### Updating Dependencies
Backend:
```bash
cd backend
pip install -r requirements.txt --upgrade
```

Frontend:
```bash
cd frontend
npm update
```

## Troubleshooting

### Chat endpoint returning 401
- Verify JWT token is included in request headers
- Confirm user authentication is working

### AI not processing commands correctly
- Check OpenAI API key is valid
- Verify MCP tools are properly registered
- Review natural language processing logs

### Conversation history not persisting
- Confirm database migrations are applied
- Verify Conversation and Message models are properly configured
- Check database connection settings