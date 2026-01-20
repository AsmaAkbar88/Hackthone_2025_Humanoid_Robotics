# Data Model: Authentication System Enhancement

## Entities

### User Account
- **Fields**:
  - id (UUID/string): Unique identifier for the user
  - email (string): User's email address, must be unique and properly formatted
  - password_hash (string): Securely hashed password
  - signup_date (timestamp): Date and time when account was created (non-nullable)
  - created_at (timestamp): Record creation timestamp
  - updated_at (timestamp): Record last update timestamp
- **Validation rules**:
  - Email must pass standard email validation
  - Password must meet security requirements
  - Signup date must be a valid timestamp and cannot be NULL
- **State transitions**: N/A for this entity

### Authentication Session
- **Fields**:
  - session_id (string): Unique session identifier
  - user_id (UUID/string): Reference to associated user account
  - jwt_token (string): JSON Web Token for session management
  - expires_at (timestamp): Session expiration time
  - created_at (timestamp): Session creation timestamp
- **Validation rules**:
  - JWT token must be properly formatted
  - Session must expire within defined timeframe
- **State transitions**: Active → Expired

### Signup Date
- **Fields**:
  - date_value (timestamp): The specific date and time of signup (non-nullable)
  - timezone_offset (integer): Optional timezone information for accurate recording
- **Validation rules**:
  - Must be a valid timestamp
  - Cannot be NULL
  - Should represent the moment of account creation
- **State transitions**: N/A

## Relationships
- User Account (1) → Authentication Session (Many): One user can have multiple sessions
- User Account (1) → Signup Date (1): Each user account has exactly one signup date