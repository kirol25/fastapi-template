from fastapi import APIRouter
from fastapi.security import HTTPBearer

from app.api.health.router import router as health_router
from app.api.users.router import router as users_router

router = APIRouter()
security = HTTPBearer()

router.include_router(health_router)
router.include_router(users_router)
