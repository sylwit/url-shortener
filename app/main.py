from fastapi import FastAPI

from app.models.url import UrlTable
from app.routers import url

app = FastAPI()

app.include_router(url.router)


@app.get("/", include_in_schema=False)
def index():
    return {"message": "Hello URL shortner!"}


@app.get("/db/init", include_in_schema=False)
def db():
    if UrlTable.exists():
        UrlTable.delete_table()

    UrlTable.create_table(wait=True)
    return {"message": "DB initialize"}
