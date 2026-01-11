#!/usr/bin/env python3
"""
Main entry point for the In-Memory Python Console Todo Application.

This module implements the main application loop that handles user commands
and orchestrates the interaction between UI, business logic, and data models.
"""
import sys
import os
from typing import NoReturn

# Add the current directory to the path to allow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from todo_manager import TodoManager
from ui import (
    display_menu, get_user_choice, get_and_validate_task_input,
    display_tasks, display_message, get_task_id_input, confirm_action
)


class TodoApp:
    """Main application class that orchestrates the todo application."""

    def __init__(self):
        """Initialize the Todo application with a TodoManager."""
        self.todo_manager = TodoManager()

    def run(self) -> NoReturn:
        """Run the main application loop."""
        print("Welcome to the Todo Application!")

        while True:
            display_menu()
            choice = get_user_choice()

            if choice == '1':
                self._handle_add_task()
            elif choice == '2':
                self._handle_view_tasks()
            elif choice == '3':
                self._handle_update_task()
            elif choice == '4':
                self._handle_complete_task()
            elif choice == '5':
                self._handle_delete_task()
            elif choice == '6':
                self._handle_exit()
            else:
                display_message("Invalid option. Please choose 1-6.")

    def _handle_add_task(self):
        """Handle the add task operation."""
        print("\nADD NEW TASK")
        print("-" * 12)
        task_title = get_and_validate_task_input("Enter task description: ")

        if task_title:
            try:
                new_todo = self.todo_manager.add_todo(task_title)
                display_message(f"Task added successfully with ID: {new_todo.id}")
            except ValueError as e:
                display_message(f"Error adding task: {str(e)}")
        else:
            display_message("Task not added due to validation error.")

    def _handle_view_tasks(self):
        """Handle the view tasks operation."""
        print("\nVIEW ALL TASKS")
        print("-" * 13)
        todos = self.todo_manager.get_all_todos()
        display_tasks(todos)

    def _handle_update_task(self):
        """Handle the update task operation."""
        print("\nUPDATE TASK")
        print("-" * 11)
        task_id = get_task_id_input("Enter task ID to update: ")

        if task_id == -1:
            return  # Invalid input

        if self.todo_manager.get_todo_by_id(task_id) is None:
            display_message(f"Task with ID {task_id} not found.")
            return

        new_title = get_and_validate_task_input("Enter new task description: ")
        if new_title:
            success = self.todo_manager.update_todo(task_id, new_title)
            if success:
                display_message(f"Task {task_id} updated successfully.")
            else:
                display_message(f"Failed to update task {task_id}.")
        else:
            display_message("Task not updated due to validation error.")

    def _handle_complete_task(self):
        """Handle the complete task operation."""
        print("\nCOMPLETE TASK")
        print("-" * 12)
        task_id = get_task_id_input("Enter task ID to complete: ")

        if task_id == -1:
            return  # Invalid input

        success = self.todo_manager.complete_todo(task_id)
        if success:
            display_message(f"Task {task_id} marked as complete.")
        else:
            display_message(f"Task with ID {task_id} not found.")

    def _handle_delete_task(self):
        """Handle the delete task operation."""
        print("\nDELETE TASK")
        print("-" * 11)
        task_id = get_task_id_input("Enter task ID to delete: ")

        if task_id == -1:
            return  # Invalid input

        todo = self.todo_manager.get_todo_by_id(task_id)
        if todo is None:
            display_message(f"Task with ID {task_id} not found.")
            return

        # Show the task to be deleted and ask for confirmation
        print(f"You are about to delete task: [{task_id}] {todo.title}")
        confirmed = confirm_action("Are you sure you want to delete this task? (y/n): ")

        if not confirmed:
            display_message("Task deletion cancelled.")
            return

        success = self.todo_manager.delete_todo(task_id)
        if success:
            display_message(f"Task {task_id} deleted successfully.")
        else:
            display_message(f"Failed to delete task {task_id}.")

    def _handle_exit(self):
        """Handle the exit operation."""
        display_message("Thank you for using the Todo Application. Goodbye!")
        sys.exit(0)


def main():
    """Main function to start the application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()