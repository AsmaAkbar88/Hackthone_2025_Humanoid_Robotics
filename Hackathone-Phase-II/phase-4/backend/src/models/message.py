from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .conversation import Conversation  # Avoid circular import for type checking


class MessageRole(str, Enum):
    """Enumeration for message roles."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageBase(SQLModel):
    """Base model for Message with common fields."""
    role: MessageRole = Field(sa_column_kwargs={"default": "user"})
    content: str = Field(max_length=5000)
    conversation_id: int = Field(foreign_key="conversation.id")


class Message(MessageBase, table=True):
    """Message model for the database table."""
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationship
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    """Model for creating a new message."""
    pass


class MessageRead(MessageBase):
    """Model for reading message data."""
    id: int
    timestamp: datetime