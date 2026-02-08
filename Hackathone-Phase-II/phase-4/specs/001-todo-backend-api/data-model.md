# Data Model: Todo Backend API

## Entities

### Task
**Description**: Represents a user's task with properties like title, description, completion status, and creation timestamp. Associated with a specific user.

**Fields**:
- id: Integer (Primary Key, Auto-generated)
- title: String (Required, Max length: 255)
- description: String (Optional, Max length: 1000)
- completed: Boolean (Default: False)
- user_id: Integer (Foreign Key to User, Required)
- created_at: DateTime (Auto-generated, UTC)
- updated_at: DateTime (Auto-generated, UTC, Updates on modification)

**Relationships**:
- Belongs to: User (Many-to-One relationship)

**Validation Rules**:
- Title must not be empty
- Title must be between 1-255 characters
- Description, if provided, must be between 1-1000 characters
- Task can only be modified by the owner user

### User
**Description**: Represents an authenticated user with unique identifier used to control task access permissions.

**Fields**:
- id: Integer (Primary Key, Auto-generated)
- email: String (Required, Unique, Max length: 255)
- created_at: DateTime (Auto-generated, UTC)
- updated_at: DateTime (Auto-generated, UTC, Updates on modification)

**Relationships**:
- Has many: Tasks (One-to-Many relationship)

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users

## State Transitions

### Task State Transitions
- `created`: Task is initially created with completed=False
- `updated`: Task details (title, description) can be modified by owner
- `completed`: Task status can be toggled to True by owner
- `deleted`: Task can be deleted by owner

## Database Schema Considerations

### Indexes
- Index on user_id for efficient user-based filtering
- Index on created_at for chronological ordering
- Composite index on (user_id, created_at) for optimized user timeline queries

### Constraints
- Foreign key constraint on user_id referencing users table
- Cascade delete: When user is deleted, all their tasks are deleted
- Check constraint: Prevent modification of task by non-owner user (enforced in application logic)