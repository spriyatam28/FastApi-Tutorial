from typing import Any, Sequence

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .model import User
from .schema import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: UserCreate) -> User:
        new_user = User(**user.model_dump())

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user

    async def update(self, user: UserUpdate) -> UserUpdate:
        # TODO: Update the user details

        return user

    async def get_by_email(self, email: EmailStr) -> User | None:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()

    async def get_users(self) -> list[User]:
        users = await self.db.execute(select(User))

        return list(users.scalars().unique().all())
