from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from ...models.task import TaskCreate, TaskRead, TaskUpdate
from ...services.task_service import TaskService
from ..deps import get_current_user
from ...models.user import UserRead
from ...database.database import get_async_session
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=dict)
async def get_tasks(
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
    limit: int = 20,
    offset: int = 0
):
    """
    Retrieve all tasks for the authenticated user.

    Args:
        current_user: The authenticated user
        session: Async database session
        limit: Maximum number of tasks to return (default: 20)
        offset: Number of tasks to skip (default: 0)

    Returns:
        Dictionary containing tasks and total count
    """
    try:
        tasks = await TaskService.get_tasks_for_user(session, current_user.id, limit, offset)

        return {
            "success": True,
            "data": {
                "tasks": tasks,
                "total": len(tasks)  # In a real implementation, this would come from a count query
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to retrieve tasks: {str(e)}"
        )


@router.post("/", response_model=dict)
async def create_task(
    task_create: TaskCreate,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task for the authenticated user.

    Args:
        task_create: Task creation data
        current_user: The authenticated user
        session: Async database session

    Returns:
        Dictionary containing the created task
    """
    try:
        # Create the task with the authenticated user's ID
        created_task = await TaskService.create_task(session, task_create, current_user.id)

        return {
            "success": True,
            "data": created_task
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unable to create task: {str(e)}"
        )


@router.get("/{task_id}", response_model=dict)
async def get_task(
    task_id: int,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve a specific task by ID for the authenticated user.

    Args:
        task_id: ID of the task to retrieve
        current_user: The authenticated user
        session: Async database session

    Returns:
        Dictionary containing the task data
    """
    try:
        task = await TaskService.get_task_by_id(session, task_id, current_user.id)

        return {
            "success": True,
            "data": task
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to retrieve task: {str(e)}"
        )


@router.put("/{task_id}", response_model=dict)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update a specific task by ID for the authenticated user.

    Args:
        task_id: ID of the task to update
        task_update: Task update data
        current_user: The authenticated user
        session: Async database session

    Returns:
        Dictionary containing the updated task
    """
    try:
        updated_task = await TaskService.update_task(session, task_id, task_update, current_user.id)

        return {
            "success": True,
            "data": updated_task
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unable to update task: {str(e)}"
        )


@router.delete("/{task_id}", response_model=dict)
async def delete_task(
    task_id: int,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific task by ID for the authenticated user.

    Args:
        task_id: ID of the task to delete
        current_user: The authenticated user
        session: Async database session

    Returns:
        Dictionary containing success message
    """
    try:
        await TaskService.delete_task(session, task_id, current_user.id)

        return {
            "success": True,
            "data": {
                "message": "Task deleted successfully"
            }
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to delete task: {str(e)}"
        )


@router.patch("/{task_id}/toggle", response_model=dict)
async def toggle_task_completion(
    task_id: int,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Toggle the completion status of a specific task.

    Args:
        task_id: ID of the task to toggle
        current_user: The authenticated user
        session: Async database session

    Returns:
        Dictionary containing the updated task
    """
    try:
        updated_task = await TaskService.toggle_task_completion(session, task_id, current_user.id)

        return {
            "success": True,
            "data": {
                "id": updated_task.id,
                "completed": updated_task.completed,
                "updated_at": updated_task.updated_at
            }
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to toggle task completion: {str(e)}"
        )