from datetime import UTC, datetime
from unittest.mock import patch

import pytest
from jose import JWTError, jwt

from src.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from src.services.jwt_service import (
    create_access_token,
    create_refresh_token,
    decode_token,
)

TEST_SECRET_KEY = "test-secret-key"


@pytest.fixture(autouse=True)
def mock_secret_key():
    with patch(
        "src.services.jwt_service.SECRET_KEY",
        TEST_SECRET_KEY,
    ):
        yield


def test_create_access_token():
    data = {
        "sub": "user-123",
        "email": "user@example.com",
    }

    token = create_access_token(data)

    assert isinstance(token, str)

    payload = jwt.decode(
        token,
        TEST_SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    assert payload["sub"] == "user-123"
    assert payload["email"] == "user@example.com"
    assert payload["type"] == "access"
    assert "exp" in payload


def test_create_access_token_has_correct_expiration():
    data = {"sub": "user-123"}

    before = datetime.now(UTC)

    token = create_access_token(data)

    after = datetime.now(UTC)

    payload = jwt.decode(
        token,
        TEST_SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    expected_min = int(before.timestamp() + ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    expected_max = int(after.timestamp() + ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    assert expected_min <= payload["exp"] <= expected_max


def test_create_refresh_token():
    data = {
        "sub": "user-123",
        "email": "user@example.com",
    }

    token = create_refresh_token(data)

    assert isinstance(token, str)

    payload = jwt.decode(
        token,
        TEST_SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    assert payload["sub"] == "user-123"
    assert payload["email"] == "user@example.com"
    assert payload["type"] == "refresh"
    assert "exp" in payload


def test_create_refresh_token_has_seven_days_expiration():
    data = {"sub": "user-123"}

    before = datetime.now(UTC)

    token = create_refresh_token(data)

    after = datetime.now(UTC)

    payload = jwt.decode(
        token,
        TEST_SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    expected_min = int(before.timestamp() + (7 * 24 * 60 * 60))

    expected_max = int(after.timestamp() + (7 * 24 * 60 * 60))

    assert expected_min <= payload["exp"] <= expected_max


def test_decode_token():
    data = {
        "sub": "user-123",
        "email": "user@example.com",
        "type": "access",
    }

    token = jwt.encode(
        data,
        TEST_SECRET_KEY,
        algorithm=ALGORITHM,
    )

    payload = decode_token(token)

    assert payload["sub"] == "user-123"
    assert payload["email"] == "user@example.com"
    assert payload["type"] == "access"


def test_decode_token_rejects_invalid_token():
    with pytest.raises(JWTError):
        decode_token("token-invalido")


def test_decode_token_rejects_token_with_wrong_secret():
    token = jwt.encode(
        {"sub": "user-123"},
        "wrong-secret",
        algorithm=ALGORITHM,
    )

    with pytest.raises(JWTError):
        decode_token(token)


def test_create_access_token_does_not_modify_original_data():
    data = {
        "sub": "user-123",
    }

    original_data = data.copy()

    create_access_token(data)

    assert data == original_data


def test_create_refresh_token_does_not_modify_original_data():
    data = {
        "sub": "user-123",
    }

    original_data = data.copy()

    create_refresh_token(data)

    assert data == original_data
