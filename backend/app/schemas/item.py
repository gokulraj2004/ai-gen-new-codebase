import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    tags: list[str] | None = None


class ItemUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    tags: list[str] | None = None


class TagResponse(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        from_attributes = True


class ItemResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    user_id: uuid.UUID
    tags: list[TagResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaginatedItemResponse(BaseModel):
    items: list[ItemResponse]
    total: int
    page: int
    page_size: int
    total_pages: int