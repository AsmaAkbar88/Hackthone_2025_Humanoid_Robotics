from typing import Optional
from datetime import datetime

import sqlalchemy as sa
from sqlmodel import Field, SQLModel, ForeignKey


class TaskBase(SQLModel):
    """Base model for Task with common fields."""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class TaskCreate(TaskBase):
    """Model for creating a new task."""
    pass  # user_id will be set by the service layer


class TaskUpdate(SQLModel):
    """Model for updating task data."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None


class Task(TaskBase, table=True):
    """Task model for the database table."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # String identifier for user (matches database schema)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})


class TaskRead(TaskBase):
    """Model for reading task data."""
    id: int
    user_id: str  # Include user_id in read model as string
    created_at: datetime
    updated_at: datetime