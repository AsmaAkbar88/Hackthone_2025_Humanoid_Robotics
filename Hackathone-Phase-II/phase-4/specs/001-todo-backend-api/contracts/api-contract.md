# API Contract: Todo Backend API

## Overview
This document defines the REST API contract for the Todo Backend API, specifying endpoints, request/response formats, and authentication requirements.

## Base URL
```
https://api.todoapp.com/v1  # Production
http://localhost:8000       # Development
```

## Authentication
All endpoints require JWT authentication in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

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

## Endpoints

### Task Management

#### GET /api/tasks
**Description**: Retrieve all tasks for the authenticated user

**Authentication**: Required
**Parameters**:
- `limit` (optional, integer, default: 20): Number of tasks to return
- `offset` (optional, integer, default: 0): Number of tasks to skip

**Response**:
- 200: Successful retrieval
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
- 401: Unauthorized
- 500: Internal server error

#### POST /api/tasks
**Description**: Create a new task for the authenticated user

**Authentication**: Required
**Request Body**:
```json
{
  "title": "New Task Title",
  "description": "Optional task description",
  "completed": false
}
```

**Response**:
- 201: Task created successfully
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
- 400: Invalid request data
- 401: Unauthorized
- 500: Internal server error

#### GET /api/tasks/{task_id}
**Description**: Retrieve a specific task by ID for the authenticated user

**Authentication**: Required
**Path Parameters**:
- `task_id` (integer): Task ID

**Response**:
- 200: Task retrieved successfully
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
- 401: Unauthorized
- 404: Task not found
- 500: Internal server error

#### PUT /api/tasks/{task_id}
**Description**: Update a specific task by ID for the authenticated user

**Authentication**: Required
**Path Parameters**:
- `task_id` (integer): Task ID

**Request Body**:
```json
{
  "title": "Updated Task Title",
  "description": "Updated task description",
  "completed": true
}
```

**Response**:
- 200: Task updated successfully
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
- 400: Invalid request data
- 401: Unauthorized
- 404: Task not found
- 500: Internal server error

#### DELETE /api/tasks/{task_id}
**Description**: Delete a specific task by ID for the authenticated user

**Authentication**: Required
**Path Parameters**:
- `task_id` (integer): Task ID

**Response**:
- 200: Task deleted successfully
```json
{
  "success": true,
  "data": {
    "message": "Task deleted successfully"
  }
}
```
- 401: Unauthorized
- 404: Task not found
- 500: Internal server error

#### PATCH /api/tasks/{task_id}/toggle
**Description**: Toggle the completion status of a specific task

**Authentication**: Required
**Path Parameters**:
- `task_id` (integer): Task ID

**Response**:
- 200: Task status toggled successfully
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
- 401: Unauthorized
- 404: Task not found
- 500: Internal server error

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| AUTH_001 | 401 | Invalid or expired token |
| AUTH_002 | 401 | Missing authorization header |
| VALIDATION_001 | 400 | Invalid request data |
| RESOURCE_001 | 404 | Resource not found |
| SERVER_001 | 500 | Internal server error |
| ACCESS_001 | 403 | Access denied - user not authorized for this resource |