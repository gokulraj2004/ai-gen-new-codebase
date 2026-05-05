from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.items import router as items_router
from app.api.tags import router as tags_router
from app.api.users import router as users_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(items_router, prefix="/items", tags=["Items"])
router.include_router(tags_router, prefix="/tags", tags=["Tags"])
router.include_router(users_router, prefix="/users", tags=["Users"])