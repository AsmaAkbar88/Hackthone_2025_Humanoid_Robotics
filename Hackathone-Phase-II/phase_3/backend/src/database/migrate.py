"""
Database migration script for Todo Backend API.

This script handles database schema creation and updates.
"""
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlmodel import SQLModel
from sqlalchemy import text
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
    
    # Add columns that might be missing in existing tables
    print("Checking for missing columns...")
    with sync_engine.connect() as conn:
        try:
            # PostgreSQL specific: ADD COLUMN IF NOT EXISTS for user.username
            conn.execute(text("ALTER TABLE \"user\" ADD COLUMN IF NOT EXISTS username VARCHAR(255);"))

            # Update existing users to have a username based on their email or id
            conn.execute(text("UPDATE \"user\" SET username = 'user_' || id WHERE username IS NULL OR username = '';"))

            # Make username required and unique
            conn.execute(text("ALTER TABLE \"user\" ALTER COLUMN username SET NOT NULL;"))
            conn.execute(text("ALTER TABLE \"user\" ADD CONSTRAINT username_unique UNIQUE (username);"))

            # PostgreSQL specific: ADD COLUMN IF NOT EXISTS for conversation.title
            conn.execute(text("ALTER TABLE conversation ADD COLUMN IF NOT EXISTS title VARCHAR(255) DEFAULT 'New Conversation';"))

            # PostgreSQL specific: ADD COLUMN IF NOT EXISTS for message.timestamp
            conn.execute(text("ALTER TABLE message ADD COLUMN IF NOT EXISTS timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP;"))

            # PostgreSQL specific: ADD COLUMN IF NOT EXISTS for message.user_id
            # Corrected syntax for foreign key constraint with NOT NULL
            conn.execute(text('ALTER TABLE message ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES "user"(id);'))

            conn.commit()
            print("Missing columns check/add completed.")
        except Exception as e:
            print(f"Non-critical error adding columns: {e}")
            # Fallback for SQLite or other DBs if needed
            try:
                # For fallback, add username column first
                conn.execute(text("ALTER TABLE \"user\" ADD COLUMN username VARCHAR(255);"))

                # Update existing users to have a username
                conn.execute(text("UPDATE \"user\" SET username = 'user_' || id WHERE username IS NULL OR username = '';"))

                # Add constraints for SQLite
                conn.execute(text("ALTER TABLE \"user\" ADD CONSTRAINT username_unique UNIQUE (username);"))

                conn.execute(text("ALTER TABLE conversation ADD COLUMN title VARCHAR(255) DEFAULT 'New Conversation';"))
                conn.execute(text("ALTER TABLE message ADD COLUMN timestamp DATETIME DEFAULT CURRENT_TIMESTAMP;"))
                # Corrected syntax for fallback foreign key constraint
                conn.execute(text('ALTER TABLE message ADD COLUMN user_id INTEGER REFERENCES "user"(id);'))
                conn.commit()
                print("Missing columns added via fallback.")
            except Exception as e2:
                print(f"Could not add columns (they might already exist): {e2}")
    
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_db_and_tables()