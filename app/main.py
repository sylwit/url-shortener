from fastapi import FastAPI

from app.routers import url

app = FastAPI()

app.include_router(url.router)


@app.get("/")
def index():
    return {"message": "Hello URL shortner!"}
