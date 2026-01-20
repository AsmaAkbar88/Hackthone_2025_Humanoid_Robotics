from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..config import settings

# Synchronous engine for general use
sync_engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,  # Set to True for SQL query logging
    pool_pre_ping=True,           # Verify connections before use
    pool_recycle=300,             # Recycle connections every 5 minutes
    pool_size=5,                  # Number of connections to maintain
    max_overflow=10,              # Additional connections beyond pool_size
    pool_timeout=30,              # Timeout for getting connection from pool
)

# Async engine for async operations (recommended for Neon Serverless PostgreSQL)
async_engine = create_async_engine(
    settings.async_database_url,
    echo=settings.database_echo,  # Set to True for SQL query logging
    pool_pre_ping=True,           # Verify connections before use
    pool_recycle=300,             # Recycle connections every 5 minutes
    pool_size=5,                  # Number of connections to maintain
    max_overflow=10,              # Additional connections beyond pool_size
    pool_timeout=30,              # Timeout for getting connection from pool
    connect_args={
        "server_settings": {
            "application_name": "todo-backend",
        }
    }
)

# Session makers
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
    expire_on_commit=False
)


def get_sync_session():
    """Get a synchronous database session."""
    session = SyncSessionLocal()
    try:
        yield session
    finally:
        session.close()


async def get_async_session():
    """Get an asynchronous database session."""
    async with AsyncSessionLocal() as session:
        yield session
        await session.close()