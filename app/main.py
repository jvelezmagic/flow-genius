from fastapi import FastAPI
from dotenv import load_dotenv

from app.api.v1.routes.router import router as v1_router
from app.config.settings import settings

load_dotenv()

app = FastAPI(
    title=settings.title,
    description=settings.description,
    version=settings.version,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(v1_router)
