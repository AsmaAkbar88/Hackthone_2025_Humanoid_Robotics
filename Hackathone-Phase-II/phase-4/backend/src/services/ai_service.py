"""
AI Service for the Todo Backend API.

Implements MCP tools for task operations and integrates with OpenAI Agents SDK.
"""
from typing import Optional, List, Dict, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..models.user import UserRead
from ..services.task_service import TaskService
from ..config import settings
import openai
from openai import OpenAI


class AIService:
    """
    Service class to handle AI interactions and MCP tools for task operations.
    """
    
    def __init__(self):
        # Initialize OpenAI client lazily (only when needed)
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            self._client = OpenAI(api_key=settings.openai_api_key)
        return self._client
        
    async def add_task_tool(
        self,
        title: str,
        user: UserRead,
        session: AsyncSession,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        MCP tool for adding tasks.

        Args:
            title: Title of the task
            description: Optional description of the task
            user: User who owns the task
            session: Database session

        Returns:
            Dictionary with task creation result
        """
        try:
            # Create task data
            task_create = TaskCreate(title=title, description=description)

            # Use TaskService to create the task
            # Convert user.id to string to match database schema
            user_id_str = str(user.id)
            created_task = await TaskService.create_task(session, task_create, user_id_str)

            return {
                "success": True,
                "task_id": created_task.id,
                "message": f"Task '{created_task.title}' added successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to add task"
            }
    
    async def list_tasks_tool(
        self,
        user: UserRead,
        session: AsyncSession,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        MCP tool for listing tasks.

        Args:
            user: User whose tasks to list
            session: Database session
            limit: Maximum number of tasks to return
            offset: Number of tasks to skip

        Returns:
            Dictionary with list of tasks
        """
        try:
            # Use TaskService to get tasks
            # Convert user.id to string to match database schema
            user_id_str = str(user.id)
            tasks = await TaskService.get_tasks_for_user(session, user_id_str, limit, offset)

            return {
                "success": True,
                "tasks": [task.model_dump() for task in tasks],
                "count": len(tasks)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to list tasks"
            }
    
    async def update_task_tool(
        self,
        task_id: int,
        user: UserRead,
        session: AsyncSession,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        MCP tool for updating tasks.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)
            user: User who owns the task
            session: Database session

        Returns:
            Dictionary with task update result
        """
        try:
            # Prepare update data
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if description is not None:
                update_data["description"] = description
            if completed is not None:
                update_data["completed"] = completed

            task_update = TaskUpdate(**update_data)

            # Use TaskService to update the task
            # Convert user.id to string to match database schema
            user_id_str = str(user.id)
            updated_task = await TaskService.update_task(session, task_id, task_update, user_id_str)

            return {
                "success": True,
                "task_id": updated_task.id,
                "message": f"Task '{updated_task.title}' updated successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update task"
            }
    
    async def delete_task_tool(
        self,
        task_id: int,
        user: UserRead,
        session: AsyncSession
    ) -> Dict[str, Any]:
        """
        MCP tool for deleting tasks.

        Args:
            task_id: ID of the task to delete
            user: User who owns the task
            session: Database session

        Returns:
            Dictionary with task deletion result
        """
        try:
            # Use TaskService to delete the task
            # Convert user.id to string to match database schema
            user_id_str = str(user.id)
            await TaskService.delete_task(session, task_id, user_id_str)

            return {
                "success": True,
                "task_id": task_id,
                "message": "Task deleted successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to delete task"
            }
    
    async def complete_task_tool(
        self,
        task_id: int,
        user: UserRead,
        session: AsyncSession
    ) -> Dict[str, Any]:
        """
        
        MCP tool for completing tasks.

        Args:
            task_id: ID of the task to mark as complete
            user: User who owns the task
            session: Database session

        Returns:
            Dictionary with task completion result
        """
        try:
            # Use TaskService to toggle task completion
            # Convert user.id to string to match database schema
            user_id_str = str(user.id)
            updated_task = await TaskService.toggle_task_completion(session, task_id, user_id_str)

            status = "completed" if updated_task.completed else "marked as incomplete"
            return {
                "success": True,
                "task_id": updated_task.id,
                "completed": updated_task.completed,
                "message": f"Task '{updated_task.title}' {status} successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to complete task"
            }


# Global instance
ai_service = AIService()