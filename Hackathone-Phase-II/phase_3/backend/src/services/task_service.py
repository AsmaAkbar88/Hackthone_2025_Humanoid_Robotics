from typing import List, Optional
from datetime import datetime

import sqlalchemy as sa
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError

from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..utils.error_handlers import NotFoundError, ValidationError, UnauthorizedError


class TaskService:
    """Service class for handling task-related business logic."""

    @staticmethod
    async def create_task(session: AsyncSession, task_create: TaskCreate, user_id: str) -> TaskRead:
        """
        Create a new task for a user.

        Args:
            session: Database session
            task_create: Task creation data
            user_id: ID of the user creating the task

        Returns:
            Created task as TaskRead object
        """
        # Create task object with the authenticated user ID
        # We need to create the Task object directly since TaskCreate doesn't include user_id
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            user_id=str(user_id)  # Ensure user_id is explicitly set as string
        )

        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)

        # Return as TaskRead object
        return TaskRead.model_validate(db_task)

    @staticmethod
    async def get_task_by_id(session: AsyncSession, task_id: int, user_id: str) -> TaskRead:
        """
        Get a specific task by ID for a user.

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the requesting user

        Returns:
            Task as TaskRead object

        Raises:
            NotFoundError: If task doesn't exist
            UnauthorizedError: If task exists but doesn't belong to the user
        """
        # First, check if the task exists regardless of ownership
        statement_exists = select(Task).where(Task.id == task_id)
        result_exists = await session.execute(statement_exists)
        task_exists = result_exists.scalar_one_or_none()

        if not task_exists:
            raise NotFoundError(message=f"Task with id {task_id} not found")

        # Now check if the user owns the task - ensuring both sides are strings for comparison
        statement = select(Task).where(Task.id == task_id, Task.user_id == str(user_id))
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            # Task exists but doesn't belong to the user - return 401 Unauthorized
            raise UnauthorizedError(message=f"Access denied: Task with id {task_id} does not belong to you")

        return TaskRead.model_validate(task)

    @staticmethod
    async def get_tasks_for_user(session: AsyncSession, user_id: str, limit: int = 20, offset: int = 0) -> List[TaskRead]:
        """
        Get all tasks for a specific user.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve
            limit: Maximum number of tasks to return
            offset: Number of tasks to skip

        Returns:
            List of tasks as TaskRead objects
        """
        statement = select(Task).where(Task.user_id == str(user_id)).offset(offset).limit(limit)
        result = await session.execute(statement)
        tasks = result.scalars().all()

        return [TaskRead.model_validate(task) for task in tasks]

    @staticmethod
    async def update_task(session: AsyncSession, task_id: int, task_update: TaskUpdate, user_id: str) -> TaskRead:
        """
        Update a specific task for a user.

        Args:
            session: Database session
            task_id: ID of the task to update
            task_update: Task update data
            user_id: ID of the requesting user

        Returns:
            Updated task as TaskRead object

        Raises:
            NotFoundError: If task doesn't exist
            UnauthorizedError: If task exists but doesn't belong to the user
        """
        # First, check if the task exists regardless of ownership
        statement_exists = select(Task).where(Task.id == task_id)
        result_exists = await session.execute(statement_exists)
        task_exists = result_exists.scalar_one_or_none()

        if not task_exists:
            raise NotFoundError(message=f"Task with id {task_id} not found")

        # Now check if the user owns the task - ensuring both sides are strings for comparison
        statement = select(Task).where(Task.id == task_id, Task.user_id == str(user_id))
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            # Task exists but doesn't belong to the user - return 401 Unauthorized
            raise UnauthorizedError(message=f"Access denied: Task with id {task_id} does not belong to you")

        # Update task fields with provided values
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        task.updated_at = datetime.utcnow()

        session.add(task)
        await session.commit()
        await session.refresh(task)

        return TaskRead.model_validate(task)

    @staticmethod
    async def delete_task(session: AsyncSession, task_id: int, user_id: str) -> bool:
        """
        Delete a specific task for a user.

        Args:
            session: Database session
            task_id: ID of the task to delete
            user_id: ID of the requesting user

        Returns:
            True if task was deleted, False otherwise

        Raises:
            NotFoundError: If task doesn't exist
            UnauthorizedError: If task exists but doesn't belong to the user
        """
        # First, check if the task exists regardless of ownership
        statement_exists = select(Task).where(Task.id == task_id)
        result_exists = await session.execute(statement_exists)
        task_exists = result_exists.scalar_one_or_none()

        if not task_exists:
            raise NotFoundError(message=f"Task with id {task_id} not found")

        # Now check if the user owns the task - ensuring both sides are strings for comparison
        statement = select(Task).where(Task.id == task_id, Task.user_id == str(user_id))
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            # Task exists but doesn't belong to the user - return 401 Unauthorized
            raise UnauthorizedError(message=f"Access denied: Task with id {task_id} does not belong to you")

        await session.delete(task)
        await session.commit()

        return True

    @staticmethod
    async def toggle_task_completion(session: AsyncSession, task_id: int, user_id: str) -> TaskRead:
        """
        Toggle the completion status of a specific task.

        Args:
            session: Database session
            task_id: ID of the task to toggle
            user_id: ID of the requesting user

        Returns:
            Updated task as TaskRead object

        Raises:
            NotFoundError: If task doesn't exist
            UnauthorizedError: If task exists but doesn't belong to the user
        """
        # First, check if the task exists regardless of ownership
        statement_exists = select(Task).where(Task.id == task_id)
        result_exists = await session.execute(statement_exists)
        task_exists = result_exists.scalar_one_or_none()

        if not task_exists:
            raise NotFoundError(message=f"Task with id {task_id} not found")

        # Now check if the user owns the task - ensuring both sides are strings for comparison
        statement = select(Task).where(Task.id == task_id, Task.user_id == str(user_id))
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            # Task exists but doesn't belong to the user - return 401 Unauthorized
            raise UnauthorizedError(message=f"Access denied: Task with id {task_id} does not belong to you")

        # Toggle the completion status
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()

        session.add(task)
        await session.commit()
        await session.refresh(task)

        return TaskRead.model_validate(task)

    @staticmethod
    async def verify_task_ownership(session: AsyncSession, task_id: int, user_id: str) -> bool:
        """
        Verify if a user owns a specific task.

        Args:
            session: Database session
            task_id: ID of the task to check
            user_id: ID of the user to check ownership for

        Returns:
            True if the user owns the task, False otherwise
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == str(user_id))
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        return task is not None