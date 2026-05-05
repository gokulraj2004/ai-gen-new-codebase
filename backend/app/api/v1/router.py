from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, items, tags

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])