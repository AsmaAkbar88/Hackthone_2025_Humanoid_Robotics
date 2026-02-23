from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse, parse_qs, urlencode

from ..config import settings

# Helper function to clean database URLs for asyncpg compatibility
def clean_database_url(url: str, is_async: bool = True) -> str:
    """Remove query parameters that asyncpg doesn't support and ensure SSL is configured"""
    # Skip processing for SQLite
    if url.startswith('sqlite'):
        return url
    try:
        # Parse the URL properly
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query) if parsed.query else {}

        if is_async:
            # For async (asyncpg), remove parameters that asyncpg doesn't support
            # asyncpg doesn't support 'channel_binding' or 'sslmode' parameters
            # It handles SSL automatically for secure connections
            params_to_remove = ['channel_binding', 'sslmode', 'ssl']
            for param in params_to_remove:
                if param in query_params:
                    del query_params[param]
        else:
            # For sync (psycopg2), keep sslmode=require format
            # Just remove channel_binding which psycopg2 doesn't support
            if 'channel_binding' in query_params:
                del query_params['channel_binding']
            # Ensure sslmode is set to require for secure connection
            if 'sslmode' not in query_params:
                query_params['sslmode'] = ['require']

        # Rebuild the query string
        cleaned_params = urlencode(query_params, doseq=True)

        # Rebuild the URL
        cleaned_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if cleaned_params:
            cleaned_url += f"?{cleaned_params}"

        return cleaned_url
    except Exception as e:
        print(f"Error cleaning database URL: {e}")
        # Fallback: just remove the problematic params manually
        base_url = url.split('?')[0]
        if is_async:
            return f"{base_url}?ssl=true"
        else:
            return f"{base_url}?sslmode=require"

# Clean URLs for asyncpg compatibility (skip for SQLite)
clean_sync_url = clean_database_url(settings.database_url, is_async=False)
clean_async_url = clean_database_url(settings.async_database_url, is_async=True)

# Optional: Enable debug prints if needed - commented out by default
# print(f"DEBUG: Original sync URL: {settings.database_url}")
# print(f"DEBUG: Cleaned sync URL: {clean_sync_url}")
# print(f"DEBUG: Original async URL: {settings.async_database_url}")
# print(f"DEBUG: Cleaned async URL: {clean_async_url}")

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