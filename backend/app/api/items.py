import uuid
import math
import enum
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.schemas import ItemCreate, ItemUpdate, ItemResponse, PaginatedItemResponse
from app.core.security import get_current_user
from app.models import User, Item
from app.models.tag import Tag, ItemTag

router = APIRouter()


class SortBy(str, enum.Enum):
    title_asc = "title_asc"
    title_desc = "title_desc"
    created_at_asc = "created_at_asc"
    created_at_desc = "created_at_desc"
    updated_at_asc = "updated_at_asc"
    updated_at_desc = "updated_at_desc"


@router.get("/", response_model=PaginatedItemResponse)
async def list_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    tags: Optional[List[str]] = Query(None),
    sort_by: Optional[SortBy] = Query(SortBy.created_at_desc),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Item).options(selectinload(Item.tags).selectinload(ItemTag.tag))

    # Search filter
    if search:
        query = query.where(
            Item.title.ilike(f"%{search}%") | Item.description.ilike(f"%{search}%")
        )

    # Tag filter
    if tags:
        for tag_name in tags:
            tag_subquery = (
                select(ItemTag.item_id)
                .join(Tag)
                .where(Tag.name == tag_name)
            )
            query = query.where(Item.id.in_(tag_subquery))

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Sorting
    if sort_by:
        sort_value = sort_by.value
        if sort_value == "title_asc":
            query = query.order_by(Item.title.asc())
        elif sort_value == "title_desc":
            query = query.order_by(Item.title.desc())
        elif sort_value == "created_at_asc":
            query = query.order_by(Item.created_at.asc())
        elif sort_value == "created_at_desc":
            query = query.order_by(Item.created_at.desc())
        elif sort_value == "updated_at_asc":
            query = query.order_by(Item.updated_at.asc())
        elif sort_value == "updated_at_desc":
            query = query.order_by(Item.updated_at.desc())
    else:
        query = query.order_by(Item.created_at.desc())

    # Pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    items = result.scalars().unique().all()

    # Transform items to include tags properly
    item_responses = []
    for item in items:
        item_tags = [{"id": str(it.tag.id), "name": it.tag.name} for it in item.tags] if item.tags else []
        item_responses.append(
            ItemResponse(
                id=item.id,
                title=item.title,
                description=item.description,
                user_id=item.user_id,
                tags=item_tags,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
        )

    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return PaginatedItemResponse(
        items=item_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Item)
        .options(selectinload(Item.tags).selectinload(ItemTag.tag))
        .where(Item.id == item_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    item_tags = [{"id": str(it.tag.id), "name": it.tag.name} for it in item.tags] if item.tags else []
    return ItemResponse(
        id=item.id,
        title=item.title,
        description=item.description,
        user_id=item.user_id,
        tags=item_tags,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_data: ItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    item = Item(
        title=item_data.title,
        description=item_data.description,
        user_id=current_user.id,
    )
    db.add(item)
    await db.flush()

    # Handle tags
    if item_data.tags:
        for tag_name in item_data.tags:
            # Find or create tag
            result = await db.execute(select(Tag).where(Tag.name == tag_name))
            tag = result.scalar_one_or_none()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                await db.flush()

            item_tag = ItemTag(item_id=item.id, tag_id=tag.id)
            db.add(item_tag)

    await db.commit()
    await db.refresh(item)

    # Reload with tags
    result = await db.execute(
        select(Item)
        .options(selectinload(Item.tags).selectinload(ItemTag.tag))
        .where(Item.id == item.id)
    )
    item = result.scalar_one()

    item_tags = [{"id": str(it.tag.id), "name": it.tag.name} for it in item.tags] if item.tags else []
    return ItemResponse(
        id=item.id,
        title=item.title,
        description=item.description,
        user_id=item.user_id,
        tags=item_tags,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: uuid.UUID,
    item_data: ItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Item)
        .options(selectinload(Item.tags).selectinload(ItemTag.tag))
        .where(Item.id == item_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if item.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    if item_data.title is not None:
        item.title = item_data.title
    if item_data.description is not None:
        item.description = item_data.description

    # Handle tags update
    if item_data.tags is not None:
        # Remove existing tags
        for item_tag in item.tags:
            await db.delete(item_tag)
        await db.flush()

        # Add new tags
        for tag_name in item_data.tags:
            result = await db.execute(select(Tag).where(Tag.name == tag_name))
            tag = result.scalar_one_or_none()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                await db.flush()

            item_tag = ItemTag(item_id=item.id, tag_id=tag.id)
            db.add(item_tag)

    await db.commit()
    await db.refresh(item)

    # Reload with tags
    result = await db.execute(
        select(Item)
        .options(selectinload(Item.tags).selectinload(ItemTag.tag))
        .where(Item.id == item.id)
    )
    item = result.scalar_one()

    item_tags = [{"id": str(it.tag.id), "name": it.tag.name} for it in item.tags] if item.tags else []
    return ItemResponse(
        id=item.id,
        title=item.title,
        description=item.description,
        user_id=item.user_id,
        tags=item_tags,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if item.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    await db.delete(item)
    await db.commit()