"""
TodoManager for the In-Memory Python Console Todo Application.

This module manages the collection of Todo items in memory, providing methods
for adding, retrieving, updating, and deleting todo items.
"""
from typing import List, Optional
import sys
import os

# Add the current directory to the path to allow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from todo import Todo


class TodoManager:
    """
    Manages the collection of Todo items in memory.

    Handles all business logic for todo operations including adding, retrieving,
    updating, and deleting todo items with unique IDs.
    """

    def __init__(self):
        """Initialize the TodoManager with an empty list of todos and ID counter."""
        self.todos: List[Todo] = []
        self.next_id: int = 1

    def add_todo(self, title: str) -> Todo:
        """
        Create a new Todo with a unique ID and add it to the collection.

        Args:
            title (str): The title/description of the new todo

        Returns:
            Todo: The newly created Todo object

        Raises:
            ValueError: If the title is empty or contains only whitespace
        """
        if not title or not title.strip():
            raise ValueError("Todo title cannot be empty or contain only whitespace")

        # Create a new Todo with the next available ID
        new_todo = Todo(id=self.next_id, title=title.strip(), completed=False)
        self.todos.append(new_todo)

        # Increment the ID counter for the next todo
        self.next_id += 1

        return new_todo

    def get_all_todos(self) -> List[Todo]:
        """
        Retrieve all todos in the collection.

        Returns:
            List[Todo]: A list of all Todo objects
        """
        return self.todos.copy()  # Return a copy to prevent external modification

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """
        Find a todo by its ID.

        Args:
            todo_id (int): The ID of the todo to find

        Returns:
            Optional[Todo]: The Todo object if found, None otherwise
        """
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def update_todo(self, todo_id: int, title: str) -> bool:
        """
        Update the title of an existing todo.

        Args:
            todo_id (int): The ID of the todo to update
            title (str): The new title for the todo

        Returns:
            bool: True if the update was successful, False if todo not found
        """
        if not title or not title.strip():
            raise ValueError("Todo title cannot be empty or contain only whitespace")

        for todo in self.todos:
            if todo.id == todo_id:
                todo.title = title.strip()
                return True
        return False

    def complete_todo(self, todo_id: int) -> bool:
        """
        Mark a todo as completed.

        Args:
            todo_id (int): The ID of the todo to mark as completed

        Returns:
            bool: True if the operation was successful, False if todo not found
        """
        for todo in self.todos:
            if todo.id == todo_id:
                todo.completed = True
                return True
        return False

    def delete_todo(self, todo_id: int) -> bool:
        """
        Remove a todo from the collection.

        Args:
            todo_id (int): The ID of the todo to remove

        Returns:
            bool: True if the deletion was successful, False if todo not found
        """
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                del self.todos[i]
                return True
        return False

    def get_pending_todos(self) -> List[Todo]:
        """
        Retrieve all todos that are not completed.

        Returns:
            List[Todo]: A list of pending Todo objects
        """
        return [todo for todo in self.todos if not todo.completed]

    def get_completed_todos(self) -> List[Todo]:
        """
        Retrieve all todos that are completed.

        Returns:
            List[Todo]: A list of completed Todo objects
        """
        return [todo for todo in self.todos if todo.completed]

    def reopen_todo(self, todo_id: int) -> bool:
        """
        Mark a completed todo as pending again.

        Args:
            todo_id (int): The ID of the todo to reopen

        Returns:
            bool: True if the operation was successful, False if todo not found
        """
        for todo in self.todos:
            if todo.id == todo_id:
                todo.completed = False
                return True
        return False