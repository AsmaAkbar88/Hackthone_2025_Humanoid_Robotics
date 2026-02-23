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
        print(f"Getting tasks for user ID: {current_user.id}")
        tasks = await TaskService.get_tasks_for_user(session, current_user.id, limit, offset)
        print(f"Retrieved {len(tasks)} tasks from database")

        # Convert tasks to dict to ensure proper serialization
        task_dicts = []
        for task in tasks:
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": task.user_id,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }
            task_dicts.append(task_dict)

        print(f"Successfully converted {len(task_dicts)} tasks to dict format")

        return {
            "success": True,
            "data": {
                "tasks": task_dicts,
                "total": len(task_dicts)
            }
        }
    except Exception as e:
        print(f"Error in get_tasks: {str(e)}")
        import traceback
        traceback.print_exc()
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

        # Convert to dict to ensure proper serialization
        task_dict = {
            "id": created_task.id,
            "title": created_task.title,
            "description": created_task.description,
            "completed": created_task.completed,
            "user_id": created_task.user_id,
            "created_at": created_task.created_at.isoformat() if created_task.created_at else None,
            "updated_at": created_task.updated_at.isoformat() if created_task.updated_at else None
        }

        return {
            "success": True,
            "data": task_dict
        }
    except Exception as e:
        print(f"Error in create_task: {str(e)}")
        import traceback
        traceback.print_exc()
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

        # Convert to dict to ensure proper serialization
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "user_id": task.user_id,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        }

        return {
            "success": True,
            "data": task_dict
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Error in get_task: {str(e)}")
        import traceback
        traceback.print_exc()
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

        # Convert to dict to ensure proper serialization
        task_dict = {
            "id": updated_task.id,
            "title": updated_task.title,
            "description": updated_task.description,
            "completed": updated_task.completed,
            "user_id": updated_task.user_id,
            "created_at": updated_task.created_at.isoformat() if updated_task.created_at else None,
            "updated_at": updated_task.updated_at.isoformat() if updated_task.updated_at else None
        }

        return {
            "success": True,
            "data": task_dict
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Error in update_task: {str(e)}")
        import traceback
        traceback.print_exc()
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
        print(f"Error in delete_task: {str(e)}")
        import traceback
        traceback.print_exc()
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
                "updated_at": updated_task.updated_at.isoformat() if updated_task.updated_at else None
            }
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Error in toggle_task_completion: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to toggle task completion: {str(e)}"
        )