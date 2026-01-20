import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from sqlmodel import Session
from backend.src.services.auth_service import AuthService, AuthException
from backend.src.models.user import User
from backend.src.utils.date_validator import validate_signup_date


class TestAuthService:
    def setup_method(self):
        self.auth_service = AuthService()

    def test_create_access_token(self):
        """Test creating an access token."""
        user_id = 123
        expires_delta = timedelta(minutes=30)

        with patch('backend.src.services.auth_service.jwt.encode') as mock_encode, \
             patch('backend.src.services.auth_service.SECRET_KEY', 'test_secret'), \
             patch('backend.src.services.auth_service.ALGORITHM', 'HS256'):

            mock_encode.return_value = 'mocked_token'

            token = self.auth_service.create_access_token(user_id, expires_delta)

            assert token == 'mocked_token'
            mock_encode.assert_called_once()

    def test_verify_token_valid(self):
        """Test verifying a valid token."""
        token = 'valid_token'

        with patch('backend.src.services.auth_service.jwt.decode') as mock_decode, \
             patch('backend.src.services.auth_service.SECRET_KEY', 'test_secret'), \
             patch('backend.src.services.auth_service.ALGORITHM', 'HS256'):

            mock_decode.return_value = {'sub': '123'}

            result = self.auth_service.verify_token(token)

            assert result == 123
            mock_decode.assert_called_once()

    def test_verify_token_invalid(self):
        """Test verifying an invalid token."""
        token = 'invalid_token'

        with patch('backend.src.services.auth_service.jwt.decode') as mock_decode, \
             patch('backend.src.services.auth_service.SECRET_KEY', 'test_secret'), \
             patch('backend.src.services.auth_service.ALGORITHM', 'HS256'):

            mock_decode.side_effect = Exception('Invalid token')

            result = self.auth_service.verify_token(token)

            assert result is None

    @pytest.mark.asyncio
    async def test_authenticate_user_email_not_found(self):
        """Test authenticating a user with non-existent email."""
        session = Mock(spec=Session)
        email = 'nonexistent@example.com'
        password = 'somepassword'

        with patch('backend.src.services.auth_service.select') as mock_select:
            # Mock the query execution
            mock_exec = Mock()
            mock_exec.first.return_value = None  # No user found

            session.exec.return_value = mock_exec

            with pytest.raises(AuthException) as exc_info:
                await self.auth_service.authenticate_user(session, email, password)

            assert exc_info.value.error_type == "EMAIL_NOT_FOUND"

    @pytest.mark.asyncio
    async def test_authenticate_user_invalid_password(self):
        """Test authenticating a user with invalid password."""
        session = Mock(spec=Session)
        email = 'existing@example.com'
        password = 'wrongpassword'

        # Create a mock user
        mock_user = Mock(spec=User)
        mock_user.password = 'hashed_correct_password'
        mock_user.id = 1

        with patch('backend.src.services.auth_service.select') as mock_select, \
             patch('backend.src.services.auth_service.pwd_context') as mock_pwd_context:

            mock_exec = Mock()
            mock_exec.first.return_value = mock_user
            session.exec.return_value = mock_exec
            mock_pwd_context.verify.return_value = False  # Password is wrong

            with pytest.raises(AuthException) as exc_info:
                await self.auth_service.authenticate_user(session, email, password)

            assert exc_info.value.error_type == "INVALID_PASSWORD"

    @pytest.mark.asyncio
    async def test_authenticate_user_success(self):
        """Test successful authentication."""
        session = Mock(spec=Session)
        email = 'existing@example.com'
        password = 'correctpassword'

        # Create a mock user
        mock_user = Mock(spec=User)
        mock_user.password = 'hashed_correct_password'
        mock_user.id = 1
        mock_user.email = email

        with patch('backend.src.services.auth_service.select') as mock_select, \
             patch('backend.src.services.auth_service.pwd_context') as mock_pwd_context, \
             patch.object(self.auth_service, 'create_access_token') as mock_create_token:

            mock_exec = Mock()
            mock_exec.first.return_value = mock_user
            session.exec.return_value = mock_exec
            mock_pwd_context.verify.return_value = True  # Password is correct
            mock_create_token.return_value = 'mocked_token'

            result = await self.auth_service.authenticate_user(session, email, password)

            assert result['user'] == mock_user
            assert result['token'] == 'mocked_token'

    def test_register_user_success(self):
        """Test successful user registration."""
        session = Mock(spec=Session)
        email = 'newuser@example.com'
        password = 'newpassword'
        name = 'New User'

        with patch('backend.src.services.auth_service.select') as mock_select, \
             patch('backend.src.services.auth_service.pwd_context') as mock_pwd_context, \
             patch('backend.src.services.auth_service.validate_signup_date') as mock_validate, \
             patch.object(self.auth_service, 'create_access_token') as mock_create_token:

            # Mock no existing user found
            mock_exec = Mock()
            mock_exec.first.return_value = None
            session.exec.return_value = mock_exec

            mock_pwd_context.hash.return_value = 'hashed_newpassword'
            mock_validate.return_value = datetime.utcnow()
            mock_create_token.return_value = 'mocked_token'

            result = self.auth_service.register_user(session, email, password, name)

            assert result['token'] == 'mocked_token'
            assert result['user'].email == email
            assert result['user'].name == name
            session.add.assert_called_once()

    def test_register_user_duplicate_email(self):
        """Test registering a user with duplicate email."""
        session = Mock(spec=Session)
        email = 'existing@example.com'
        password = 'newpassword'

        # Create a mock existing user
        mock_existing_user = Mock(spec=User)
        mock_existing_user.email = email

        with patch('backend.src.services.auth_service.select') as mock_select:
            mock_exec = Mock()
            mock_exec.first.return_value = mock_existing_user
            session.exec.return_value = mock_exec

            with pytest.raises(AuthException) as exc_info:
                self.auth_service.register_user(session, email, password)

            assert exc_info.value.error_type == "EMAIL_EXISTS"