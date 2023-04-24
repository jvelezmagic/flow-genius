from fastapi import FastAPI
from app.api.v1.router import router as v1_router

app = FastAPI(
    title="Flow Genius API",
    description="API for Flow Genius",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(v1_router)
