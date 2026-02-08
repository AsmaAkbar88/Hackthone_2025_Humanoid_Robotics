from typing import Optional
from sqlmodel import Session, select
from datetime import datetime
from ..models.user import User, UserCreate, UserRead
from ..utils.date_validator import validate_signup_date


class UserService:
    def __init__(self):
        pass

    def get_user_by_email(self, session: Session, email: str) -> Optional[User]:
        """Retrieve a user by their email address."""
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        return user

    def get_user_by_id(self, session: Session, user_id: int) -> Optional[User]:
        """Retrieve a user by their ID."""
        user = session.get(User, user_id)
        return user

    def create_user(self, session: Session, user_data: UserCreate, signup_date: Optional[datetime] = None) -> User:
        """
        Create a new user with proper signup date validation.

        Args:
            session: Database session
            user_data: User creation data
            signup_date: Signup date (defaults to current time if not provided)

        Returns:
            User: The created user object
        """
        # Validate and set signup date
        validated_signup_date = validate_signup_date(signup_date)

        # Create user object with validated signup date
        user = User(
            email=user_data.email,
            password=user_data.password,  # Should be hashed before this
            name=user_data.name,
            date_of_birth=getattr(user_data, 'date_of_birth', None),
            signup_date=validated_signup_date  # Non-nullable field, enforced here
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    def update_user(self, session: Session, user_id: int, **kwargs) -> Optional[User]:
        """Update user information."""
        user = session.get(User, user_id)
        if not user:
            return None

        # Update allowed fields
        for field, value in kwargs.items():
            if hasattr(user, field):
                setattr(user, field, value)

        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    def delete_user(self, session: Session, user_id: int) -> bool:
        """Delete a user by ID."""
        user = session.get(User, user_id)
        if not user:
            return False

        session.delete(user)
        session.commit()
        return True

    def validate_user_data(self, user_data: UserCreate) -> dict:
        """
        Validate user data before creating/updating.

        Args:
            user_data: User data to validate

        Returns:
            dict: Validation results with 'valid' boolean and 'errors' list
        """
        errors = []

        # Validate email format (basic check)
        if '@' not in user_data.email or '.' not in user_data.email.split('@')[1]:
            errors.append("Invalid email format")

        # Validate password strength (basic check)
        if len(user_data.password) < 6:
            errors.append("Password must be at least 6 characters long")

        # Validate signup date if provided
        if hasattr(user_data, 'signup_date') and user_data.signup_date is not None:
            try:
                validate_signup_date(user_data.signup_date)
            except ValueError as e:
                errors.append(str(e))

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def get_all_users(self, session: Session, skip: int = 0, limit: int = 100) -> list[User]:
        """Retrieve all users with pagination."""
        statement = select(User).offset(skip).limit(limit)
        users = session.exec(statement).all()
        return users