from typing import Optional, Union
from datetime import datetime, date
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """Base model for User with common fields."""
    email: str = Field(unique=True, nullable=False, max_length=255)
    username: Optional[str] = Field(default=None, nullable=True, max_length=255)  # String identifier for MCP tools


class User(UserBase, table=True):
    """User model for the database table."""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: Optional[str] = Field(default=None, nullable=True, unique=True, max_length=255)  # String identifier for MCP tools
    password: str = Field(nullable=False, max_length=255)  # Hashed password
    name: Optional[str] = Field(default=None, max_length=255)  # Optional name field
    date_of_birth: Optional[date] = Field(default=None, nullable=True)  # Date of birth
    signup_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)  # Non-nullable signup date
    force_password_change: bool = Field(default=False)  # Flag to indicate if user needs to change password
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})


class UserCreate(UserBase):
    """Model for creating a new user."""
    password: str
    name: Optional[str] = None
    date_of_birth: Optional[Union[str, datetime]] = None  # Date of birth as string or datetime
    # username is inherited from UserBase


class UserRead(UserBase):
    """Model for reading user data."""
    id: int
    username: str  # Include username in read model
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    signup_date: datetime  # Include signup_date in read model
    force_password_change: bool = False
    created_at: datetime
    updated_at: datetime