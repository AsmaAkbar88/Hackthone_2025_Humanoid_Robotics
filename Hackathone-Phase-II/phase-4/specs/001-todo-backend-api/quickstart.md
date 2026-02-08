# Quickstart Guide: Todo Backend API

## Overview
This guide provides instructions for setting up and running the Todo Backend API locally.

## Prerequisites
- Python 3.11+
- Poetry or pip for dependency management
- PostgreSQL database (or Neon Serverless PostgreSQL account)
- Environment variables configured

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up Virtual Environment
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using poetry
poetry install
poetry shell
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
# Or if using poetry: poetry install
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
DEBUG=true
```

### 5. Database Setup
```bash
# Run database migrations
python -m backend.src.database.migrations

# Or if using alembic directly
alembic upgrade head
```

### 6. Run the Application
```bash
# Using uvicorn directly
uvicorn backend.src.api.main:app --reload --host 0.0.0.0 --port 8000

# Or using the run script
python -m backend.src.api.main
```

## API Testing

### 1. Get Authentication Token
First, register and authenticate a user to obtain a JWT token.

### 2. Test Endpoints
```bash
# Get all tasks for authenticated user
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     http://localhost:8000/api/tasks

# Create a new task
curl -X POST \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title":"Test Task","description":"Test Description","completed":false}' \
     http://localhost:8000/api/tasks
```

## Key Components

### Project Structure
```
backend/
├── src/
│   ├── models/           # SQLModel database models
│   ├── services/         # Business logic
│   ├── api/             # FastAPI application and routes
│   ├── database/        # Database connection and migrations
│   └── utils/           # Utility functions
└── tests/               # Test suite
```

### Authentication
All API endpoints require JWT authentication. Include the Authorization header with the format: `Bearer <token>`

### Error Handling
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

## Troubleshooting

### Common Issues
1. **Database Connection**: Ensure PostgreSQL is running and credentials are correct
2. **JWT Authentication**: Verify the `BETTER_AUTH_SECRET` matches the token signing key
3. **Migration Errors**: Run migrations with `alembic upgrade head`
4. **Port Already in Use**: Change the port in the uvicorn command

### Environment Variables
- `DATABASE_URL`: Database connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT token signing
- `DEBUG`: Enable/disable debug mode
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS