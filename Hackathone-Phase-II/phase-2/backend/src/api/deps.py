from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from sqlmodel import select
from datetime import datetime

from ..utils.jwt_utils import decode_access_token
from ..models.user import User, UserRead
from ..database.database import get_async_session
from sqlmodel.ext.asyncio.session import AsyncSession

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_async_session)
) -> UserRead:
    """
    Dependency to get the current authenticated user from the JWT token.

    Args:
        credentials: HTTP authorization credentials from the request
        session: Async database session

    Returns:
        UserRead object if token is valid and user exists

    Raises:
        HTTPException: If token is invalid, expired, or user doesn't exist
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Fetch the user from the database
    user = await session.get(User, int(user_id))
    if user is None:
        raise credentials_exception

    # Create UserRead object manually to ensure required fields are present
    # This handles potential issues with datetime fields being None
    from datetime import datetime
    created_at = user.created_at or datetime.utcnow()
    updated_at = user.updated_at or datetime.utcnow()

    return UserRead(
        id=user.id,
        email=user.email,
        name=user.name,
        date_of_birth=user.date_of_birth,
        signup_date=user.signup_date,
        force_password_change=user.force_password_change,
        created_at=created_at,
        updated_at=updated_at
    )