from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)

    nome = fields.CharField(max_length=100)
    email = fields.CharField(max_length=255, unique=True)
    password_hash = fields.CharField(max_length=255)

    criado_em = fields.DatetimeField(auto_now_add=True)
    atualizado_em = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"
