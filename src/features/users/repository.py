from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from .model import User
from .schema import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: UserCreate) -> User:
        """
        Creates a new user, if email doesn't exist
        :param user: Takes the user details
        :return: New user details
        """
        new_user = User(**user.model_dump())

        if new_user.email:
            result = await self.db.execute(select(User).where(User.email==user.email))

            if result.scalar_one_or_none():
                raise HTTPException(
                    status_code=400,
                    detail="Email already in use. Try with a different one"
                )

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user

    async def update(self, user: UserUpdate) -> User | None:
        """
        Updates user email and/or name, identifies user by their id
        :param user: User details that need to be updated
        :return: Returns user details after successfully updating them
        """
        db_user = await self.get_user_by_id(user.id)

        if not db_user:
            return None

        # Check if the new email already exists in db
        if user.email and user.email != db_user.email:
            result = await self.db.execute(select(User).where(User.email == user.email))
            existing_user = result.scalar_one_or_none()

            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="Email already in use. Try with a different one"
                )

        # If email does not exist, apply the update
        for field, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)

        await self.db.commit()
        await self.db.refresh(db_user)

        return db_user

    async def get_user_by_email(self, email: EmailStr) -> User | None:
        """
        Gets user details by their email if exists
        :param email: email of the user
        :return: Details of the user
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Gets a user details if exists
        :param user_id: user id
        :return: user details
        """
        db_user = await self.db.execute(select(User).where(User.id == user_id))

        return db_user.scalar_one_or_none()

    async def get_users(self) -> list[User]:
        """
        Returns a list of all users' details
        :return: All users' details
        """
        users = await self.db.execute(select(User))

        return list(users.scalars().unique().all())
