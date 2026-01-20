from functools import wraps
from typing import Callable, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .deps import get_current_user
from ..models.user import UserRead

security = HTTPBearer()

def require_auth(func: Callable) -> Callable:
    """
    Decorator to require authentication for API endpoints.

    This decorator ensures that the user is authenticated before allowing access to the endpoint.
    It uses the get_current_user dependency to validate the JWT token.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # The get_current_user dependency will automatically validate the token
        # and raise an HTTPException if the token is invalid
        current_user: UserRead = kwargs.get('current_user') or args[-1]  # Assuming current_user is passed as a param

        # If we reach this point, the user is authenticated
        return await func(*args, **kwargs)

    # Add the dependency to the wrapper function
    wrapper.__annotations__['current_user'] = UserRead
    wrapper.__defaults__ = (Depends(get_current_user),)

    return wrapper

def auth_required():
    """
    Alternative decorator to require authentication for API endpoints.

    This is a more explicit way to add authentication to routes.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        # Inject the dependency
        if 'current_user' not in func.__annotations__:
            func.__annotations__['current_user'] = UserRead
        if 'current_user' not in kwargs:
            kwargs['current_user'] = Depends(get_current_user)

        return wrapper
    return decorator

# Alternative implementation that works better with FastAPI's dependency injection
def get_auth_dependency():
    """
    Helper function to get the authentication dependency.

    This can be used in route definitions like:
    @router.get("/protected", dependencies=[Depends(get_auth_dependency())])
    """
    return Depends(get_current_user)