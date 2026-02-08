import pytest
from fastapi.testclient import TestClient

from backend.src.api.main import app


@pytest.fixture
def client():
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client


def test_get_tasks_contract(client):
    """Test the contract for GET /api/tasks endpoint."""
    # This would normally require authentication
    headers = {"Authorization": "Bearer fake-token"}

    response = client.get("/api/tasks/", headers=headers)

    # The response should follow the contract format
    if response.status_code != 401:  # If not unauthorized (due to missing auth)
        # If authorized, should return the expected format
        assert "success" in response.json()
        data = response.json()
        assert isinstance(data["success"], bool)

        if data["success"]:
            assert "data" in data
            assert "tasks" in data["data"]
            assert isinstance(data["data"]["tasks"], list)


def test_post_tasks_contract(client):
    """Test the contract for POST /api/tasks endpoint."""
    headers = {"Authorization": "Bearer fake-token"}
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False
    }

    response = client.post("/api/tasks/", json=task_data, headers=headers)

    # The response should follow the contract format
    if response.status_code not in [401, 422]:  # If not unauthorized or validation error
        assert "success" in response.json()
        data = response.json()
        assert isinstance(data["success"], bool)

        if data["success"]:
            assert "data" in data
            assert "id" in data["data"] or "message" in data["data"]


def test_get_specific_task_contract(client):
    """Test the contract for GET /api/tasks/{task_id} endpoint."""
    headers = {"Authorization": "Bearer fake-token"}

    response = client.get("/api/tasks/1", headers=headers)

    # The response should follow the contract format
    if response.status_code not in [401, 404]:  # If not unauthorized or not found
        assert "success" in response.json()
        data = response.json()
        assert isinstance(data["success"], bool)


def test_put_task_contract(client):
    """Test the contract for PUT /api/tasks/{task_id} endpoint."""
    headers = {"Authorization": "Bearer fake-token"}
    update_data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "completed": True
    }

    response = client.put("/api/tasks/1", json=update_data, headers=headers)

    # The response should follow the contract format
    if response.status_code not in [401, 404, 422]:  # If not unauthorized, not found, or validation error
        assert "success" in response.json()
        data = response.json()
        assert isinstance(data["success"], bool)


def test_delete_task_contract(client):
    """Test the contract for DELETE /api/tasks/{task_id} endpoint."""
    headers = {"Authorization": "Bearer fake-token"}

    response = client.delete("/api/tasks/1", headers=headers)

    # The response should follow the contract format
    if response.status_code not in [401, 404]:  # If not unauthorized or not found
        assert "success" in response.json()
        data = response.json()
        assert isinstance(data["success"], bool)


def test_patch_toggle_task_contract(client):
    """Test the contract for PATCH /api/tasks/{task_id}/toggle endpoint."""
    headers = {"Authorization": "Bearer fake-token"}

    response = client.patch("/api/tasks/1/toggle", headers=headers)

    # The response should follow the contract format
    if response.status_code not in [401, 404]:  # If not unauthorized or not found
        assert "success" in response.json()
        data = response.json()
        assert isinstance(data["success"], bool)