from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any


class APIError(Exception):
    """Base exception class for API errors."""

    def __init__(self, message: str, code: str, status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(APIError):
    """Exception raised for validation errors."""

    def __init__(self, message: str = "Invalid request data"):
        super().__init__(message=message, code="VALIDATION_001", status_code=400)


class NotFoundError(APIError):
    """Exception raised when a resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, code="RESOURCE_001", status_code=404)


class UnauthorizedError(APIError):
    """Exception raised when authentication fails."""

    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message=message, code="AUTH_001", status_code=401)


class ForbiddenError(APIError):
    """Exception raised when authorization fails."""

    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message=message, code="ACCESS_001", status_code=403)


class InternalServerError(APIError):
    """Exception raised for internal server errors."""

    def __init__(self, message: str = "Internal server error"):
        super().__init__(message=message, code="SERVER_001", status_code=500)


async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle validation errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )


async def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    """Handle not found errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )


async def unauthorized_error_handler(request: Request, exc: UnauthorizedError) -> JSONResponse:
    """Handle unauthorized errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )


async def forbidden_error_handler(request: Request, exc: ForbiddenError) -> JSONResponse:
    """Handle forbidden errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )


async def internal_server_error_handler(request: Request, exc: InternalServerError) -> JSONResponse:
    """Handle internal server errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions."""
    error_code_map = {
        400: "VALIDATION_001",
        401: "AUTH_001",
        403: "ACCESS_001",
        404: "RESOURCE_001",
        500: "SERVER_001"
    }

    error_code = error_code_map.get(exc.status_code, f"HTTP_{exc.status_code}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": error_code,
                "message": str(exc.detail) if hasattr(exc, 'detail') else "An error occurred"
            }
        }
    )


def add_exception_handlers(app):
    """Add all exception handlers to the FastAPI app."""
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(NotFoundError, not_found_error_handler)
    app.add_exception_handler(UnauthorizedError, unauthorized_error_handler)
    app.add_exception_handler(ForbiddenError, forbidden_error_handler)
    app.add_exception_handler(InternalServerError, internal_server_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)