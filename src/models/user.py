from tortoise import fields
from tortoise.models import Model

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .role import Role


class User(Model):
    id = fields.IntField(primary_key=True)

    nome = fields.CharField(max_length=100)
    email = fields.CharField(max_length=255, unique=True)
    password_hash = fields.CharField(max_length=255)

    criado_em = fields.DatetimeField(auto_now_add=True)
    atualizado_em = fields.DatetimeField(auto_now=True)

    roles: fields.ManyToManyRelation["Role"] = fields.ManyToManyField(
        "models.Role",
        releted_name="users",
    )

    class Meta:
        table = "users"
