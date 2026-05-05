import uuid
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tag import Tag
from app.schemas.tag import TagCreate


class TagService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, tag_id: uuid.UUID) -> Optional[Tag]:
        result = await self.db.execute(select(Tag).where(Tag.id == tag_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Tag]:
        result = await self.db.execute(select(Tag).where(Tag.name == name))
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Tag]:
        result = await self.db.execute(select(Tag).order_by(Tag.name))
        return list(result.scalars().all())

    async def create(self, tag_data: TagCreate) -> Tag:
        tag = Tag(name=tag_data.name)
        self.db.add(tag)
        await self.db.flush()
        await self.db.refresh(tag)
        return tag