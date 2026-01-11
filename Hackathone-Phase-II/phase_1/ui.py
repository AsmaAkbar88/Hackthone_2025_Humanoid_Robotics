"""
UI utilities for the In-Memory Python Console Todo Application.

This module provides console interface functions for displaying menus,
getting user input, and formatting output.
"""
from typing import List
import sys
import os

# Add the current directory to the path to allow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from todo import Todo


def display_menu():
    """Display the main menu options to the user."""
    print("\nTODO APPLICATION")
    print("-" * 18)
    print("1. Add new task")
    print("2. View all tasks")
    print("3. Update task")
    print("4. Complete task")
    print("5. Delete task")
    print("6. Exit")
    print("-" * 18)


def get_user_choice() -> str:
    """
    Get the user's menu selection.

    Returns:
        str: The user's choice as a string
    """
    return input("Choose an option (1-6): ").strip()


def get_task_input(prompt: str = "Enter task description: ") -> str:
    """
    Get task description from user input.

    Args:
        prompt (str): The prompt to display to the user

    Returns:
        str: The user's input (may be empty)
    """
    return input(prompt).strip()


def get_and_validate_task_input(prompt: str = "Enter task description: ") -> str:
    """
    Get and validate task description from user input.

    Args:
        prompt (str): The prompt to display to the user

    Returns:
        str: The validated user's input, or empty string if invalid
    """
    task_input = input(prompt).strip()

    if not task_input:
        print("Error: Task description cannot be empty.")
        return ""

    if len(task_input) > 500:  # Maximum length validation
        print("Error: Task description is too long (maximum 500 characters).")
        return ""

    return task_input


def display_tasks(todos: List[Todo]):
    """
    Display all tasks in a readable format.

    Args:
        todos (List[Todo]): List of Todo objects to display
    """
    if not todos:
        print("\nNo tasks found.")
        return

    print("\nYOUR TASKS")
    print("-" * 40)
    for todo in todos:
        status = "[x]" if todo.completed else "[ ]"
        print(f"{status} [{todo.id}] {todo.title}")
    print("-" * 40)


def get_task_id_input(prompt: str = "Enter task ID: ") -> int:
    """
    Get task ID from user input and validate it's a number.

    Args:
        prompt (str): The prompt to display to the user

    Returns:
        int: The task ID or -1 if invalid input
    """
    try:
        user_input = input(prompt).strip()
        return int(user_input)
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return -1


def display_message(message: str):
    """
    Display a message to the user.

    Args:
        message (str): The message to display
    """
    print(f"\n{message}")


def confirm_action(prompt: str = "Are you sure? (y/n): ") -> bool:
    """
    Get confirmation from the user before performing an action.

    Args:
        prompt (str): The confirmation prompt

    Returns:
        bool: True if user confirms, False otherwise
    """
    response = input(prompt).strip().lower()
    return response in ['y', 'yes', '1', 'true']