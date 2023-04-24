from fastapi import FastAPI
from app.api.v1.router import router as v1_router
from app.config.settings import settings

app = FastAPI(
    title=settings.title,
    description=settings.description,
    version=settings.version,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(v1_router)
