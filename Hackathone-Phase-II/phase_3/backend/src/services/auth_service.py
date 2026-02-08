from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlmodel import Session, select
from jose import JWTError, jwt
import os
from ..models.user import User
from ..config import settings
from ..utils.date_validator import validate_signup_date

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm


class AuthException(Exception):
    """Custom exception for authentication-related errors"""
    def __init__(self, error_type: str, message: str):
        self.error_type = error_type
        self.message = message
        super().__init__(self.message)


class AuthService:
    def __init__(self):
        pass

    def create_access_token(self, user_id: int, expires_delta: Optional[timedelta] = None):
        """Create a new JWT access token for a user"""
        to_encode = {"sub": str(user_id)}

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

        to_encode.update({"exp": expire, "iat": datetime.utcnow()})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[int]:
        """Verify JWT token and return user ID if valid"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return int(user_id)
        except JWTError:
            return None

    def authenticate_user(self, session: Session, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with enhanced error handling to differentiate between email and password errors.

        Args:
            session: Database session
            email: User's email address
            password: User's password

        Returns:
            Dict with user info and token if authentication successful, None otherwise
        """
        # Find user by email
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        if user is None:
            # User with this email doesn't exist
            raise AuthException(
                error_type="EMAIL_NOT_FOUND",
                message="Invalid email or password"
            )

        # At this point, we know the email exists, so we check the password
        # Import here to avoid circular imports
        from passlib.context import CryptContext

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        if not pwd_context.verify(password, user.password):
            # Email exists but password is incorrect
            raise AuthException(
                error_type="INVALID_PASSWORD",
                message="Invalid email or password"
            )

        # Authentication successful
        token = self.create_access_token(user.id)
        return {
            "user": user,
            "token": token
        }

    def authenticate_user_detailed_errors(self, session: Session, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with detailed error messages for different error types.
        This method is used for the enhanced error handling feature.

        Args:
            session: Database session
            email: User's email address
            password: User's password

        Returns:
            Dict with user info and token if authentication successful, None otherwise
        """
        # Find user by email
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        if user is None:
            # User with this email doesn't exist
            raise AuthException(
                error_type="EMAIL_NOT_FOUND",
                message="No account found with this email address"
            )

        # At this point, we know the email exists, so we check the password
        # Import here to avoid circular imports
        from passlib.context import CryptContext

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        if not pwd_context.verify(password, user.password):
            # Email exists but password is incorrect
            raise AuthException(
                error_type="INVALID_PASSWORD",
                message="Incorrect password"
            )

        # Authentication successful
        token = self.create_access_token(user.id)
        return {
            "user": user,
            "token": token
        }

    def authenticate_user_secure(self, session: Session, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Secure authentication that doesn't reveal whether an email exists in the system.
        This maintains security best practices while still providing helpful feedback.

        Args:
            session: Database session
            email: User's email address
            password: User's password

        Returns:
            Dict with user info and token if authentication successful, None otherwise
        """
        # Find user by email
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        # Always perform password verification to prevent timing attacks
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        # If user doesn't exist, create a fake hash to compare against for timing consistency
        if user is None:
            # Use a fake password to maintain consistent timing
            pwd_context.hash("fake_password_for_timing_attack_prevention")
            raise AuthException(
                error_type="AUTH_FAILED",
                message="Invalid email or password"
            )

        # If user exists, verify the actual password
        if not pwd_context.verify(password, user.password):
            raise AuthException(
                error_type="AUTH_FAILED",
                message="Invalid email or password"
            )

        # Authentication successful
        token = self.create_access_token(user.id)
        return {
            "user": user,
            "token": token
        }

    def register_user(self, session: Session, email: str, password: str, name: Optional[str] = None,
                     date_of_birth: Optional[str] = None, signup_date: Optional[datetime] = None) -> Optional[Dict[str, Any]]:
        """
        Register a new user with signup date validation.

        Args:
            session: Database session
            email: User's email address
            password: User's password
            name: Optional user name
            date_of_birth: Optional date of birth
            signup_date: Signup date (will be set to now if not provided)

        Returns:
            Dict with user info and token if registration successful, None otherwise
        """
        # Check if user already exists
        statement = select(User).where(User.email == email)
        existing_user = session.exec(statement).first()

        if existing_user:
            raise AuthException(
                error_type="EMAIL_EXISTS",
                message="A user with this email already exists"
            )

        # Hash the password
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(password)

        # Validate and set signup date
        validated_signup_date = validate_signup_date(signup_date)

        # Create new user
        user = User(
            email=email,
            password=hashed_password,
            name=name,
            date_of_birth=date_of_birth,
            signup_date=validated_signup_date  # Non-nullable field
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        # Create access token
        token = self.create_access_token(user.id)

        return {
            "user": user,
            "token": token
        }