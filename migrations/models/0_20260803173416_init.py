from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "nome" VARCHAR(100) NOT NULL,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL,
    "criado_em" TIMESTAMPTZ NOT NULL,
    "atualizado_em" TIMESTAMPTZ NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztl2tP2zAUhv9KlE9M2hB03LRvoesE02gnml3ENFmniZtYOHaInZWO9b/PdpI6F1rRaY"
    "yB+NTmPe+Jjx/H8cmNm/AQU7H9SeDMfePcuAwSrP409JeOC2lqVS1ImFBjzJXDKDARMoNA"
    "KnEKVGAlhVgEGUkl4UypLKdUizxQRsIiK+WMXOUYSR5hGZtCvn1XMmEhvsaiukwv0ZRgGj"
    "bqJKEe2+hIzlOjnTL5zhj1aBMUcJonzJrTuYw5W7oJk1qNMMMZSKxvL7Ncl6+rK6dZzaio"
    "1FqKEms5IZ5CTmVtuhNkNReh4chH44GPkLsBoIAzDVeVKszsI13Cq97u3uHe0euDvSNlMW"
    "UulcNFMbQFUyQaPEPfXZg4SCgchrGFyrj67WDtx5DdzrXyt8iqkttkK47r0FaCZWufp38B"
    "N4FrRDGLZKwud3d21qD87J33T7zzLeV6oYfkagMU22JYhnpFTPO2fHEChG4CeJnwdwg/7M"
    "Pb4Nvb378DX+VaydfEmnxTEGLGsxDFIOJNOHcSn+ATfS/EVVkQcoSTLu23CpQkCb6deCOx"
    "RTssM7erP4+RfYYhHDE6L3fZGvT+6dlg7HtnH/VwiRBX1ODz/IGO9Iw6b6lbB61VWt7E+X"
    "Lqnzj60rkYDQcGLxcyysyI1udfuLomyCVHjM8QhLUXQqVW1BprDjIHSn7+2bp3kp/X/n9Z"
    "+4pRbfFN9boHm17WGgYtTCC4nIF6Y3YivMdXebuhpJe0FWAQmTXTcHWZZUvq4YwEsXtLs1"
    "pG1rarYD3P/epT6Vd/qE8QXdIGJ30t5fmMv9sZrzfVBoRL+xOkey/fBGpEiYut3ST8fjwa"
    "ruidbEr79CSBdH45lIjOu+IR0F4DV8NoHJEV060z72sbd//D6Lh99ukbHCv0D3qYLX4D9n"
    "GOGw=="
)
