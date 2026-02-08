"""
Authentication middleware for chat endpoints in the Todo Backend API.

Handles JWT validation specifically for chat endpoints.
"""
from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from ..config import settings
from ..utils.jwt_utils import decode_access_token
from ..models.user import UserRead
from sqlmodel.ext.asyncio.session import AsyncSession
from ..database.database import get_async_session
from sqlmodel import select


class ChatAuthMiddleware:
    """
    Middleware to handle authentication for chat endpoints.
    Validates JWT tokens and ensures user access rights.
    """
    
    def __init__(self):
        self.security = HTTPBearer()
    
    async def verify_token(self, token: str, user_id: int) -> Optional[UserRead]:
        """
        Verify the JWT token and ensure it belongs to the specified user_id.
        
        Args:
            token: JWT token to verify
            user_id: Expected user ID from the endpoint path
            
        Returns:
            UserRead object if token is valid and belongs to user_id, None otherwise
        """
        try:
            payload = decode_access_token(token)
            token_user_id: str = payload.get("sub")
            
            if token_user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
                
            # Convert to int for comparison
            token_user_id_int = int(token_user_id)
            
            # Check if the token user_id matches the requested user_id
            if token_user_id_int != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: Token does not match requested user"
                )
                
            # Here we would typically fetch user details from the database
            # For now, we'll return a basic UserRead object
            return UserRead(
                id=token_user_id_int,
                email="placeholder@example.com"  # This would come from DB in real implementation
            )
            
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except ValueError:
            # Handle case where token_user_id is not a valid integer
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format",
                headers={"WWW-Authenticate": "Bearer"},
            )


# Global instance
chat_auth = ChatAuthMiddleware()