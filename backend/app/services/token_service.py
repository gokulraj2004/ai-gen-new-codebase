import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.token_blocklist import TokenBlocklist


class TokenService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def blocklist_token(
        self,
        jti: str,
        token_type: str,
        user_id: uuid.UUID,
        expires_at: datetime,
    ) -> TokenBlocklist:
        entry = TokenBlocklist(
            jti=jti,
            token_type=token_type,
            user_id=user_id,
            expires_at=expires_at,
        )
        self.db.add(entry)
        await self.db.flush()
        return entry

    async def is_token_blocklisted(self, jti: str) -> bool:
        result = await self.db.execute(
            select(TokenBlocklist).where(TokenBlocklist.jti == jti)
        )
        return result.scalar_one_or_none() is not None