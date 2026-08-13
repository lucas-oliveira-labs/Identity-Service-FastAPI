from tortoise import fields
from tortoise.models import Model

from src.models.rule import Rule


class Role(Model):
    id = fields.IntField(primary_key=True)

    name = fields.CharField(
        max_length=100,
        unique=True,
    )

    description = fields.TextField(
        null=True,
    )

    rules: fields.ManyToManyRelation[Rule] = fields.ManyToManyField(
        "models.Rule",
        related_name="roles",
    )

    criado_em = fields.DatetimeField(
        auto_now_add=True,
    )

    atualizado_em = fields.DatetimeField(
        auto_now=True,
    )

    class Meta:
        table = "roles"
