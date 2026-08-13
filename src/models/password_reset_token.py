from tortoise import fields, models


class PasswordResetToken(models.Model):
    id = fields.IntField(primary_key=True)

    user = fields.ForeignKeyField(
        "models.User",
        related_name="password_reset_tokens",
        on_delete=fields.CASCADE,
    )

    token_hash = fields.CharField(max_length=128, unique=True)

    expires_at = fields.DatetimeField()

    used_at = fields.DatetimeField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
