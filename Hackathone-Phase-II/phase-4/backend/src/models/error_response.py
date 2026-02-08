from pydantic import BaseModel
from enum import Enum
from typing import Optional


class AuthErrorType(str, Enum):
    """Enumeration of authentication error types."""
    EMAIL_NOT_FOUND = "EMAIL_NOT_FOUND"
    INVALID_PASSWORD = "INVALID_PASSWORD"
    AUTH_FAILED = "AUTH_FAILED"
    INVALID_EMAIL_FORMAT = "INVALID_EMAIL_FORMAT"
    MISSING_FIELDS = "MISSING_FIELDS"
    EMAIL_EXISTS = "EMAIL_EXISTS"
    INVALID_SIGNUP_DATE = "INVALID_SIGNUP_DATE"
    WEAK_PASSWORD = "WEAK_PASSWORD"


class ErrorResponse(BaseModel):
    """Model for authentication error responses."""
    error: AuthErrorType
    message: str
    details: Optional[str] = None


class ValidationErrorResponse(BaseModel):
    """Model for validation error responses."""
    error: str
    message: str
    field: Optional[str] = None
    value: Optional[str] = None


class SuccessResponse(BaseModel):
    """Model for successful responses."""
    success: bool = True
    message: Optional[str] = None
    data: Optional[dict] = None


class AuthSuccessResponse(BaseModel):
    """Model for authentication success responses."""
    success: bool = True
    token: str
    user: dict
    message: Optional[str] = "Authentication successful"