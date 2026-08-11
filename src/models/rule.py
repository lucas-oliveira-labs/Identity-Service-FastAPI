from tortoise import fields
from tortoise.models import Model


class Rule(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(
        max_length=100,
        unique=True,
    )

    description = fields.TextField(
        null=True,
    )

    resource = fields.CharField(
        max_length=100,
    )

    action = fields.CharField(
        max_length=50,
    )

    criado_em = fields.DatetimeField(
        auto_now_add=True,
    )

    atualizado_em = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "rules"
        unique_together = (("resource", "action"),)
