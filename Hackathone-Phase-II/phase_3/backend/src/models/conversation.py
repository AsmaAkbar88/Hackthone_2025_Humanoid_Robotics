from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .message import Message  # Avoid circular import for type checking


class ConversationBase(SQLModel):
    """Base model for Conversation with common fields."""
    title: str = Field(default="New Conversation", max_length=255)
    user_id: str = Field(index=True)  # String identifier for user (matches database schema)


class Conversation(ConversationBase, table=True):
    """Conversation model for the database table."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Relationship
    messages: List["Message"] = Relationship(back_populates="conversation")


class ConversationCreate(ConversationBase):
    """Model for creating a new conversation."""
    pass


class ConversationRead(ConversationBase):
    """Model for reading conversation data."""
    id: int
    created_at: datetime
    updated_at: datetime
    # Note: messages are typically not included in read models to avoid circular references
    # They can be retrieved separately when needed