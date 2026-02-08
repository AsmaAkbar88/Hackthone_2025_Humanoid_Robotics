# Quickstart Guide: Todo Web App Security Implementation

## Prerequisites

- Python 3.11+ with pip
- Node.js 18+ with npm/yarn
- Better Auth configured with BETTER_AUTH_SECRET environment variable
- Neon PostgreSQL database setup

## Environment Setup

### Backend Configuration
```bash
# Set up backend environment variables
export BETTER_AUTH_SECRET="your-jwt-secret-here"
export DATABASE_URL="your-neon-postgres-url"
```

### Frontend Configuration
```bash
# Set up frontend environment variables
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:8000"  # Backend URL
```

## Security Architecture Components

### Backend JWT Middleware
The security implementation includes centralized JWT verification middleware that:

1. Intercepts all incoming API requests
2. Verifies JWT token signature using BETTER_AUTH_SECRET
3. Extracts user identity from token claims
4. Attaches user context to request object
5. Returns 401 Unauthorized for invalid tokens

### User Ownership Validation
All task operations include user ownership validation:

1. Extract user ID from JWT token
2. Compare with task's userId field
3. Allow operation only if IDs match
4. Return 401 Unauthorized for mismatched ownership

### Frontend Auth State Management
The frontend implements secure authentication state management:

1. Stores JWT tokens securely (preferably HTTP-only cookies)
2. Intercepts all API requests to add Authorization header
3. Handles 401 responses by redirecting to login
4. Clears auth state on logout or session expiration

## Running the Application

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m src.main  # Start the FastAPI server
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev  # Start the Next.js development server
```

## Key Security Features

### Authentication Enforcement
- All API endpoints require valid JWT tokens in Authorization header
- Invalid or missing tokens result in 401 Unauthorized responses
- Token expiration is strictly enforced

### Task Ownership
- Users can only access tasks they own
- Cross-user access attempts are blocked with 401 responses
- Database queries are filtered by authenticated user ID

### Session Management
- Stateless authentication using JWT tokens
- Secure token storage and transmission
- Proper handling of token expiration

## API Usage Examples

### Authenticating a User
```javascript
// Login request
fetch('/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'securePassword'
  })
})
.then(response => response.json())
.then(data => {
  // Store JWT token securely
  localStorage.setItem('authToken', data.token);
});
```

### Making Authenticated Requests
```javascript
// Include JWT token in all subsequent requests
fetch('/api/tasks', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
  }
})
.then(response => response.json());
```

### Handling Authentication Errors
```javascript
// Frontend should handle 401 responses
fetch('/api/tasks', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
.then(response => {
  if (response.status === 401) {
    // Redirect to login page
    window.location.href = '/login';
    return;
  }
  return response.json();
});
```

## Testing Security Features

### Unit Tests
- JWT token validation tests
- User ownership verification tests
- Authentication middleware tests

### Integration Tests
- End-to-end authentication flow
- Cross-user access prevention
- Token expiration handling

### Security Tests
- Attempting access without tokens
- Using invalid/expired tokens
- Cross-user data access attempts