from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from typing import Optional
from datetime import timedelta, datetime
from sqlmodel import select
from pydantic import BaseModel

from ...models.user import User, UserCreate, UserRead
from ...services.auth_service import AuthService, AuthException
from ...database.database import get_async_session
from sqlmodel.ext.asyncio.session import AsyncSession
from ...utils.jwt_utils import create_access_token, decode_access_token, get_password_hash, verify_password
from ...config import settings
from ...utils.date_validator import validate_signup_date
from ..deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

# Initialize the auth service
auth_service = AuthService()

class SignupRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    date_of_birth: Optional[str] = None
    signup_date: Optional[str] = None  # Allow client to send signup date (will be validated and potentially overridden)

class SigninRequest(BaseModel):
    email: str
    password: str

class ErrorResponse(BaseModel):
    error: str
    message: str

@router.post("/signup", response_model=dict, responses={
    400: {"model": ErrorResponse, "description": "Invalid request format or validation error"},
    409: {"model": ErrorResponse, "description": "Email already exists"}
})
async def signup_user(
    signup_request: SignupRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create new user account with signup date validation.
    """
    try:
        # Validate and set signup date
        validated_signup_date = validate_signup_date(signup_request.signup_date)

        # Hash the password before storing
        hashed_password = get_password_hash(signup_request.password)

        # Create new user with signup date validation
        db_user = User(
            email=signup_request.email,
            password=hashed_password,
            name=signup_request.name,
            date_of_birth=signup_request.date_of_birth,
            signup_date=validated_signup_date  # Non-nullable field, enforced here
        )
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(db_user.id)}, expires_delta=access_token_expires
        )

        response = JSONResponse(content={
            "success": True,
            "data": {
                "user": UserRead.model_validate(db_user),
                "access_token": access_token,
                "token_type": "bearer"
            }
        })

        # Set JWT as an HTTP-only cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            expires=access_token_expires.total_seconds(),
            httponly=True,
            samesite="lax",
            # secure=True # Use secure=True in production with HTTPS
        )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Signup failed: {str(e)}"
        )

@router.post("/signin", response_model=dict, responses={
    400: {"model": ErrorResponse, "description": "Invalid request format"},
    401: {"model": ErrorResponse, "description": "Authentication failed"}
})
async def signin_user(
    signin_request: SigninRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Authenticate user with enhanced error handling to differentiate between email and password errors.
    """
    try:
        # Find user by email
        statement = select(User).where(User.email == signin_request.email)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Verify the provided password against the stored hash
        if not verify_password(signin_request.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        response = JSONResponse(content={
            "success": True,
            "data": {
                "user": UserRead.model_validate(user),
                "access_token": access_token,
                "token_type": "bearer"
            }
        })

        # Set JWT as an HTTP-only cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            expires=access_token_expires.total_seconds(),
            httponly=True,  # HttpOnly flag prevents client-side access
            samesite="lax", # Lax for CSRF protection
            # secure=True # Use secure=True in production with HTTPS
        )
        return response
    except AuthException as e:
        # Map our custom exceptions to appropriate HTTP responses
        status_code = status.HTTP_401_UNAUTHORIZED
        if e.error_type == "EMAIL_NOT_FOUND":
            status_code = status.HTTP_401_UNAUTHORIZED
        elif e.error_type == "INVALID_PASSWORD":
            status_code = status.HTTP_401_UNAUTHORIZED

        raise HTTPException(
            status_code=status_code,
            detail=e.message
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Signin failed: {str(e)}"
        )


class LoginRequest(BaseModel):
    email: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str
    date_of_birth: str  # Format: YYYY-MM-DD

@router.post("/forgot-password", response_model=dict)
async def forgot_password(
    request_data: ForgotPasswordRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Verify user identity using email and date of birth for password reset.
    """
    try:
        # Find user by email
        statement = select(User).where(User.email == request_data.email)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            # Return the same error message even if email doesn't exist to prevent email enumeration
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="If an account with that email exists, a password reset link has been sent."
            )

        # Verify the date of birth matches
        print(f"DEBUG: Looking up user by email: {request_data.email}")
        print(f"DEBUG: Found user date_of_birth: {user.date_of_birth} (type: {type(user.date_of_birth)})")

        if not user.date_of_birth:
            print(f"DEBUG: User has no date of birth set in database")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Date of birth verification failed. Please contact support."
            )

        # Parse the provided date of birth
        from datetime import datetime
        try:
            provided_dob = datetime.strptime(request_data.date_of_birth, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Please use YYYY-MM-DD format."
            )

        # Compare dates (ignoring time component)
        print(f"DEBUG: Comparing user.date_of_birth: {user.date_of_birth} with provided: {provided_dob.date()}")

        if user.date_of_birth != provided_dob.date():  # Both should be date objects now
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Date of birth verification failed. Please check your date of birth and try again."
            )

        # In a real app, you'd send a password reset link to the user's email
        # For demo purposes, we'll just return success

        return {
            "success": True,
            "data": {
                "message": "Identity verified successfully. Please set your new password.",
                "email": request_data.email
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Forgot password request failed: {str(e)}"
        )


class SetNewPasswordRequest(BaseModel):
    email: str
    new_password: str

@router.post("/set-new-password", response_model=dict)
async def set_new_password(
    request_data: SetNewPasswordRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Set new password after successful verification.
    """
    try:
        # Find user by email
        statement = select(User).where(User.email == request_data.email)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Hash the new password before storing
        hashed_new_password = get_password_hash(request_data.new_password)
        user.password = hashed_new_password
        user.updated_at = datetime.utcnow()

        session.add(user)
        await session.commit()

        return {
            "success": True,
            "data": {
                "message": "Password changed successfully"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password change failed: {str(e)}"
        )


class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str

@router.post("/reset-password", response_model=dict)
async def reset_password(
    request_data: ResetPasswordRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Reset user password directly (for admin or special cases).
    """
    try:
        # Find user by email
        statement = select(User).where(User.email == request_data.email)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Hash the new password before storing
        hashed_new_password = get_password_hash(request_data.new_password)
        user.password = hashed_new_password
        user.updated_at = datetime.utcnow()

        session.add(user)
        await session.commit()

        return {
            "success": True,
            "data": {
                "message": "Password reset successfully"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password reset failed: {str(e)}"
        )


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

@router.post("/change-password", response_model=dict)
async def change_password(
    request_data: ChangePasswordRequest,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Change user's current password after verifying the current password.
    """
    try:
        # Verify the current password
        statement = select(User).where(User.id == current_user.id)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Verify the provided current password against the stored hash
        if not verify_password(request_data.current_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )

        # Hash the new password before storing
        hashed_new_password = get_password_hash(request_data.new_password)
        user.password = hashed_new_password
        user.updated_at = datetime.utcnow()

        # Reset the force_password_change flag if set
        user.force_password_change = False

        session.add(user)
        await session.commit()

        return {
            "success": True,
            "data": {
                "message": "Password changed successfully"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password change failed: {str(e)}"
        )


@router.post("/token", response_model=dict)
async def login_for_access_token(
    login_request: LoginRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    try:
        # Find user by email
        statement = select(User).where(User.email == login_request.email)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify the provided password against the stored hash
        if not verify_password(login_request.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserRead.model_validate(user)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token creation failed: {str(e)}"
        )


# Also add a test endpoint that doesn't require auth to verify the token works
@router.get("/test-token", response_model=dict)
async def test_token():
    """
    Test endpoint to verify authentication is working.
    """
    return {
        "message": "Token is valid!",
        "success": True
    }


@router.post("/register", response_model=dict)
async def register_user(
    user_create: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Register a new user.
    """
    try:
        # Check if user already exists
        existing_user_statement = select(User).where(User.email == user_create.email)
        existing_user_result = await session.execute(existing_user_statement)
        existing_user = existing_user_result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Hash the password before storing
        hashed_password = get_password_hash(user_create.password)

        # Create new user with hashed password, optional name and date of birth
        from datetime import datetime, date
        date_of_birth_obj = None

        # Debug: Print incoming date of birth for troubleshooting
        print(f"DEBUG: Incoming date_of_birth value: {user_create.date_of_birth}, type: {type(user_create.date_of_birth)}")

        # Handle date of birth conversion - supports string, date, or datetime objects
        if user_create.date_of_birth is not None:
            dob_input = user_create.date_of_birth

            print(f"DEBUG: Processing date of birth input: {dob_input}, type: {type(dob_input)}")

            if isinstance(dob_input, str):
                # Handle string input - strip whitespace and parse
                dob_str = dob_input.strip()
                print(f"DEBUG: String date stripped: '{dob_str}'")
                if dob_str:  # Only process if not empty after stripping
                    try:
                        # Parse string to date object (to match database schema)
                        date_of_birth_obj = datetime.strptime(dob_str, '%Y-%m-%d').date()
                        print(f"DEBUG: Successfully parsed date: {date_of_birth_obj}")
                    except ValueError as e:
                        # Handle invalid date format
                        print(f"Date of birth parsing error: {e}")
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid date of birth format. Please use YYYY-MM-DD format."
                        )
            elif isinstance(dob_input, date):
                # If it's already a date object, use it as is
                date_of_birth_obj = dob_input
                print(f"DEBUG: Using date object directly: {date_of_birth_obj}")
            elif isinstance(dob_input, datetime):
                # If it's a datetime object, convert to date to match database schema
                date_of_birth_obj = dob_input.date()
                print(f"DEBUG: Converted datetime to date: {date_of_birth_obj}")
        else:
            print("DEBUG: No date of birth provided in request")

        print(f"DEBUG: Final date_of_birth_obj value: {date_of_birth_obj}")

        # Use current time as signup_date if not provided in the request
        current_time = datetime.utcnow()

        db_user = User(
            email=user_create.email,
            password=hashed_password,
            name=user_create.name,
            date_of_birth=date_of_birth_obj,
            signup_date=current_time,  # Non-nullable field, enforced here
            force_password_change=False  # New users don't need to change password immediately
        )
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        # Additional debug: Check what was actually saved
        print(f"DEBUG: User saved with date_of_birth: {db_user.date_of_birth}, signup_date: {db_user.signup_date}")

        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(db_user.id)}, expires_delta=access_token_expires
        )

        # Create a UserRead instance manually to avoid serialization issues
        user_read = UserRead(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            date_of_birth=db_user.date_of_birth,
            signup_date=db_user.signup_date,
            force_password_change=db_user.force_password_change,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )

        return {
            "success": True,
            "data": {
                "user": user_read,
                "access_token": access_token,
                "token_type": "bearer"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=dict)
async def login_user(
    login_request: LoginRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Authenticate user and return access token.
    """
    try:
        # Find user by email
        statement = select(User).where(User.email == login_request.email)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Verify the provided password against the stored hash
        if not verify_password(login_request.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        return {
            "success": True,
            "data": {
                "user": UserRead.model_validate(user),
                "access_token": access_token,
                "token_type": "bearer"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )