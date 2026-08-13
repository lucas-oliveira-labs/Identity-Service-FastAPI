from unittest.mock import AsyncMock, Mock, patch
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException
from jose import JWTError

from src.schemas.auth import Login, ForgotPassword
from src.services.AuthService import AuthService


@pytest.fixture
def auth_service():
    return AuthService()


@pytest.mark.asyncio
async def test_login_user_not_found(auth_service):
    login = Login(
        email="user@exemple.com",
        password="123456",
    )

    with patch("src.services.AuthService.User.filter") as mock_filter:
        mock_filter.return_value.first = AsyncMock(return_value=None)

        with pytest.raises(HTTPException) as exc_info:
            await auth_service.login(login)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Credenciais inválidas"

    mock_filter.assert_called_once_with(email=login.email)


@pytest.mark.asyncio
async def test_login_invalid_password(auth_service):
    login = Login(
        email="user@exemple.com",
        password="wrong-password",
    )

    user = Mock()
    user.id = 1
    user.email = login.email
    user.password_hash = "hashed-password"

    with (
        patch("src.services.AuthService.User.filter") as mock_filter,
        patch(
            "src.services.AuthService.verify_password",
            return_value=False,
        ) as mock_verify_password,
    ):
        mock_filter.return_value.first = AsyncMock(return_value=user)

        with pytest.raises(HTTPException) as exc_info:
            await auth_service.login(login)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Credenciais inválidas"

    mock_verify_password.assert_called_once_with(
        login.password,
        user.password_hash,
    )


@pytest.mark.asyncio
async def test_login_success(auth_service):
    login = Login(
        email="user@example.com",
        password="correct-password",
    )

    user = Mock()
    user.id = 1
    user.email = login.email
    user.password_hash = "hashed-password"

    with (
        patch("src.services.AuthService.User.filter") as mock_user_filter,
        patch(
            "src.services.AuthService.verify_password",
            return_value=True,
        ) as mock_verify_password,
        patch(
            "src.services.AuthService.create_access_token",
            return_value="access-token",
        ) as mock_create_access_token,
        patch(
            "src.services.AuthService.create_refresh_token",
            return_value="refresh-token",
        ) as mock_create_refresh_token,
        patch("src.services.AuthService.RefreshToken.filter") as mock_token_filter,
        patch("src.services.AuthService.RefreshToken.create") as mock_token_create,
    ):
        mock_user_filter.return_value.first = AsyncMock(return_value=user)

        mock_token_filter.return_value.update = AsyncMock()

        mock_token_create.return_value = Mock()

        result = await auth_service.login(login)

    assert result == {
        "access_token": "access-token",
        "refresh_token": "refresh-token",
        "token_type": "bearer",
    }

    mock_user_filter.assert_called_once_with(
        email=login.email,
    )

    mock_verify_password.assert_called_once_with(
        login.password,
        user.password_hash,
    )

    mock_create_access_token.assert_called_once_with(
        {"sub": "1"},
    )

    mock_create_refresh_token.assert_called_once_with(
        {"sub": "1"},
    )

    mock_token_filter.assert_called_once_with(
        user=user,
        revoked=False,
    )

    mock_token_filter.return_value.update.assert_awaited_once_with(
        revoked=True,
    )

    mock_token_create.assert_awaited_once()

    create_kwargs = mock_token_create.call_args.kwargs

    assert create_kwargs["token"] == "refresh-token"
    assert create_kwargs["user"] == user
    assert create_kwargs["expires_at"] is not None


@pytest.mark.asyncio
async def test_refresh_token_invalid_jwt(auth_service):
    with patch(
        "src.services.AuthService.jwt.decode",
        side_effect=JWTError,
    ):
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.refresh_token("invalid-token")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid refresh token"


@pytest.mark.asyncio
async def test_refresh_token_wrong_type(auth_service):
    with patch(
        "src.services.AuthService.jwt.decode",
        return_value={
            "sub": "1",
            "type": "access",
        },
    ):
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.refresh_token("access-token")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "invalid refresh token"


@pytest.mark.asyncio
async def test_refresh_token_not_found(auth_service):
    with (
        patch(
            "src.services.AuthService.jwt.decode",
            return_value={
                "sub": "1",
                "type": "refresh",
            },
        ),
        patch("src.services.AuthService.RefreshToken.filter") as mock_filter,
    ):
        mock_filter.return_value.first = AsyncMock(return_value=None)

        with pytest.raises(HTTPException) as exc_info:
            await auth_service.refresh_token("refresh-token")

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Refresh token inválido"

        mock_filter.assert_called_once_with(token="refresh-token", revoked=False)


