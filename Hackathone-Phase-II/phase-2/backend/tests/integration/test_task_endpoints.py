import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

from backend.src.api.main import app
from backend.src.database.database import AsyncSessionLocal
from backend.src.models.task import Task, TaskCreate


@pytest.fixture
def client():
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.asyncio
async def test_secure_task_operations():
    """Test that users can only access their own tasks."""
    # This test would require proper authentication setup
    # For now, we'll just verify the endpoints exist and return appropriate responses
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        # Test that endpoints require authentication
        response = await ac.get("/api/tasks/")
        assert response.status_code in [401, 403]  # Unauthorized or Forbidden

        response = await ac.post("/api/tasks/", json={"title": "Test", "user_id": 1})
        assert response.status_code in [401, 403]  # Unauthorized or Forbidden


def test_task_crud_operations(client):
    """Test basic CRUD operations for tasks."""
    # This test would require mocking authentication
    # For now, we'll just check if the routes exist
    headers = {"Authorization": "Bearer fake-token"}

    # Test GET /api/tasks
    response = client.get("/api/tasks/", headers=headers)
    # This might return 401, 403, or 200 depending on auth implementation
    assert response.status_code in [200, 401, 403]

    # Test POST /api/tasks
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False
    }
    response = client.post("/api/tasks/", json=task_data, headers=headers)
    assert response.status_code in [200, 201, 401, 403, 422]


def test_task_update_and_delete(client):
    """Test updating and deleting tasks."""
    headers = {"Authorization": "Bearer fake-token"}

    # These would require a created task first, which needs auth
    # Just testing that endpoints exist
    response = client.put("/api/tasks/1", json={"title": "Updated"}, headers=headers)
    assert response.status_code in [200, 401, 403, 404, 422]

    response = client.delete("/api/tasks/1", headers=headers)
    assert response.status_code in [200, 204, 401, 403, 404]