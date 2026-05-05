from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.tag import TagCreate, TagResponse
from app.models.user import User
from app.core.deps import get_current_user
from app.services.tag_service import TagService

router = APIRouter()


@router.get("", response_model=List[TagResponse])
async def list_tags(
    db: AsyncSession = Depends(get_db),
):
    tag_service = TagService(db)
    tags = await tag_service.get_all()
    return tags


@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    tag_service = TagService(db)
    existing = await tag_service.get_by_name(tag_data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag already exists",
        )
    tag = await tag_service.create(tag_data)
    await db.commit()
    return tag