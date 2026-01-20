# Frontend API Contract: Todo Frontend UI

## Overview
This document defines how the frontend application will interact with the backend API, specifying expected request/response formats, authentication requirements, and error handling patterns.

## Authentication
All API requests require JWT authentication in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

The frontend should:
1. Store JWT tokens using Better Auth's cookie management
2. Include the token automatically in all API requests
3. Handle token expiration by redirecting to login page
4. Refresh tokens when needed

## Common Response Format

### Success Responses
```json
{
  "success": true,
  "data": { /* response data */ }
}
```

### Error Responses
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

## API Client Implementation

### Frontend API Client Responsibilities
1. Automatically attach JWT token to all requests
2. Handle authentication errors by redirecting to login
3. Parse common response format
4. Retry failed requests with exponential backoff
5. Cache responses where appropriate

### Expected API Endpoints Usage

#### GET /api/tasks
**Description**: Retrieve all tasks for the authenticated user

**Frontend Implementation**:
- Called when loading the task list page
- Should handle loading state display
- Should handle error display
- Should update local task state

**Expected Response**:
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": 1,
        "title": "Sample Task",
        "description": "Task description",
        "completed": false,
        "user_id": 123,
        "created_at": "2023-01-01T10:00:00Z",
        "updated_at": "2023-01-01T10:00:00Z"
      }
    ],
    "total": 1
  }
}
```

#### POST /api/tasks
**Description**: Create a new task for the authenticated user

**Frontend Implementation**:
- Called when submitting the task creation form
- Should show loading indicator
- Should update task list upon success
- Should show success/error notifications

**Expected Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "New Task Title",
    "description": "Optional task description",
    "completed": false,
    "user_id": 123,
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-01T10:00:00Z"
  }
}
```

#### GET /api/tasks/{task_id}
**Description**: Retrieve a specific task by ID for the authenticated user

**Frontend Implementation**:
- Called when viewing a specific task
- Should handle loading state
- Should handle "not found" errors

**Expected Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Sample Task",
    "description": "Task description",
    "completed": false,
    "user_id": 123,
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-01T10:00:00Z"
  }
}
```

#### PUT /api/tasks/{task_id}
**Description**: Update a specific task by ID for the authenticated user

**Frontend Implementation**:
- Called when updating task details
- Should show loading indicator
- Should update local task state upon success

**Expected Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Updated Task Title",
    "description": "Updated task description",
    "completed": true,
    "user_id": 123,
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-01T11:00:00Z"
  }
}
```

#### DELETE /api/tasks/{task_id}
**Description**: Delete a specific task by ID for the authenticated user

**Frontend Implementation**:
- Called when deleting a task
- Should show confirmation dialog
- Should update local task list upon success

**Expected Response**:
```json
{
  "success": true,
  "data": {
    "message": "Task deleted successfully"
  }
}
```

#### PATCH /api/tasks/{task_id}/toggle
**Description**: Toggle the completion status of a specific task

**Frontend Implementation**:
- Called when toggling task completion
- Should update the task status in the UI immediately
- Should handle optimistic updates

**Expected Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "completed": true,
    "updated_at": "2023-01-01T11:00:00Z"
  }
}
```

## Error Handling Patterns

### Authentication Errors (401)
- Redirect user to login page
- Clear local authentication state
- Show notification about authentication loss

### Authorization Errors (403)
- Show error message to user
- Log error for debugging
- Potentially redirect to safe page

### Validation Errors (400)
- Display specific validation errors near form fields
- Highlight invalid fields
- Provide helpful error messages

### Server Errors (500)
- Show generic error message to user
- Log error details for debugging
- Provide option to retry

### Network Errors
- Show connection error message
- Provide option to retry
- Queue operations for when connection is restored

## Loading States
The frontend should implement loading states for:
- Initial page load
- API requests
- Form submissions
- Navigation between pages

## Caching Strategy
- Cache user's task list for short periods (e.g., 30 seconds)
- Invalidate cache after mutations (create, update, delete)
- Cache user profile information
- Don't cache sensitive information

## Security Considerations
- Never expose JWT tokens in client-side code
- Validate all user input before sending to API
- Sanitize data before displaying in UI
- Implement CSRF protection
- Use HTTPS for all API communications