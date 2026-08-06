from tortoise import fields, models


class RefreshToken(models.Model):
    id = fields.IntField(pk=True)

    token = fields.CharField(max_length=512, unique=True)

    user = fields.ForeignKeyField(
        "models.User", related_name="refresh_tokens", on_delete=fields.CASCADE
    )

    expires_at = fields.DatetimeField()

    created_at = fields.DatetimeField(auto_now_add=True)

    revoked = fields.BooleanField(default=False)

    class Meta:
        table = "refresh_tokens"
