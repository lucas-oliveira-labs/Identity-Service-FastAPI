from fastapi import FastAPI
from src.database import TORTOISE_ORM
from src.routers.public_router import router as public_router
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(title="Identity Service", version="1.0.0")

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
app.include_router(public_router)


@app.get("/")
def root():
    return {"message": "Welcome to the Identity Service!"}
