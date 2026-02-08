# API Contracts: Todo Web App Security

## Authentication Endpoints

### POST /api/auth/login
**Purpose**: Authenticate user and return JWT token

**Request**:
- Headers: None required
- Body:
  ```json
  {
    "email": "string (user email)",
    "password": "string (user password)"
  }
  ```

**Success Response (200)**:
- Headers: None
- Body:
  ```json
  {
    "token": "string (JWT token)",
    "user": {
      "id": "string (user ID)",
      "email": "string (user email)"
    },
    "expiresAt": "string (ISO 8601 timestamp)"
  }
  ```

**Error Response (401)**:
- Headers: None
- Body:
  ```json
  {
    "error": "string (error message)",
    "code": "AUTHENTICATION_FAILED"
  }
  ```

### POST /api/auth/logout
**Purpose**: Invalidate current session (stateless - client removes token)

**Request**:
- Headers:
  - Authorization: "Bearer {valid JWT token}"
- Body: `{}`

**Success Response (200)**:
- Headers: None
- Body:
  ```json
  {
    "message": "Successfully logged out"
  }
  ```

**Error Response (401)**:
- Headers: None
- Body:
  ```json
  {
    "error": "string (error message)",
    "code": "UNAUTHORIZED"
  }
  ```

## Protected Task Endpoints

### GET /api/tasks
**Purpose**: Retrieve all tasks belonging to authenticated user

**Request**:
- Headers:
  - Authorization: "Bearer {valid JWT token}"
- Query Parameters: None
- Body: None

**Success Response (200)**:
- Headers: None
- Body:
  ```json
  {
    "tasks": [
      {
        "id": "string (task ID)",
        "title": "string (task title)",
        "description": "string (task description)",
        "completed": "boolean (completion status)",
        "userId": "string (owner user ID)",
        "createdAt": "string (ISO 8601 timestamp)",
        "updatedAt": "string (ISO 8601 timestamp)"
      }
    ]
  }
  ```

**Error Response (401)**:
- Headers: None
- Body:
  ```json
  {
    "error": "string (error message)",
    "code": "UNAUTHORIZED"
  }
  ```

### POST /api/tasks
**Purpose**: Create a new task for authenticated user

**Request**:
- Headers:
  - Authorization: "Bearer {valid JWT token}"
- Body:
  ```json
  {
    "title": "string (task title)",
    "description": "string (optional task description)"
  }
  ```

**Success Response (201)**:
- Headers: Location: "/api/tasks/{new_task_id}"
- Body:
  ```json
  {
    "id": "string (new task ID)",
    "title": "string (task title)",
    "description": "string (task description)",
    "completed": "false",
    "userId": "string (owner user ID)",
    "createdAt": "string (ISO 8601 timestamp)",
    "updatedAt": "string (ISO 8601 timestamp)"
  }
  ```

**Error Response (401)**:
- Headers: None
- Body:
  ```json
  {
    "error": "string (error message)",
    "code": "UNAUTHORIZED"
  }
  ```

### GET /api/tasks/{taskId}
**Purpose**: Retrieve a specific task if it belongs to authenticated user

**Request**:
- Headers:
  - Authorization: "Bearer {valid JWT token}"
- Path Parameters:
  - taskId: "string (ID of task to retrieve)"
- Body: None

**Success Response (200)**:
- Headers: None
- Body:
  ```json
  {
    "id": "string (task ID)",
    "title": "string (task title)",
    "description": "string (task description)",
    "completed": "boolean (completion status)",
    "userId": "string (owner user ID)",
    "createdAt": "string (ISO 8601 timestamp)",
    "updatedAt": "string (ISO 8601 timestamp)"
  }
  ```

**Error Response (401)**:
- Headers: None
- Body:
  ```json
  {
    "error": "string (error message)",
    "code": "UNAUTHORIZED"
  }
  ```

**Error Response (404)**:
- Headers: None
- Body:
  ```json
  {
    "error": "string (error message)",
    "code": "TASK_NOT_FOUND"
  }
  ```

### PUT /api/tasks/{taskId}
**Purpose**: Update a specific task if it belongs to authenticated user

**Request**:
- Headers:
  - Authorization: "Bearer {valid JWT token}"
- Path Parameters:
  - taskId: "string (ID of task to update)"
- Body:
  ```json
  {
    "title": "string (updated task title)",
    "description": "string (updated task description)",
    "completed": "boolean (updated completion status)"
  }
  ```

**Success Response (200)**:
- Headers: None
- Body:
  ```json
  {
    "id": "string (task ID)",
    "title": "string (updated task title)",
    "description": "string (updated task description)",
    "completed": "boolean (updated completion status)",
    "userId": "string (owner user ID)",
    "createdAt": "string (original creation timestamp)",
    "updatedAt": "string (updated ISO 8601 timestamp)"
  }
  ```

**Error Response (401)**:
- Headers: None
- Body:
  ```json
  {
    "error": "string (error message)",
    "code": "UNAUTHORIZED"
  }
  ```

**Error Response (404)**:
- Headers: None
- Body:
  ```json
  {
    "error": "string (error message)",
    "code": "TASK_NOT_FOUND"
  }
  ```

### DELETE /api/tasks/{taskId}
**Purpose**: Delete a specific task if it belongs to authenticated user

**Request**:
- Headers:
  - Authorization: "Bearer {valid JWT token}"
- Path Parameters:
  - taskId: "string (ID of task to delete)"
- Body: None

**Success Response (204)**:
- Headers: None
- Body: None

**Error Response (401)**:
- Headers: None
- Body:
  ```json
  {
    "error": "string (error message)",
    "code": "UNAUTHORIZED"
  }
  ```

**Error Response (404)**:
- Headers: None
- Body:
  ```json
  {
    "error": "string (error message)",
    "code": "TASK_NOT_FOUND"
  }
  ```

## Security Headers and Behaviors

### Authorization Header Format
All authenticated requests must include the Authorization header with the format:
```
Authorization: Bearer {jwt_token}
```

### Common Error Responses
All endpoints may return these error responses:
- **401 Unauthorized**: Missing, invalid, or expired JWT token
- **500 Internal Server Error**: Unexpected server error during processing

### Security Behaviors
- All endpoints require valid JWT authentication unless explicitly noted
- JWT tokens must be verified using BETTER_AUTH_SECRET
- User ownership verification must occur for all task operations
- Expired JWT tokens must be rejected with 401 Unauthorized
- All timestamps must be in ISO 8601 format