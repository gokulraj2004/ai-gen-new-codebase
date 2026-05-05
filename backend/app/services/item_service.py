import uuid
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.item import Item
from app.models.tag import Tag
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, item_id: uuid.UUID) -> Optional[Item]:
        result = await self.db.execute(
            select(Item).options(selectinload(Item.tags)).where(Item.id == item_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Item]:
        result = await self.db.execute(
            select(Item)
            .options(selectinload(Item.tags))
            .offset(skip)
            .limit(limit)
            .order_by(Item.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_owner(self, owner_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Item]:
        result = await self.db.execute(
            select(Item)
            .options(selectinload(Item.tags))
            .where(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .order_by(Item.created_at.desc())
        )
        return list(result.scalars().all())

    async def _get_or_create_tags(self, tag_names: List[str]) -> List[Tag]:
        tags = []
        for name in tag_names:
            name = name.strip()
            if not name:
                continue
            result = await self.db.execute(select(Tag).where(Tag.name == name))
            tag = result.scalar_one_or_none()
            if not tag:
                tag = Tag(name=name)
                self.db.add(tag)
                await self.db.flush()
            tags.append(tag)
        return tags

    async def create(self, item_data: ItemCreate, owner_id: uuid.UUID) -> Item:
        tags = await self._get_or_create_tags(item_data.tag_names)
        item = Item(
            title=item_data.title,
            description=item_data.description,
            owner_id=owner_id,
            tags=tags,
        )
        self.db.add(item)
        await self.db.flush()
        await self.db.refresh(item)
        # Ensure tags are loaded
        result = await self.db.execute(
            select(Item).options(selectinload(Item.tags)).where(Item.id == item.id)
        )
        return result.scalar_one()

    async def update(self, item: Item, item_data: ItemUpdate) -> Item:
        update_data = item_data.model_dump(exclude_unset=True)
        tag_names = update_data.pop("tag_names", None)
        for field, value in update_data.items():
            setattr(item, field, value)
        if tag_names is not None:
            item.tags = await self._get_or_create_tags(tag_names)
        await self.db.flush()
        await self.db.refresh(item)
        # Ensure tags are loaded
        result = await self.db.execute(
            select(Item).options(selectinload(Item.tags)).where(Item.id == item.id)
        )
        return result.scalar_one()

    async def delete(self, item: Item) -> None:
        await self.db.delete(item)
        await self.db.flush()