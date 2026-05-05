import uuid
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User
from app.models.token_blocklist import TokenBlocklist
from app.schemas import UserCreate, UserLogin, Token
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.config import settings


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, user_data: UserCreate) -> User:
        # Check if user already exists
        result = await self.db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def login(self, credentials: UserLogin) -> Token | None:
        result = await self.db.execute(
            select(User).where(User.email == credentials.email)
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(credentials.password, user.hashed_password):
            return None

        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    async def refresh(self, refresh_token: str) -> Token | None:
        payload = decode_token(refresh_token)
        if payload is None:
            return None

        if payload.get("type") != "refresh":
            return None

        jti = payload.get("jti")
        if jti:
            # Check if token is blocklisted
            result = await self.db.execute(
                select(TokenBlocklist).where(TokenBlocklist.jti == jti)
            )
            if result.scalar_one_or_none():
                return None

        user_id = payload.get("sub")
        if not user_id:
            return None

        # Verify user still exists and is active
        result = await self.db.execute(
            select(User).where(User.id == uuid.UUID(user_id))
        )
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            return None

        # Blocklist the old refresh token
        if jti:
            exp = payload.get("exp")
            expires_at = datetime.utcfromtimestamp(exp) if exp else datetime.utcnow() + timedelta(days=7)
            blocked = TokenBlocklist(
                jti=jti,
                token_type="refresh",
                user_id=user.id,
                expires_at=expires_at,
            )
            self.db.add(blocked)
            await self.db.commit()

        # Issue new tokens
        new_access_token = create_access_token(subject=str(user.id))
        new_refresh_token = create_refresh_token(subject=str(user.id))

        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )

    async def logout(self, refresh_token: str) -> None:
        payload = decode_token(refresh_token)
        if payload and payload.get("jti"):
            jti = payload["jti"]
            user_id = payload.get("sub")
            exp = payload.get("exp")
            expires_at = datetime.utcfromtimestamp(exp) if exp else datetime.utcnow() + timedelta(days=7)

            # Check if already blocklisted
            result = await self.db.execute(
                select(TokenBlocklist).where(TokenBlocklist.jti == jti)
            )
            if not result.scalar_one_or_none():
                blocked = TokenBlocklist(
                    jti=jti,
                    token_type="refresh",
                    user_id=uuid.UUID(user_id) if user_id else None,
                    expires_at=expires_at,
                )
                self.db.add(blocked)
                await self.db.commit()