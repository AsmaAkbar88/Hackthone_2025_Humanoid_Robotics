# Data Model: In-Memory Python Console Todo Application

**Feature**: 1-console-todo-app
**Created**: 2026-01-11
**Model**: Todo Entity and Manager

## Todo Entity

### Attributes
- **id**: `int` (Required, Unique, Auto-generated)
  - Sequential identifier starting from 1
  - Used to reference specific tasks in operations
  - Never changes once assigned

- **title**: `str` (Required, Non-empty)
  - Text description of the task
  - Maximum length: 500 characters
  - Cannot be empty or whitespace-only

- **completed**: `bool` (Required, Default: False)
  - Status indicator for task completion
  - True if task is completed, False if pending
  - Default value is False when creating new tasks

### Validation Rules
- Title must not be empty or contain only whitespace
- Title must not exceed 500 characters
- ID must be positive integer
- Completed status must be boolean value

### State Transitions
- **Pending** → **Completed**: When user marks task as complete
- **Completed** → **Pending**: When user updates completed task (optional feature)

## TodoManager Entity

### Collections
- **todos**: `List[Todo]` (In-memory storage)
  - Maintains all todo items during application runtime
  - Preserves insertion order
  - Resets when application exits

- **next_id**: `int` (Auto-increment counter)
  - Tracks the next available ID for new todos
  - Starts at 1 and increments with each new todo
  - Ensures unique IDs across all tasks

### Operations

#### Creation
- **add_todo(title: str) -> Todo**
  - Creates new Todo with unique ID
  - Sets completion status to False by default
  - Adds to todos collection
  - Returns the created Todo object

#### Retrieval
- **get_all_todos() -> List[Todo]**
  - Returns all todos in the collection
  - Maintains order of insertion

- **get_todo_by_id(todo_id: int) -> Optional[Todo]**
  - Finds todo by its ID
  - Returns Todo object if found, None otherwise

- **get_pending_todos() -> List[Todo]**
  - Returns todos with completed=False
  - Helper method for filtered views

- **get_completed_todos() -> List[Todo]**
  - Returns todos with completed=True
  - Helper method for filtered views

#### Modification
- **update_todo(todo_id: int, title: str) -> bool**
  - Updates the title of an existing todo
  - Returns True if successful, False if todo not found

- **complete_todo(todo_id: int) -> bool**
  - Marks a todo as completed (sets completed=True)
  - Returns True if successful, False if todo not found

- **reopen_todo(todo_id: int) -> bool**
  - Reopens a completed todo (sets completed=False)
  - Returns True if successful, False if todo not found

#### Deletion
- **delete_todo(todo_id: int) -> bool**
  - Removes a todo from the collection
  - Returns True if successful, False if todo not found

### Business Rules
- Duplicate titles are allowed (different tasks can have same name)
- IDs are never reused after deletion
- Empty collections are valid state
- All operations are synchronous (in-memory)

## Relationships
- TodoManager contains zero or more Todo entities
- Each Todo belongs to exactly one TodoManager instance
- No relationships between individual Todo entities