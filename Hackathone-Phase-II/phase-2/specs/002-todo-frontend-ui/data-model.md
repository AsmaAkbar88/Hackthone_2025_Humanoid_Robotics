# Data Model: Todo Frontend UI

## Entities

### Task
**Description**: Represents a user's task with properties like title, description, completion status, and timestamps. Displayed in the UI for user interaction.

**Fields**:
- id: string/number (Unique identifier for the task)
- title: string (Required, Max length: 255)
- description: string (Optional, Max length: 1000)
- completed: boolean (Default: false)
- userId: string/number (Identifier of the user who owns the task)
- createdAt: Date (Timestamp when task was created)
- updatedAt: Date (Timestamp when task was last updated)

**State Transitions**:
- `created`: Task is initially created with completed=false
- `updated`: Task details (title, description) can be modified
- `toggled`: Task completion status can be toggled
- `deleted`: Task can be deleted

**Validation Rules**:
- Title must not be empty
- Title must be between 1-255 characters
- Description, if provided, must be between 1-1000 characters

### User
**Description**: Represents an authenticated user with identity information used for authentication and task ownership verification.

**Fields**:
- id: string/number (Unique identifier for the user)
- email: string (Required, Unique, Valid email format)
- name: string (Optional, Max length: 255)
- createdAt: Date (Timestamp when user account was created)
- lastLoginAt: Date (Timestamp of last login)

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users

## Frontend State Objects

### TaskState
**Description**: Represents the state of tasks in the frontend application.

**Fields**:
- tasks: Array<Task> (List of all tasks for the current user)
- loading: boolean (Indicates if tasks are being loaded)
- error: string/null (Error message if task loading failed)
- currentFilter: 'all' | 'active' | 'completed' (Current filter applied to task list)

### AuthState
**Description**: Represents the authentication state in the frontend application.

**Fields**:
- user: User/null (Current authenticated user, null if not logged in)
- loading: boolean (Indicates if auth status is being determined)
- error: string/null (Error message if authentication failed)
- isAuthenticated: boolean (Whether user is currently authenticated)

### Notification
**Description**: Represents a notification/toast message in the UI.

**Fields**:
- id: string/number (Unique identifier for the notification)
- type: 'success' | 'error' | 'warning' | 'info' (Type of notification)
- message: string (The message to display)
- duration: number (How long to show the notification in milliseconds)
- visible: boolean (Whether the notification is currently visible)