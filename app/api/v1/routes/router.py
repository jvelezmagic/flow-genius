from fastapi import APIRouter
from app.api.v1.routes import reservations
from app.api.v1.routes import agent_routes

router = APIRouter(prefix="/v1", tags=["v1"])

router.include_router(reservations.router)
router.include_router(agent_routes.router)
