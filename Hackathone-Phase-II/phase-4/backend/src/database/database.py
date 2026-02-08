from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import urllib.parse

from ..config import settings

# Helper function to clean database URLs for asyncpg compatibility
def clean_database_url(url: str, is_async: bool = True) -> str:
    """Remove query parameters that asyncpg doesn't support"""
    if '?' in url:
        base_url, params = url.split('?', 1)
        param_dict = dict(p.split('=') for p in params.split('&') if '=' in p)
        
        # For asyncpg, we need to be selective about which parameters are supported
        if is_async:
            # Only keep parameters that asyncpg supports
            supported_params = {}
            for key, value in param_dict.items():
                # asyncpg supports sslmode but through different mechanisms
                if key.lower() not in ['channel_binding']:  # Remove unsupported parameters
                    supported_params[key] = value
        else:
            # For sync psycopg2, most parameters are supported
            supported_params = param_dict
        
        if supported_params:
            cleaned_params = '&'.join([f"{k}={v}" for k, v in supported_params.items()])
            return f"{base_url}?{cleaned_params}"
        else:
            return base_url
    return url

# Clean URLs for asyncpg compatibility
clean_sync_url = clean_database_url(settings.database_url, is_async=False)
clean_async_url = clean_database_url(settings.async_database_url, is_async=True)

# Determine if we're using SQLite (which doesn't support pooling parameters)
is_sqlite_sync = clean_sync_url.startswith('sqlite')
is_sqlite_async = clean_async_url.startswith('sqlite')

# Synchronous engine for general use
if is_sqlite_sync:
    # SQLite doesn't support pooling parameters
    sync_engine = create_engine(
        clean_sync_url,
        echo=settings.database_echo,  # Set to True for SQL query logging
        poolclass=None,               # Use NullPool for SQLite
    )
else:
    # PostgreSQL supports pooling parameters
    sync_engine = create_engine(
        clean_sync_url,
        echo=settings.database_echo,  # Set to True for SQL query logging
        pool_pre_ping=True,           # Verify connections before use
        pool_recycle=300,             # Recycle connections every 5 minutes
        pool_size=5,                  # Number of connections to maintain
        max_overflow=10,              # Additional connections beyond pool_size
        pool_timeout=30,              # Timeout for getting connection from pool
    )

# Async engine for async operations
if is_sqlite_async:
    # SQLite doesn't support pooling parameters
    async_engine = create_async_engine(
        clean_async_url,
        echo=settings.database_echo,  # Set to True for SQL query logging
        poolclass=None,               # Use NullPool for SQLite
    )
else:
    # PostgreSQL supports pooling parameters
    async_engine = create_async_engine(
        clean_async_url,
        echo=settings.database_echo,  # Set to True for SQL query logging
        pool_pre_ping=True,           # Verify connections before use
        pool_recycle=300,             # Recycle connections every 5 minutes
        pool_size=5,                  # Number of connections to maintain
        max_overflow=10,              # Additional connections beyond pool_size
        pool_timeout=30,              # Timeout for getting connection from pool
        connect_args={
            "server_settings": {
                "application_name": "todo-backend",
            },
            "statement_cache_size": 0,  # Disable statement caching to avoid issues with Neon schema changes
            "command_timeout": 30,
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