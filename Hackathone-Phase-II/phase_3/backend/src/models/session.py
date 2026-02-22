from typing import Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Column


class SessionBase(SQLModel):
    """Base model for Session with common fields."""
    user_id: str = Field(index=True, nullable=False)  # Reference to associated user
    expires_at: datetime = Field(nullable=False)  # Session expiration time


class Session(SessionBase, table=True):
    """Session model for the database table."""
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, sa_column=Column(UUID(as_uuid=True), primary_key=True, default=uuid4))
    user_id: str = Field(index=True, nullable=False)  # Reference to associated user
    expires_at: datetime = Field(nullable=False)  # Session expiration time
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class SessionCreate(SessionBase):
    """Model for creating a new session."""
    pass


class SessionRead(SessionBase):
    """Model for reading session data."""
    id: UUID
    created_at: datetime