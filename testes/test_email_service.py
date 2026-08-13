from email.message import EmailMessage
from unittest.mock import AsyncMock, patch

import pytest

from src.services.email_service import EmailService


@pytest.fixture
def email_service():
    return EmailService()


@pytest.mark.asyncio
async def test_send_password_reset_email():
    service = EmailService()

    with patch(
        "src.services.email_service.aiosmtplib.send",
        new_callable=AsyncMock,
    ) as mock_send:
        await service.send_password_reset_email(
            email="user@example.com",
            reset_token="abc123",
        )

    mock_send.assert_awaited_once()

    message = mock_send.await_args.args[0]

    assert isinstance(message, EmailMessage)
    assert message["From"] == "no-reply@identity.local"
    assert message["To"] == "user@example.com"
    assert message["Subject"] == "Redefinicao de senha"

    body = message.get_content()

    assert "Olá!" in body
    assert "abc123" in body
    assert "http://localhost:3000/reset-password?token=abc123" in body
    assert "30 minutos" in body


@pytest.mark.asyncio
async def test_send_password_reset_email_uses_smtp_environment_variables():
    service = EmailService()

    smtp_port = 587

    with (
        patch.dict(
            "os.environ",
            {
                "SMTP_FROM": "noreply@example.com",
                "SMTP_HOST": "smtp.example.com",
                "SMTP_PORT": "587",
            },
            clear=False,
        ),
        patch(
            "src.services.email_service.aiosmtplib.send",
            new_callable=AsyncMock,
        ) as mock_send,
    ):
        await service.send_password_reset_email(
            email="user@example.com",
            reset_token="token-456",
        )

    mock_send.assert_awaited_once()

    kwargs = mock_send.await_args.kwargs

    assert kwargs["hostname"] == "smtp.example.com"
    assert kwargs["port"] == smtp_port

    message = mock_send.await_args.args[0]

    assert message["From"] == "noreply@example.com"
    assert message["To"] == "user@example.com"


@pytest.mark.asyncio
async def test_send_password_reset_email_uses_default_smtp_configuration():
    service = EmailService()

    mailpit_port = 1025

    with (
        patch.dict(
            "os.environ",
            {},
            clear=True,
        ),
        patch(
            "src.services.email_service.aiosmtplib.send",
            new_callable=AsyncMock,
        ) as mock_send,
    ):
        await service.send_password_reset_email(
            email="user@example.com",
            reset_token="token-default",
        )

    mock_send.assert_awaited_once()

    kwargs = mock_send.await_args.kwargs

    assert kwargs["hostname"] == "mailpit"
    assert kwargs["port"] == mailpit_port

    message = mock_send.await_args.args[0]

    assert message["From"] == "no-reply@identity.local"
