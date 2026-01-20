import pytest
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Request

from backend.src.utils.error_handlers import (
    APIError,
    ValidationError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
    InternalServerError,
    validation_error_handler,
    not_found_error_handler,
    unauthorized_error_handler,
    forbidden_error_handler,
    internal_server_error_handler,
    http_exception_handler
)


@pytest.fixture
def mock_request():
    """Mock request object for testing."""
    return Request({"type": "http"})


def test_api_error_initialization():
    """Test APIError initialization."""
    error = APIError(message="Test error", code="TEST_ERROR", status_code=400)
    assert error.message == "Test error"
    assert error.code == "TEST_ERROR"
    assert error.status_code == 400


def test_validation_error():
    """Test ValidationError."""
    error = ValidationError()
    assert error.message == "Invalid request data"
    assert error.code == "VALIDATION_001"
    assert error.status_code == 400

    custom_error = ValidationError("Custom validation error")
    assert custom_error.message == "Custom validation error"


def test_not_found_error():
    """Test NotFoundError."""
    error = NotFoundError()
    assert error.message == "Resource not found"
    assert error.code == "RESOURCE_001"
    assert error.status_code == 404

    custom_error = NotFoundError("Custom not found error")
    assert custom_error.message == "Custom not found error"


def test_unauthorized_error():
    """Test UnauthorizedError."""
    error = UnauthorizedError()
    assert error.message == "Unauthorized access"
    assert error.code == "AUTH_001"
    assert error.status_code == 401

    custom_error = UnauthorizedError("Custom unauthorized error")
    assert custom_error.message == "Custom unauthorized error"


def test_forbidden_error():
    """Test ForbiddenError."""
    error = ForbiddenError()
    assert error.message == "Access forbidden"
    assert error.code == "ACCESS_001"
    assert error.status_code == 403

    custom_error = ForbiddenError("Custom forbidden error")
    assert custom_error.message == "Custom forbidden error"


def test_internal_server_error():
    """Test InternalServerError."""
    error = InternalServerError()
    assert error.message == "Internal server error"
    assert error.code == "SERVER_001"
    assert error.status_code == 500

    custom_error = InternalServerError("Custom server error")
    assert custom_error.message == "Custom server error"


@pytest.mark.asyncio
async def test_validation_error_handler(mock_request):
    """Test validation error handler."""
    error = ValidationError("Test validation error")
    response = await validation_error_handler(mock_request, error)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 400

    response_body = response.body.decode()
    assert "VALIDATION_001" in response_body
    assert "Test validation error" in response_body


@pytest.mark.asyncio
async def test_not_found_error_handler(mock_request):
    """Test not found error handler."""
    error = NotFoundError("Test not found error")
    response = await not_found_error_handler(mock_request, error)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 404

    response_body = response.body.decode()
    assert "RESOURCE_001" in response_body
    assert "Test not found error" in response_body


@pytest.mark.asyncio
async def test_unauthorized_error_handler(mock_request):
    """Test unauthorized error handler."""
    error = UnauthorizedError("Test unauthorized error")
    response = await unauthorized_error_handler(mock_request, error)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 401

    response_body = response.body.decode()
    assert "AUTH_001" in response_body
    assert "Test unauthorized error" in response_body


@pytest.mark.asyncio
async def test_forbidden_error_handler(mock_request):
    """Test forbidden error handler."""
    error = ForbiddenError("Test forbidden error")
    response = await forbidden_error_handler(mock_request, error)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 403

    response_body = response.body.decode()
    assert "ACCESS_001" in response_body
    assert "Test forbidden error" in response_body


@pytest.mark.asyncio
async def test_internal_server_error_handler(mock_request):
    """Test internal server error handler."""
    error = InternalServerError("Test server error")
    response = await internal_server_error_handler(mock_request, error)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 500

    response_body = response.body.decode()
    assert "SERVER_001" in response_body
    assert "Test server error" in response_body


@pytest.mark.asyncio
async def test_http_exception_handler(mock_request):
    """Test HTTP exception handler."""
    http_exc = HTTPException(status_code=404, detail="Item not found")
    response = await http_exception_handler(mock_request, http_exc)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 404

    response_body = response.body.decode()
    assert "RESOURCE_001" in response_body  # Maps 404 to RESOURCE_001
    assert "Item not found" in response_body