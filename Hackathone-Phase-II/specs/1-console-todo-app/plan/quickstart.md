# Quickstart Guide: In-Memory Python Console Todo Application

**Feature**: 1-console-todo-app
**Created**: 2026-01-11
**Version**: Phase I

## Prerequisites

### System Requirements
- Python 3.7 or higher (Python 3.12+ recommended)
- Operating System: Windows, macOS, or Linux
- Terminal/Command Prompt access

### Installation
No external dependencies required - only Python standard library is used.

## Setup Instructions

### 1. Clone or Access the Repository
```bash
# Navigate to your project directory
cd path/to/your/project
```

### 2. Verify Python Installation
```bash
python --version
# Should show Python 3.7+ (preferably 3.12+)
```

### 3. Create Project Structure
```bash
mkdir phase_1
cd phase_1
```

## Running the Application

### Execute the Application
```bash
python main.py
```

## Basic Usage Guide

### Main Menu Options
Once the application starts, you'll see the main menu:

```
===== TODO APPLICATION =====
1. Add new task
2. View all tasks
3. Update task
4. Complete task
5. Delete task
6. Exit
Choose an option (1-6):
```

### Available Operations

#### 1. Add New Task
- Select option `1`
- Enter your task description when prompted
- The task will be added with a unique ID

#### 2. View All Tasks
- Select option `2`
- See all tasks with their IDs and completion status
- Pending tasks marked as `[ ]`
- Completed tasks marked as `[x]`

#### 3. Update Task
- Select option `3`
- Enter the task ID you want to update
- Enter the new task description
- The task will be updated in the list

#### 4. Complete Task
- Select option `4`
- Enter the task ID you want to mark as complete
- The task status will be updated to completed

#### 5. Delete Task
- Select option `5`
- Enter the task ID you want to delete
- The task will be removed from the list

#### 6. Exit
- Select option `6`
- The application will terminate
- All data will be lost (in-memory only)

## Example Workflow

1. Start the application: `python phase_1/main.py`
2. Add a task: Choose option `1`, enter "Buy groceries"
3. View tasks: Choose option `2`, see your task listed
4. Add more tasks: Repeat step 2 with different descriptions
5. Complete a task: Choose option `4`, enter the ID of a task
6. View updated list: Choose option `2`, see completed status
7. Exit: Choose option `6`

## Troubleshooting

### Common Issues

**Issue**: "python: command not found"
- **Solution**: Ensure Python is installed and added to your system PATH

**Issue**: "SyntaxError" or import errors
- **Solution**: Verify you're using Python 3.7 or higher (recommended Python 3.12+)

**Issue**: Application crashes when entering invalid input
- **Solution**: The application handles most invalid inputs gracefully, but extreme cases might cause issues

## Development Information

### File Structure
```
phase_1/
├── main.py          # Application entry point and main loop
├── todo.py          # Todo data model definition
├── todo_manager.py  # Business logic and data management
├── ui.py            # User interface and console interaction
└── utils.py         # Utility functions
```

### Key Features
- In-memory storage (resets on application exit)
- Sequential task IDs starting from 1
- Simple menu-driven interface
- Input validation and error handling
- Beginner-friendly design

## Next Steps

After familiarizing yourself with the application:
1. Explore the source code to understand the implementation
2. Consider enhancements for future phases
3. Review the specification and implementation plan