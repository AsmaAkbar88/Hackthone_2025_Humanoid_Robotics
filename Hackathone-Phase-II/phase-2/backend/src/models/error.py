from typing import Optional
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Model for error details in API responses."""
    code: str
    message: str


class ErrorResponse(BaseModel):
    """Model for error responses from the API."""
    success: bool = False
    error: ErrorDetail


class SuccessResponse(BaseModel):
    """Model for success responses from the API."""
    success: bool = True
    data: Optional[dict] = None