"""
Todo data model for the In-Memory Python Console Todo Application.

This module defines the Todo class using dataclass for clean, simple representation
of todo items with id, title, and completion status.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Todo:
    """
    Represents a single todo task with id, title, and completion status.

    Attributes:
        id (int): Unique identifier for the todo item
        title (str): Description of the task
        completed (bool): Status indicating if the task is completed (default: False)
    """
    id: int
    title: str
    completed: bool = False

    def __post_init__(self):
        """Validate the todo attributes after initialization."""
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("ID must be a positive integer")
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Title must be a non-empty string")
        if not isinstance(self.completed, bool):
            raise ValueError("Completed status must be a boolean")