# Data Model: Todo Web App Security

## Entity Definitions

### JWT Token
- **Description**: Represents user authentication state with expiration
- **Fields**:
  - `token`: String (the JWT token string)
  - `userId`: String (identifier of the authenticated user)
  - `expiresAt`: DateTime (expiration timestamp)
  - `issuedAt`: DateTime (issue timestamp)
  - `claims`: Object (user identity claims)
- **Relationships**: Belongs to a User
- **Validation**: Must have valid JWT format, not expired

### User
- **Description**: Identity associated with authenticated sessions and task ownership
- **Fields**:
  - `id`: String (unique user identifier)
  - `email`: String (user's email address)
  - `createdAt`: DateTime (account creation timestamp)
  - `updatedAt`: DateTime (last update timestamp)
- **Relationships**: Owns many Tasks
- **Validation**: Email must be valid format, id must be unique

### Task
- **Description**: Data entity that belongs to a specific user, accessible only by the owner
- **Fields**:
  - `id`: String (unique task identifier)
  - `title`: String (task title)
  - `description`: Text (optional task description)
  - `completed`: Boolean (completion status)
  - `userId`: String (foreign key to owning user)
  - `createdAt`: DateTime (creation timestamp)
  - `updatedAt`: DateTime (last update timestamp)
- **Relationships**: Belongs to a User
- **Validation**: Must have a valid userId, title must not be empty

### Authentication Session
- **Description**: Server-side representation of active user session (for stateless auth)
- **Fields**:
  - `tokenId`: String (reference to JWT token)
  - `userId`: String (authenticated user)
  - `isActive`: Boolean (session validity status)
  - `lastAccessed`: DateTime (last activity timestamp)
- **Relationships**: Links JWT Token to User
- **Validation**: Must correspond to valid user and unexpired token

## Security-Specific Models

### AuthenticatedRequest
- **Description**: Represents an API request with attached authentication context
- **Fields**:
  - `requestId`: String (unique request identifier)
  - `endpoint`: String (requested API endpoint)
  - `method`: String (HTTP method)
  - `userId`: String (authenticated user, if applicable)
  - `timestamp`: DateTime (request timestamp)
  - `authStatus`: Enum ['valid', 'invalid', 'missing'] (authentication status)
- **Validation**: Must have valid endpoint format and method

### SecurityLog
- **Description**: Audit trail for authentication and authorization events
- **Fields**:
  - `id`: String (unique log entry identifier)
  - `eventType`: Enum ['login', 'logout', 'auth_failure', 'access_denied']
  - `userId`: String (affected user, if known)
  - `ipAddress`: String (client IP address)
  - `timestamp`: DateTime (event timestamp)
  - `details`: Text (additional event details)
- **Validation**: Must have valid event type and timestamp

## Validation Rules from Requirements

### Authentication Validation
- All API requests must include a valid JWT token in the Authorization header
- JWT tokens must be verified using the BETTER_AUTH_SECRET
- Expired tokens must be rejected with 401 Unauthorized response

### Authorization Validation
- Users can only access tasks they own (based on userId field)
- Requests for tasks belonging to other users must return 401 Unauthorized
- All task operations (create, read, update, delete) must verify user ownership

### Data Integrity Validation
- Task userId field must correspond to an existing User record
- JWT tokens must have valid format and not be expired
- User identifiers in tokens must correspond to existing User records

## State Transitions

### JWT Token Lifecycle
1. **Issued**: Token is created upon successful authentication
2. **Active**: Token is valid and can be used for API requests
3. **Expired**: Token has passed its expiration time, becomes invalid
4. **Revoked**: Token is invalidated before natural expiration (logout)

### Task Ownership Verification
1. **Requested**: API request arrives with JWT token and task identifier
2. **Authenticated**: JWT token is validated, user identity extracted
3. **Authorized**: User's identity is compared with task's userId
4. **Approved/Denied**: Request proceeds or returns 401 Unauthorized

## Relationships and Constraints

### User-Task Relationship
- One-to-Many: One User can own many Tasks
- Foreign Key Constraint: Task.userId must reference existing User.id
- Cascade Behavior: When User is deleted, their Tasks should also be deleted
- Access Control: Only the owning User can access a specific Task

### JWT-User Relationship
- Many-to-One: Many JWT tokens can be associated with one User (across different sessions)
- Validation: JWT claims must contain valid User.id
- Security: Tokens must be signed with BETTER_AUTH_SECRET to be valid