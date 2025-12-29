from .repository import UserRepository
from .schema import UserCreate, UserResponse


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        # Business logic here

        new_user = await self.repo.create(user_data)

        return UserResponse.model_validate(new_user)

    async def get_all_users(self) -> list[UserResponse]:
        users = await self.repo.get_users()

        return users
