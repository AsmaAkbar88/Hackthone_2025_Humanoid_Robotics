from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel


class AuthenticationSessionBase(SQLModel):
    """Base model for Authentication Session with common fields."""
    user_id: str = Field(nullable=False)  # Reference to associated user
    expires_at: datetime = Field(nullable=False)  # Session expiration time


class AuthenticationSession(AuthenticationSessionBase, table=True):
    """Authentication Session model for the database table."""
    session_id: Optional[str] = Field(default=None, primary_key=True)
    user_id: str = Field(nullable=False)  # Reference to associated user
    jwt_token: str = Field(nullable=False, max_length=500)  # JWT token for session management
    expires_at: datetime = Field(nullable=False)  # Session expiration time
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)


class AuthenticationSessionCreate(AuthenticationSessionBase):
    """Model for creating a new authentication session."""
    jwt_token: str
    user_id: str
    expires_at: datetime


class AuthenticationSessionRead(AuthenticationSessionBase):
    """Model for reading authentication session data."""
    session_id: str
    jwt_token: str
    created_at: datetime