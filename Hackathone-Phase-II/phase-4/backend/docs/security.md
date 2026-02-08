# Security Documentation: Todo Web App

## JWT Authentication

### Overview
The application uses JWT (JSON Web Tokens) for stateless authentication. All API requests require a valid JWT token in the Authorization header.

### Token Structure
- Algorithm: HS256
- Payload includes:
  - `sub`: User ID (subject)
  - `exp`: Expiration timestamp
  - `iat`: Issued at timestamp

### Configuration
- Environment variable: `BETTER_AUTH_SECRET`
- Expiration time: 30 minutes (configurable in settings)
- Algorithm: HS256

### Token Lifecycle
1. User authenticates with credentials
2. Server generates JWT with user ID as subject
3. Token is returned to client and stored securely
4. Client includes token in Authorization header for all requests
5. Server validates token signature and expiration
6. Token grants access to user-specific resources only

## Authorization & Access Control

### Task Ownership
- Each task is associated with a specific user via `user_id`
- Users can only access, modify, or delete their own tasks
- Attempts to access other users' tasks result in 401 Unauthorized

### API Endpoints Protection
All API endpoints require valid authentication except:
- `/api/auth/login` - for authentication
- `/api/auth/register` - for registration
- `/api/health` - for health checks

## Session Management

### Client-Side
- Tokens stored in localStorage (production apps should consider HttpOnly cookies)
- Token expiration checked before requests
- Automatic logout on 401 responses
- Redirect to login page after session expiration

### Security Headers
- All API responses include appropriate security headers
- CORS configured for allowed origins only
- Content Security Policy implemented

## Error Handling

### 401 Unauthorized Scenarios
- Missing Authorization header
- Invalid JWT token format
- Expired JWT token
- Tampered JWT token
- User account deactivated

### Response Format
```json
{
  "success": false,
  "error": {
    "code": "AUTH_001",
    "message": "Could not validate credentials"
  }
}
```

## Best Practices

### For Developers
1. Always validate user ownership before performing operations
2. Sanitize and validate all inputs
3. Use parameterized queries to prevent SQL injection
4. Log security-relevant events appropriately
5. Never expose sensitive data in error messages

### For Operations
1. Rotate JWT secrets regularly
2. Monitor authentication failure logs
3. Implement rate limiting for auth endpoints
4. Use HTTPS in all environments
5. Regular security audits of dependencies

## Environment Variables

Required environment variables for security:
- `BETTER_AUTH_SECRET`: Secret key for JWT signing (minimum 32 characters)
- `DATABASE_URL`: Secure database connection string
- `DATABASE_ECHO`: Set to "False" in production

## Compliance

This implementation follows industry-standard security practices:
- OWASP Top 10 compliance
- Statelessness of JWT tokens
- Proper error handling without information disclosure
- Input validation and sanitization
- Principle of least privilege for access control