from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.core.security import get_current_user
from app.models import User
from app.models.tag import Tag

router = APIRouter()


class TagCreate(BaseModel):
    name: str


class TagResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


@router.get("/", response_model=list[TagResponse])
async def list_tags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).order_by(Tag.name))
    tags = result.scalars().all()
    return tags


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Check if tag already exists
    result = await db.execute(select(Tag).where(Tag.name == tag_data.name))
    existing_tag = result.scalar_one_or_none()
    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag already exists",
        )

    tag = Tag(name=tag_data.name)
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag