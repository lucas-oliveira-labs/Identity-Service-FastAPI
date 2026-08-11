TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": "postgres",
                "port": 5432,
                "user": "postgres",
                "password": "postgres",
                "database": "identity_db",
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
