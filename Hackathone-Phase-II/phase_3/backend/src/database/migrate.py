"""
Database migration script for Todo Backend API.

This script handles database schema creation and updates.
"""
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlmodel import SQLModel
from .database import sync_engine
from ..models.user import User
from ..models.task import Task
from ..models.conversation import Conversation
from ..models.message import Message


def create_db_and_tables():
    """Create database tables based on SQLModel models."""
    print("Creating database tables...")
    
    # Create all tables
    SQLModel.metadata.create_all(bind=sync_engine)
    
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_db_and_tables()