@pytest.mark.asyncio
async def test_refresh_token_expired(auth_service):
    stored_token = Mock()
    stored_token.id = 1
    stored_token.user_id = 10
    stored_token.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
    stored_token.delete = AsyncMock()

    with (
        patch(
            "src.services.AuthService.jwt.decode",
            return_value={
                "sub": "10",
                "type": "refresh",
            },
        ),
        patch("src.services.AuthService.RefreshToken.filter") as mock_filter,
    ):
        mock_filter.return_value.first = AsyncMock(return_value=stored_token)

        with pytest.raises(HTTPException) as exc_info:
            await auth_service.refresh_token("refresh-token")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Refresh token expirado"

    stored_token.delete.assert_awaited_once()


@pytest.mark.asyncio
async def test_refresh_token_without_sub(auth_service):
    stored_token = Mock()
    stored_token.id = 1
    stored_token.user_id = 10
    stored_token.expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

    with (
        patch(
            "src.services.AuthService.jwt.decode",
            return_value={
                "type": "refresh",
            },
        ),
        patch("src.services.AuthService.RefreshToken.filter") as mock_filter,
    ):
        mock_filter.return_value.first = AsyncMock(return_value=stored_token)

        mock_filter.return_value.update = AsyncMock()

        with pytest.raises(HTTPException) as exc_info:
            await auth_service.refresh_token("refresh-token")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Token inválido"

    mock_filter.return_value.update.assert_awaited_once_with(
        revoked=True,
    )


@pytest.mark.asyncio
async def test_refresh_token_success(auth_service):
    stored_token = Mock()
    stored_token.id = 1
    stored_token.user_id = 10
    stored_token.expires_at = datetime.now(timezone.utc) + timedelta(days=1)

    with (
        patch(
            "src.services.AuthService.jwt.decode",
            return_value={
                "sub": "10",
                "type": "refresh",
            },
        ),
        patch("src.services.AuthService.RefreshToken.filter") as mock_filter,
        patch("src.services.AuthService.RefreshToken.create") as mock_create,
        patch(
            "src.services.AuthService.create_access_token",
            return_value="new-access-token",
        ) as mock_access_token,
        patch(
            "src.services.AuthService.create_refresh_token",
            return_value="new-refresh-token",
        ) as mock_refresh_token,
    ):
        mock_filter.return_value.first = AsyncMock(return_value=stored_token)
        mock_filter.return_value.update = AsyncMock()
        mock_create.return_value = Mock()

        result = await auth_service.refresh_token("old-refresh-token")

    assert result == {
        "access_token": "new-access-token",
        "refresh_token": "new-refresh-token",
        "token_type": "bearer",
    }

    mock_filter.return_value.update.assert_awaited_once_with(
        revoked=True,
    )

    mock_access_token.assert_called_once_with(
        {"sub": "10"},
    )

    mock_refresh_token.assert_called_once_with(
        {"sub": "10"},
    )

    mock_create.assert_awaited_once()

    create_kwargs = mock_create.call_args.kwargs

    assert create_kwargs["token"] == "new-refresh-token"
    assert create_kwargs["user_id"] == 10
    assert create_kwargs["expires_at"] is not None


@pytest.mark.asyncio
async def test_lougot(auth_service):
    current_user = Mock()

    with patch("src.service.AuthService.RefreshToken.filter") as mock_filter:
        mock_filter.return_value.update = AsyncMock()

        result = await auth_service.lougout(current_user)

    assert result == {"message": "Logout realizado com sucesso."}

    mock_filter.assert_called_once_with(user=current_user, revoked=False)

    mock_filter.return_value.update.assert_awaited_once_with(revoked=True)


@pytest.mark.asyncio
async def test_forgot_password_user_not_found(auth_service):
    data = ForgotPassword(
        email="notfound@exemple.com",
    )

    with patch("src.services.AuthService.User.filter") as mock_filter:
        mock_filter.return_value.first = AsyncMock(return_value=None)

        result = await auth_service.forgot_password(data)

    assert result == {
        "message": (
            "Se o email estiver cadastrado, voce receberá"
            "um link para redefinir sua senha."
        )
    }
