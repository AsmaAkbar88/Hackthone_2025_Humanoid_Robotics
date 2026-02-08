# Todo Backend API Documentation

## Overview
The Todo Backend API is a secure, RESTful API built with FastAPI for managing personal tasks. It provides endpoints for creating, reading, updating, and deleting tasks with strict user-based access controls.

## Features
- JWT-based authentication
- User isolation - users can only access their own tasks
- Comprehensive error handling
- Async database operations with SQLModel
- Full CRUD operations for tasks

## Getting Started

### Prerequisites
- Python 3.11+
- Poetry (recommended) or pip
- PostgreSQL database

### Installation
1. Clone the repository
2. Install dependencies: `poetry install` or `pip install -r requirements.txt`
3. Set up environment variables (see .env.example)
4. Run database migrations: `alembic upgrade head`
5. Start the server: `uvicorn backend.src.api.main:app --reload`

### Environment Variables
- `DATABASE_URL`: Database connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT token signing
- `DEBUG`: Enable/disable debug mode

## API Endpoints

### Authentication
All endpoints require JWT authentication in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

### Tasks
- `GET /api/tasks` - Get all tasks for the authenticated user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a specific task
- `DELETE /api/tasks/{task_id}` - Delete a specific task
- `PATCH /api/tasks/{task_id}/toggle` - Toggle task completion status

## Error Handling
All errors follow the standard format:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

## Security
- All endpoints require authentication
- Users can only access their own tasks
- Input validation on all endpoints
- Secure JWT token handling