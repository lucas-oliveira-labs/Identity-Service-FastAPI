from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "refresh_tokens" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" VARCHAR(512) NOT NULL UNIQUE,
    "expires_at" TIMESTAMPTZ NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "revoked" BOOL NOT NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "refresh_tokens";"""


MODELS_STATE = (
    "eJztmV1v2jAUhv8KyhWTtqqwfml3gVKVtcAE6TZ1miyTmMQisdPEKWUd/322k5BPGFSlWx"
    "BXhdfnxCfPseOX9FlxqIFs/+jOR57yqfasEOgg/iGjv68p0HUTVQgMjm0ZGPAIqcCxzzyo"
    "My5OoO0jLhnI1z3sMkwJV0lg20KkOg/ExEykgOCHAAFGTcQsWciPn1zGxEBPyI+/ulMwwc"
    "g2MnViQ8wtdcDmrtS6hF3JQDHbGOjUDhySBLtzZlGyjMaECdVEBHmQIXF55gWifFFddJvx"
    "HYWVJiFhiakcA01gYLPU7Y5BoikA9AcaGHU0AJQtAOmUCLi8VF/evSlK+NBsnJyfXHw8O7"
    "ngIbLMpXK+CKdOwISJEk9fUxZyHDIYRkjGCVRC+d8C1rYFvXKucXyOLC85TzbmuA5tLCRs"
    "k/X0FnAd+ARsRExm8a+N4+M1KL+qw/a1OqzzqHdiSso3QLgt+tFQMxwTvBO+yIHY3gbwMu"
    "F1CP/bxZvh2zw93YAvj1rJV45l+brQ92fUM4AFfWsbzoXEPVzROyHOy4IGBcgp0r7koBh2"
    "UDnxTGKOthFlHsUfqsjeQ9AYEHse7bI16LVurzPS1N4XMZ3j+w+2xKdqHTHSlOo8p9bPcl"
    "1aXqT2ratd18TX2v2g35F4qc9MT86YxGn3iqgJBowCQmcAGqkHQqzG1DI9hyyANv71sr4X"
    "kg+9/196HzNKNV9WLzzYZJoyDEIYQ306g/yJmRlJFomHJnxWi3u7KSJ+cZW0ovyrmyGyoS"
    "RcXAyRGR2G19LEpSq4HBbxHojVNFjapKvIFoecppNXIIGmvCUxt5ipjFmJwc8zXW30i508"
    "OP69cfws7v+mTmmZsHeO9LTR3MAf8aiV/kiO5Rz/k4v57gGQbXtQZjP38JSs7qlYtEQ6P/"
    "E5+Be0OZu5h22uqBnaxAh76JE/DUuOpRalNoKkvOOprFy7xzxtVx1eKm+7k1uDwW2mm62u"
    "lnt83vVanWG9IdvIgzBD6aMroS1eOIKtTEAq4+9OoApb6RXMQMHMZwEX6V5RD2GT3KC5hN"
    "zlFUGil732y706rhjcVS6dyx6cLf1oelHxe+d3jMIF21ZHbfWyoyxW/zrapd9XkYd1Sylx"
    "+tHIWo8Pk5iDt6/Sdl7n7R+R50e/qzd196mUwxvQzd6Aik21BeEofA/p7uQ/JnxGhkiJq/"
    "48GvRXOOokJW+nsc5qv2s29qt4+q+BK2BkXFbMtN5Tv+dxt28HrbwZFhdolbmDtzzMFn8A"
    "qszFeQ=="
)
