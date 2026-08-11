from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "roles" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "description" TEXT,
    "criado_em" TIMESTAMPTZ NOT NULL,
    "atualizado_em" TIMESTAMPTZ NOT NULL
);
        CREATE TABLE IF NOT EXISTS "rules" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "description" TEXT,
    "resource" VARCHAR(100) NOT NULL,
    "action" VARCHAR(50) NOT NULL,
    "criado_em" TIMESTAMPTZ NOT NULL,
    "atualizado_em" TIMESTAMPTZ NOT NULL,
    CONSTRAINT "uid_rules_resourc_60e92d" UNIQUE ("resource", "action")
);
        CREATE TABLE "roles_rules" (
    "roles_id" INT NOT NULL REFERENCES "roles" ("id") ON DELETE CASCADE,
    "rule_id" INT NOT NULL REFERENCES "rules" ("id") ON DELETE CASCADE
);
        CREATE TABLE "users_roles" (
    "users_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "role_id" INT NOT NULL REFERENCES "roles" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "users_roles";
        DROP TABLE IF EXISTS "roles_rules";
        DROP TABLE IF EXISTS "users_roles";
        DROP TABLE IF EXISTS "roles";
        DROP TABLE IF EXISTS "rules";"""


MODELS_STATE = (
    "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"
)
