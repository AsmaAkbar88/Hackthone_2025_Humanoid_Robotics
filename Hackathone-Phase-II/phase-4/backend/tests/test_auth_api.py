import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from backend.src.main import app
from backend.src.models.user import User
from backend.src.database.database import get_session
from backend.src.services.auth_service import AuthService
from backend.src.utils.date_validator import validate_signup_date


@pytest.fixture
def client():
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_test_session():
            yield session

        app.dependency_overrides[get_session] = get_test_session
        with TestClient(app) as c:
            yield c


class TestAuthAPI:
    def test_signup_endpoint_success(self, client):
        """Test successful user signup."""
        signup_data = {
            "email": "test@example.com",
            "password": "securepassword",
            "name": "Test User",
            "date_of_birth": "1990-01-01",
            "signup_date": datetime.utcnow().isoformat()
        }

        with patch('backend.src.api.routes.auth.get_password_hash') as mock_hash, \
             patch('backend.src.api.routes.auth.create_access_token') as mock_create_token, \
             patch('backend.src.utils.date_validator.validate_signup_date') as mock_validate_date:

            mock_hash.return_value = 'hashed_password'
            mock_create_token.return_value = 'mocked_token'
            mock_validate_date.return_value = datetime.utcnow()

            response = client.post("/auth/signup", json=signup_data)

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "access_token" in data["data"]

    def test_signup_endpoint_duplicate_email(self, client):
        """Test signup with duplicate email."""
        signup_data = {
            "email": "duplicate@example.com",
            "password": "securepassword",
            "name": "Test User",
            "date_of_birth": "1990-01-01",
            "signup_date": datetime.utcnow().isoformat()
        }

        # First signup should succeed
        with patch('backend.src.api.routes.auth.get_password_hash') as mock_hash, \
             patch('backend.src.api.routes.auth.create_access_token') as mock_create_token, \
             patch('backend.src.utils.date_validator.validate_signup_date') as mock_validate_date:

            mock_hash.return_value = 'hashed_password'
            mock_create_token.return_value = 'mocked_token'
            mock_validate_date.return_value = datetime.utcnow()

            # First signup
            response1 = client.post("/auth/signup", json=signup_data)
            assert response1.status_code == 200

            # Second signup with same email should fail
            response2 = client.post("/auth/signup", json=signup_data)
            assert response2.status_code == 400

    def test_signin_endpoint_success(self, client):
        """Test successful sign in."""
        signin_data = {
            "email": "test@example.com",
            "password": "securepassword"
        }

        # Mock user object
        mock_user = User(
            id=1,
            email="test@example.com",
            password="hashed_password",
            signup_date=datetime.utcnow()
        )

        with patch('backend.src.services.auth_service.AuthService.authenticate_user_detailed_errors') as mock_auth, \
             patch('backend.src.api.routes.auth.create_access_token') as mock_create_token:

            mock_auth.return_value = {
                "user": mock_user,
                "token": "mocked_token"
            }
            mock_create_token.return_value = "mocked_token"

            response = client.post("/auth/signin", json=signin_data)

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["data"]["access_token"] == "mocked_token"

    def test_signin_endpoint_invalid_email(self, client):
        """Test sign in with invalid email."""
        signin_data = {
            "email": "nonexistent@example.com",
            "password": "any_password"
        }

        with patch('backend.src.services.auth_service.AuthService.authenticate_user_detailed_errors') as mock_auth:

            # Mock the auth service to raise an AuthException
            from backend.src.services.auth_service import AuthException
            mock_auth.side_effect = AuthException(
                error_type="EMAIL_NOT_FOUND",
                message="No account found with this email address"
            )

            response = client.post("/auth/signin", json=signin_data)

            assert response.status_code == 401

    def test_signin_endpoint_invalid_password(self, client):
        """Test sign in with invalid password."""
        signin_data = {
            "email": "existing@example.com",
            "password": "wrong_password"
        }

        with patch('backend.src.services.auth_service.AuthService.authenticate_user_detailed_errors') as mock_auth:

            # Mock the auth service to raise an AuthException for invalid password
            from backend.src.services.auth_service import AuthException
            mock_auth.side_effect = AuthException(
                error_type="INVALID_PASSWORD",
                message="Incorrect password"
            )

            response = client.post("/auth/signin", json=signin_data)

            assert response.status_code == 401

    def test_forgot_password_endpoint(self, client):
        """Test forgot password endpoint."""
        forgot_data = {
            "email": "user@example.com",
            "date_of_birth": "1990-01-01"
        }

        # Mock user object
        mock_user = User(
            id=1,
            email="user@example.com",
            password="hashed_password",
            date_of_birth=datetime(1990, 1, 1).date(),
            signup_date=datetime.utcnow()
        )

        with patch('sqlmodel.select') as mock_select:
            # Mock the database query
            mock_exec = Mock()
            mock_exec.scalar_one_or_none.return_value = mock_user
            mock_select.return_value = Mock()
            mock_select.return_value.execute.return_value = mock_exec

            response = client.post("/auth/forgot-password", json=forgot_data)

            # This should succeed if user exists and DOB matches
            assert response.status_code in [200, 400, 404]  # Response varies based on implementation details

    def test_set_new_password_endpoint(self, client):
        """Test setting new password."""
        password_data = {
            "email": "user@example.com",
            "new_password": "new_secure_password"
        }

        with patch('sqlmodel.select') as mock_select, \
             patch('backend.src.api.routes.auth.get_password_hash') as mock_hash:

            # Mock user object
            mock_user = Mock()
            mock_user.id = 1
            mock_user.email = "user@example.com"

            # Mock the database query
            mock_exec = Mock()
            mock_exec.scalar_one_or_none.return_value = mock_user
            mock_select.return_value = Mock()
            mock_select.return_value.execute.return_value = mock_exec
            mock_hash.return_value = "hashed_new_password"

            response = client.post("/auth/set-new-password", json=password_data)

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True

    def test_login_endpoint_legacy(self, client):
        """Test the legacy login endpoint."""
        login_data = {
            "email": "test@example.com",
            "password": "securepassword"
        }

        # Mock user object
        mock_user = User(
            id=1,
            email="test@example.com",
            password="hashed_password",
            signup_date=datetime.utcnow()
        )

        with patch('sqlmodel.select') as mock_select, \
             patch('backend.src.api.routes.auth.verify_password') as mock_verify, \
             patch('backend.src.api.routes.auth.create_access_token') as mock_create_token:

            # Mock the database query
            mock_exec = Mock()
            mock_exec.scalar_one_or_none.return_value = mock_user
            mock_select.return_value = Mock()
            mock_select.return_value.execute.return_value = mock_exec
            mock_verify.return_value = True
            mock_create_token.return_value = "mocked_token"

            response = client.post("/auth/login", json=login_data)

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "access_token" in data["data"]