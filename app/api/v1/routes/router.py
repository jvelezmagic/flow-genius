from fastapi import APIRouter
from app.api.v1.routes import reservations
from app.api.v1.routes import agent_routes
from app.api.v1.routes import conversation

router = APIRouter(prefix="/v1", tags=["v1"])

router.include_router(reservations.router)
router.include_router(agent_routes.router)
router.include_router(conversation.router)
