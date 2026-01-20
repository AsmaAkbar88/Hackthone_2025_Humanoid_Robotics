import pytest
from datetime import datetime

from backend.src.models.task import Task, TaskCreate, TaskRead, TaskUpdate


def test_task_creation():
    """Test creating a task with valid data."""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False,
        "user_id": 1
    }

    task_create = TaskCreate(**task_data)
    assert task_create.title == "Test Task"
    assert task_create.description == "This is a test task"
    assert task_create.completed is False
    assert task_create.user_id == 1


def test_task_creation_required_fields():
    """Test that required fields are enforced."""
    with pytest.raises(ValueError):
        TaskCreate(title="", user_id=1)  # Empty title should fail

    with pytest.raises(ValueError):
        TaskCreate(title="Test Task")  # Missing user_id should fail


def test_task_creation_title_length_validation():
    """Test title length validation."""
    # Title too long should fail
    long_title = "t" * 256
    with pytest.raises(ValueError):
        TaskCreate(title=long_title, user_id=1)

    # Title at max length should pass
    max_title = "t" * 255
    task = TaskCreate(title=max_title, user_id=1)
    assert len(task.title) == 255


def test_task_update_partial():
    """Test that TaskUpdate allows partial updates."""
    # All fields should be optional in TaskUpdate
    update_data = {}
    task_update = TaskUpdate(**update_data)
    assert task_update.title is None
    assert task_update.description is None
    assert task_update.completed is None


def test_task_update_with_values():
    """Test updating with specific values."""
    update_data = {
        "title": "Updated Title",
        "completed": True
    }
    task_update = TaskUpdate(**update_data)
    assert task_update.title == "Updated Title"
    assert task_update.completed is True
    assert task_update.description is None


def test_task_read_serialization():
    """Test TaskRead model serialization."""
    task_read = TaskRead(
        id=1,
        title="Test Task",
        description="Description",
        completed=False,
        user_id=1,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    assert task_read.id == 1
    assert task_read.title == "Test Task"
    assert task_read.description == "Description"
    assert task_read.completed is False
    assert task_read.user_id == 1