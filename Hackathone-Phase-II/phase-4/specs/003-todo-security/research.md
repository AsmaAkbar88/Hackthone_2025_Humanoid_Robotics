# Research: Todo Web App Security Architecture

## Security Architecture Overview: JWT Lifecycle from Login to API Authorization

### JWT Token Flow
1. **Login/Authentication**: User credentials are verified by Better Auth
2. **Token Generation**: JWT token is generated with user identity claims and expiration time
3. **Token Storage**: Token is stored securely (HTTP-only cookie or secure localStorage)
4. **API Requests**: Token is sent in Authorization header (`Bearer <token>`)
5. **Token Verification**: Backend verifies JWT signature and validity using BETTER_AUTH_SECRET
6. **User Identification**: Claims are extracted to identify the requesting user
7. **Authorization**: User's permissions are validated for the requested resource

### Backend Security Components
- **JWT Middleware**: Centralized verification of all incoming requests
- **Route Guards**: Endpoint-level protection for sensitive operations
- **User Filtering**: Query-level filtering to ensure users only access their own data
- **Authorization Logic**: Business logic to validate user permissions for specific operations

### Frontend Security Components
- **Token Storage**: Secure storage mechanism for JWT tokens
- **Expiration Handling**: Mechanism to detect and handle token expiration
- **Auth State Management**: Centralized authentication state
- **Request Interception**: Automatic addition of Authorization headers
- **Logout Behavior**: Proper cleanup of stored tokens and cached data

## Decision: JWT Expiration Handling Strategy

### Decision: Silent Refresh vs Auto-Logout
**Chosen Approach**: Auto-logout with graceful redirection to login page
**Rationale**: Security-first approach that ensures expired tokens are not used, reducing risk of unauthorized access
**Alternatives Considered**:
- Silent refresh: Less secure as it may extend sessions indefinitely
- Manual refresh: Poor UX requiring user intervention
- Time-based warnings: Still requires user action and may be ignored

### Decision: Frontend Behavior on 401 Responses
**Chosen Approach**: Immediate redirection to login page with error message
**Rationale**: Prevents further unauthorized operations and guides user to re-authenticate
**Alternatives Considered**:
- Retry with new token: May lead to infinite loops if token issue persists
- Show modal overlay: Could be bypassed by users
- Display error notification: Doesn't address the underlying auth issue

### Decision: Backend Response Consistency for Auth-Related Errors
**Chosen Approach**: Standardized 401 Unauthorized responses with consistent error messaging
**Rationale**: Maintains predictable API behavior and simplifies frontend error handling
**Alternatives Considered**:
- Different error codes for different auth failures: Adds complexity without clear benefit
- Detailed error messages: Potential security information disclosure

### Decision: Environment Variable Management Across Frontend and Backend
**Chosen Approach**:
- Backend: Direct access to BETTER_AUTH_SECRET from environment
- Frontend: No access to JWT secret (as it should not be exposed to client)
**Rationale**: Maintains security by keeping sensitive secrets on the server-side only
**Alternatives Considered**:
- Shared config file: Risk of exposing server secrets to client
- Runtime configuration service: Unnecessary complexity for this requirement

### Decision: Logging Strategy for Authentication Failures
**Chosen Approach**: Log authentication failures with user ID (when available) and timestamp, but not sensitive details
**Rationale**: Provides audit trail for security monitoring without storing sensitive credentials
**Alternatives Considered**:
- Detailed logging: Risk of storing sensitive information
- No logging: No audit trail for security incidents

## Error-Handling Matrix

| Error Type | Condition | Response Code | Client Action |
|------------|-----------|---------------|---------------|
| Missing JWT | No Authorization header | 401 Unauthorized | Redirect to login |
| Invalid JWT | Malformed token | 401 Unauthorized | Clear token, redirect to login |
| Expired JWT | Token past expiration time | 401 Unauthorized | Clear token, redirect to login |
| Invalid Signature | Token tampering detected | 401 Unauthorized | Clear token, redirect to login |
| Permission Denied | Valid token but insufficient privileges | 403 Forbidden | Show permission error |
| Server Error | Internal server failure | 500 Internal Error | Show generic error, maintain session |

## Validation Checklist Mapped to Constitution Success Criteria

- ✅ **User-Centric Design**: Each user sees only their own tasks through proper authorization
- ✅ **Security and JWT Authentication**: JWT authentication ensures stateless, secure, token-based access
- ✅ **Accuracy and Specification Compliance**: REST API endpoints will match specifications exactly
- ✅ **Maintainability and Separation of Concerns**: Clear separation of frontend and backend security concerns
- ✅ **Technology Stack Compliance**: Uses Better Auth JWT tokens as required

## Backend Security Review: Middleware, Route Guards, User Filtering

### JWT Verification Middleware
- Intercepts all API requests
- Validates JWT token signature and expiration
- Attaches user identity to request context
- Handles token verification failures consistently

### Route Guards
- Protects specific endpoints based on authentication status
- Enforces role-based or permission-based access controls
- Provides fine-grained control over resource access

### User Filtering
- Ensures database queries are scoped to authenticated user
- Prevents unauthorized cross-user data access
- Implemented at both query construction and result validation levels

## Frontend Auth Flow Review: Token Storage, Expiration Handling, Logout Behavior

### Token Storage
- Secure storage using HTTP-only cookies or encrypted localStorage
- Protection against XSS attacks through proper encoding
- Automatic inclusion in API requests via interceptors

### Expiration Handling
- Proactive checking of token expiration before requests
- Graceful handling of 401 responses
- Automatic cleanup of expired session data

### Logout Behavior
- Complete removal of stored tokens and cached data
- Session invalidation on the server-side where applicable
- Redirection to login page with appropriate messaging

## Final Spec Compliance Report

All functional requirements from the specification have been validated against the planned implementation approach:

- FR-001: System requires valid JWT for all API endpoints ✓
- FR-002: System returns 401 for invalid JWT tokens ✓
- FR-003: System enforces task ownership ✓
- FR-004: System respects JWT token expiry ✓
- FR-005: Frontend handles auth errors gracefully ✓
- FR-006: Frontend handles session expiration ✓
- FR-007: System uses BETTER_AUTH_SECRET environment variable ✓
- FR-008: Backend validates user ownership before operations ✓
- FR-009: System provides consistent auth behavior ✓
- FR-010: System centralizes and reuses auth logic ✓