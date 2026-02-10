from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import urllib.parse

from ..config import settings

def is_sqlite_db(database_url: str) -> bool:
    """Check if the database URL is for SQLite."""
    parsed = urllib.parse.urlparse(database_url)
    return parsed.scheme.lower().startswith('sqlite')

def clean_database_url(database_url: str) -> str:
    """Remove unsupported parameters from database URL for compatibility."""
    if is_sqlite_db(database_url):
        return database_url
    
    # Parse the URL to remove unsupported parameters
    parsed = urllib.parse.urlparse(database_url)
    query_params = urllib.parse.parse_qs(parsed.query)
    
    # Remove unsupported parameters
    unsupported_params = {'channel_binding', 'sslmode'}
    for param in unsupported_params:
        query_params.pop(param, None)
    
    # Reconstruct the URL without unsupported parameters
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    cleaned_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
    
    return cleaned_url

def get_sync_pg_url(database_url: str) -> str:
    """Ensures a PostgreSQL URL uses a synchronous driver (psycopg2 by default)."""
    if database_url.startswith("postgresql+asyncpg://"):
        return database_url.replace("postgresql+asyncpg://", "postgresql://", 1)
    return database_url

# Determine if we're using SQLite
using_sqlite = is_sqlite_db(settings.database_url)

# Clean database URLs for compatibility
cleaned_database_url = clean_database_url(settings.database_url)
cleaned_async_database_url = clean_database_url(settings.async_database_url)

# Ensure sync engine uses a synchronous PG driver if applicable
sync_db_url_for_engine = get_sync_pg_url(cleaned_database_url)

# Synchronous engine for general use
if using_sqlite:
    # SQLite doesn't support connection pooling options
    sync_engine = create_engine(
        sync_db_url_for_engine,
        echo=settings.database_echo,  # Set to True for SQL query logging
    )
else:
    # PostgreSQL supports connection pooling options
    sync_engine = create_engine(
        sync_db_url_for_engine,
        echo=settings.database_echo,  # Set to True for SQL query logging
        pool_pre_ping=True,           # Verify connections before use
        pool_recycle=300,             # Recycle connections every 5 minutes
        pool_size=5,                  # Number of connections to maintain
        max_overflow=10,              # Additional connections beyond pool_size
        pool_timeout=30,              # Timeout for getting connection from pool
    )

# Async engine for async operations
if is_sqlite_db(cleaned_async_database_url):
    # SQLite doesn't support connection pooling options
    async_engine = create_async_engine(
        cleaned_async_database_url,
        echo=settings.database_echo,  # Set to True for SQL query logging
    )
else:
    # PostgreSQL supports connection pooling options
    async_engine = create_async_engine(
        cleaned_async_database_url,
        echo=settings.database_echo,  # Set to True for SQL query logging
        pool_pre_ping=True,           # Verify connections before use
        pool_recycle=300,             # Recycle connections every 5 minutes
        pool_size=5,                  # Number of connections to maintain
        max_overflow=10,              # Additional connections beyond pool_size
        pool_timeout=30,              # Timeout for getting connection from pool,
        connect_args={
            "ssl": "require",
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