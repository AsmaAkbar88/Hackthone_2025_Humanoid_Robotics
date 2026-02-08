# API Contracts: AI Chatbot Interface for Todo Application

## Overview
API contracts for the AI Chatbot Interface feature, defining endpoints for chat functionality while maintaining compatibility with existing authentication and task management systems.

## Chat Endpoint

### POST /api/{user_id}/chat
Process natural language input from user and return AI-generated response with appropriate task operations.

**Headers**:
- Authorization: Bearer {JWT_TOKEN} (required)

**Path Parameters**:
- user_id: integer (must match authenticated user ID)

**Request Body**:
```json
{
  "message": "Natural language command to process",
  "conversation_id": "Optional conversation ID to continue existing conversation"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "response": "AI-generated response",
    "conversation_id": "ID of the conversation",
    "actions_taken": [
      {
        "action": "task_created|task_updated|task_deleted|task_completed",
        "task_id": "ID of affected task (if applicable)",
        "details": "Description of action taken"
      }
    ]
  }
}
```

**Error Responses**:
- 400: Bad Request - Invalid request format
- 401: Unauthorized - Invalid or missing JWT token
- 403: Forbidden - User attempting to access another user's chat endpoint
- 422: Unprocessable Entity - Unable to process the natural language command
- 500: Internal Server Error - Unexpected error during processing

## Conversation Management Endpoints

### GET /api/{user_id}/conversations
Retrieve list of conversation summaries for the authenticated user.

**Headers**:
- Authorization: Bearer {JWT_TOKEN} (required)

**Path Parameters**:
- user_id: integer (must match authenticated user ID)

**Response**:
```json
{
  "success": true,
  "data": {
    "conversations": [
      {
        "id": "conversation ID",
        "title": "conversation title",
        "created_at": "ISO 8601 timestamp",
        "updated_at": "ISO 8601 timestamp"
      }
    ],
    "total": "total number of conversations"
  }
}
```

### GET /api/{user_id}/conversations/{conversation_id}
Retrieve full conversation history with messages.

**Headers**:
- Authorization: Bearer {JWT_TOKEN} (required)

**Path Parameters**:
- user_id: integer (must match authenticated user ID)
- conversation_id: integer (conversation ID)

**Response**:
```json
{
  "success": true,
  "data": {
    "conversation": {
      "id": "conversation ID",
      "title": "conversation title",
      "created_at": "ISO 8601 timestamp",
      "updated_at": "ISO 8601 timestamp",
      "messages": [
        {
          "id": "message ID",
          "role": "user|assistant|system",
          "content": "message content",
          "timestamp": "ISO 8601 timestamp"
        }
      ]
    }
  }
}
```

## Existing Endpoints (Remain Unchanged)
All existing task and authentication endpoints remain the same to preserve backward compatibility:

- POST /api/tasks (create task)
- GET /api/tasks (list tasks)
- GET /api/tasks/{task_id} (get specific task)
- PUT /api/tasks/{task_id} (update task)
- DELETE /api/tasks/{task_id} (delete task)
- PATCH /api/tasks/{task_id}/toggle (toggle task completion)
- All authentication endpoints under /api/auth

## Security Considerations
- All endpoints require valid JWT authentication
- User ID in path parameter must match authenticated user
- Conversation and message data is isolated by user ID
- MCP tools enforce proper authorization for task operations