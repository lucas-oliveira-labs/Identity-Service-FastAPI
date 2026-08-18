import os

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": os.getenv("DATABASE_HOST", "postgres"),
                "port": int(os.getenv("DATABASE_PORT", "5432")),
                "user": os.getenv("DATABASE_USER", "postgres"),
                "password": os.getenv("DATABASE_PASSWORD", "postgres"),
                "database": os.getenv("DATABASE_NAME", "identity_db"),
            },
        }
    },
    "apps": {
        "models": {
            "models": [
                "src.models.user",
                "src.models.refresh_token",
                "src.models.password_reset_token",
                "src.models.role",
                "src.models.rule",
                "aerich.models",
            ],
            "default_connection": "default",
        }
    },
}