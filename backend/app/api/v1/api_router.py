from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, health

api_router = APIRouter()

# Register endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
