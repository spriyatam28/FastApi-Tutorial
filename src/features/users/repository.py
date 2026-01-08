from typing import Optional

from pydantic import EmailStr
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .exception import UserNotFoundException, EmailNotFoundException, DuplicateEmailException
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
		result = await self.db.execute(select(User).where(User.email == user.email))

		# If email already exists in db, throw an exception
		if result.scalar_one_or_none():
			raise DuplicateEmailException()

		new_user = User(**user.model_dump())

		try:
			self.db.add(new_user)
			await self.db.commit()
			await self.db.refresh(new_user)

			return new_user
		except IntegrityError as err:
			await self.db.rollback()
			raise DuplicateEmailException() from err

	async def update(self, user: UserUpdate) -> Optional[User]:
		"""
		Updates user email and/or name, identifies user by their id
		:param user: User details that need to be updated
		:return: Returns user details after successfully updating them
		"""
		db_user = await self.get_user_by_id(user.id)

		if not db_user:
			raise UserNotFoundException()

		# Check if the new email already exists in db
		if user.email and user.email != db_user.email:
			result = await self.db.execute(select(User).where(User.email == user.email))
			existing_email = result.scalar_one_or_none()

			if existing_email:
				raise DuplicateEmailException()

		# If email does not exist, apply the update
		for field, value in user.model_dump(exclude_unset=True).items():
			setattr(db_user, field, value)

		try:
			await self.db.commit()
			await self.db.refresh(db_user)

			return db_user
		except IntegrityError as err:
			await self.db.rollback()
			raise DuplicateEmailException() from err

	async def get_user_by_email(self, email: EmailStr) -> User | None:
		"""
		Gets user details by their email if exists
		:param email: email of the user
		:return: Details of the user
		"""
		result = await self.db.execute(select(User).where(User.email == email))
		user = result.scalar_one_or_none()

		if not user:
			raise EmailNotFoundException()

		return user

	async def get_user_by_id(self, user_id: int) -> User | None:
		"""
		Gets a user details if exists
		:param user_id: user id
		:return: user details
		"""
		result = await self.db.execute(select(User).where(User.id == user_id))
		user = result.scalar_one_or_none()

		if not user:
			raise UserNotFoundException()

		return user

	async def get_users(self) -> list[User]:
		"""
		Returns a list of all users' details
		:return: All users' details
		"""
		users = await self.db.execute(select(User).limit(10).offset(0))

		return list(users.scalars().all())

	async def delete(self, user_id: int) -> User | None:
		"""
		Delete a user by their id
		:param user_id:
		:return:
		"""
		# TODO: Use Alembic for migration
		result = await self.db.execute(delete(User).where(User.id == user_id).returning(User))
		user = result.scalar_one_or_none()

		if not user:
			raise UserNotFoundException()

		try:
			await self.db.commit()

			return user
		except IntegrityError as err:
			await self.db.rollback()
			raise UserNotFoundException() from err
