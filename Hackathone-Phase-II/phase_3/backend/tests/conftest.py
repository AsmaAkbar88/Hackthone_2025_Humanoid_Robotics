import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from src.database.database import AsyncSessionLocal, async_engine
from src.api.main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests."""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """Create a test client for the API."""
    from fastapi.testclient import TestClient

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def async_session():
    """Create an async database session for testing."""
    async with AsyncSessionLocal() as session:
        yield session