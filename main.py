from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.database import TORTOISE_ORM
from src.routers.auth_router import router as auth_router
from src.routers.private_router import router as private_router
from src.routers.public_router import router as public_router

app = FastAPI(
    title="Identity Service", 
    summary="API de autenticação e gerenciamento de identidade.",
    description='''
    # Identity Service

    Serviço responsável por autenticação, autorização e
    gerenciamento de identidade.

    ## Recursos

    - Autenticação de usuários
    - Gerenciamento de tokens
    - Recursos públicos
    - Recursos protegidos
''',
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Endpoints relacionados à autenticação e emissão de tokens."
        },
        {
            "name": "Public",
            "description": "Endpoints que podem ser acessados sem  autenticação."
        },
        {
            "name": "Private",
            "description": "Enpoints que exigem  autenticação"
        }
    ]
)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)
app.include_router(public_router)
app.include_router(private_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "Welcome to the Identity Service!"}
