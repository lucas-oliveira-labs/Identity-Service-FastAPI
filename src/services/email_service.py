from email.message import EmailMessage
import os

import aiosmtplib


class EmailService:
    async def send_password_reset_email(
        self,
        email: str,
        reset_token: str,
    ):
        reset_url = f"http://localhost:3000/reset-password?token={reset_token}"

        message = EmailMessage()

        message["From"] = os.getenv("SMTP_FROM")
        message["To"] - email
        message["Subject"] = "Redefinicao de senha"

        message.set_content(
            f"""
                Olá!

                Recebemos uma solicitaçao para redefinir sua senha.

                Acesse o link abaixo para criar uma nova senha:

                {reset_url}

                Este link é válido por 30 minutos.

                Se voce nao solicitou a redefinicao de senha, ignore este email.
        """
        )

        await aiosmtplib.send(
            message,
            hostname=os.getenv("SMTP_HOST"),
            port=int(os.getenv("SMTP_PORT", "1025")),
            username=os.getenv("SMTP_USERNAME"),
            password=os.getenv("SMTP_PASSWORD"),
        )
