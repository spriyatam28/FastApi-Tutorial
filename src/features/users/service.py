from .exception import DuplicateEmailException, UserNotFoundException
from .model import User
from .repository import UserRepository
from .schema import UserCreate, UserUpdate


class UserService:
	def __init__(self, repo: UserRepository):
		self.repo = repo

	async def create_user(self, user_data: UserCreate) -> User:
		# Business logic here
		email_exists = await self.repo.get_user_by_email(user_data.email)

		if email_exists:
			raise DuplicateEmailException()

		new_user = await self.repo.create(user_data)

		return new_user

	async def get_user(self, user_id: int) -> User:
		user = await self.repo.get_user_by_id(user_id)

		if not user:
			raise UserNotFoundException()

		return user

	async def get_all_users(self) -> list[User]:
		users = await self.repo.get_users()

		return users

	async def update_user(self, user: UserUpdate) -> User:
		email_exists = await self.repo.get_user_by_email(user.email)
		db_user = await self.repo.get_user_by_id(user.id)

		if email_exists:
			raise DuplicateEmailException()

		if not db_user:
			raise UserNotFoundException()

		db_user = await self.repo.update(user)

		return db_user

	async def delete_user(self, user_id: int) -> User:
		deleted_user = await self.repo.delete(user_id)

		if not deleted_user:
			raise UserNotFoundException()

		return deleted_user
