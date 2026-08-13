from fastapi import APIRouter
from app.api.v1.admin.admin_auth import router as admin_auth_router
from app.api.v1.health import router as health_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router)
api_v1_router.include_router(admin_auth_router)

__all__ = ["api_v1_router"]