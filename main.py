from fastapi import FastAPI

app = FastAPI(title="Identity Service", version="1.0.0")


@app.get("/")
def root():
    return {"message": "Identity Service running"}
