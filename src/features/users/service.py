from .repository import UserRepository
from .schema import UserCreate, UserResponse, UserUpdate


class UserService:
	def __init__(self, repo: UserRepository):
		self.repo = repo

	async def create_user(self, user_data: UserCreate) -> UserResponse:
		# Business logic here
		new_user = await self.repo.create(user_data)

		return UserResponse.model_validate(new_user)

	async def get_user(self, user_id: int) -> UserResponse:
		user = await self.repo.get_user_by_id(user_id)

		return user

	async def get_all_users(self) -> list[UserResponse]:
		users = await self.repo.get_users()

		return users

	async def update_user(self, user: UserUpdate) -> UserResponse:
		db_user = await self.repo.update(user)

		return db_user

	async def delete_user(self, user_id: int) -> UserResponse:
		deleted_user = await self.repo.delete(user_id)

		return deleted_user
