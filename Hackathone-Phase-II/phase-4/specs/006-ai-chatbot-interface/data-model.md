# Data Model: AI Chatbot Interface for Todo Application

## Overview
Data model definitions for the AI Chatbot Interface feature, extending the existing Todo application models with conversation and message entities.

## Extended Database Schema

### Conversation Model
Represents a conversation thread between a user and the AI chatbot.

```python
class ConversationBase(SQLModel):
    title: str = Field(default="New Conversation", max_length=255)
    user_id: int = Field(foreign_key="user.id")

class Conversation(ConversationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    
    # Relationship
    messages: List["Message"] = Relationship(back_populates="conversation")

class ConversationCreate(ConversationBase):
    pass

class ConversationRead(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime
```

### Message Model
Represents individual messages within a conversation.

```python
class MessageBase(SQLModel):
    role: str = Field(regex="^(user|assistant|system)$")  # user, assistant, or system
    content: str = Field(max_length=5000)
    conversation_id: int = Field(foreign_key="conversation.id")

class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    # Relationship
    conversation: Optional[Conversation] = Relationship(back_populates="messages")

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: int
    timestamp: datetime
```

### Updated Task Model (for reference)
The existing Task model remains unchanged but will be accessed through MCP tools.

```python
class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")  # Foreign key for user relationship
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
```

## Relationships
- One Conversation to Many Messages (one-to-many)
- One User to Many Conversations (one-to-many)
- One Conversation to Many Messages (one-to-many)

## Validation Rules
- Conversation title must be between 1 and 255 characters
- Message content must be between 1 and 5000 characters
- Message role must be one of: 'user', 'assistant', 'system'
- Conversation and Message records must be associated with a valid user
- Messages must be associated with a valid conversation

## State Transitions
- Conversation: Created when first message is sent, updated when new messages are added
- Message: Created when user sends message or AI responds