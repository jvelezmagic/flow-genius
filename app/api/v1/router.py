from fastapi import APIRouter
from app.api.v1 import reservations

router = APIRouter(prefix="/v1", tags=["v1"])

router.include_router(reservations.router)
