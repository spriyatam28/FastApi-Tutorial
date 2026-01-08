from fastapi import APIRouter, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.endpoints import DB_SESSION
from src.core.response import BaseResponse
from src.features.users.exception import DuplicateEmailException, UserNotFoundException
from src.features.users.repository import UserRepository
from src.features.users.schema import UserResponse, UserCreate, UserUpdate
from src.features.users.service import UserService

router = APIRouter()


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = DB_SESSION):
	"""Create a new user"""
	repo = UserRepository(db)
	service = UserService(repo)

	try:
		new_user = await service.create_user(user)

		return UserResponse.model_validate(new_user)
	except DuplicateEmailException:
		return BaseResponse.response(result=False, status_code=status.HTTP_409_CONFLICT, detail="DUPLICATE_EMAIL_ERROR")
	except SQLAlchemyError:
		return BaseResponse.response(result=False, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="SERVER_ERROR")


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = DB_SESSION):
	"""
	Get user by their id
	:return: User details by their id
	"""
	repo = UserRepository(db)
	service = UserService(repo)

	try:
		user = await service.get_user(user_id)

		return UserResponse.model_validate(user)
	except UserNotFoundException:
		return BaseResponse.response(result=False, status_code=status.HTTP_404_NOT_FOUND, detail="USER_NOT_FOUND_ERROR")
	except SQLAlchemyError:
		return BaseResponse.response(result=False, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="SERVER_ERROR")


@router.get("", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = DB_SESSION):
	"""Get all users"""
	repo = UserRepository(db)
	service = UserService(repo)

	users = await service.get_all_users()

	return [UserResponse.model_validate(user) for user in users]


@router.patch("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def update_user_details(user: UserUpdate, db: AsyncSession = DB_SESSION):
	"""
	Updates user details, if email doesn't exist
	:param user: User details
	:param db: Database
	:return: Returns updated user details
	"""
	repo = UserRepository(db)
	service = UserService(repo)

	try:
		updated_user = await service.update_user(user)

		return UserResponse.model_validate(updated_user)
	except DuplicateEmailException:
		return BaseResponse.response(result=False, status_code=status.HTTP_409_CONFLICT, detail="DUPLICATE_EMAIL_ERROR")
	except SQLAlchemyError:
		return BaseResponse.response(result=False, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="SERVER_ERROR")


@router.delete("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: AsyncSession = DB_SESSION):
	"""
	Delete the user by their id
	:param user_id: User id
	:param db: Database
	:return: Returns the deleted user details
	"""
	repo = UserRepository(db)
	service = UserService(repo)

	try:
		deleted_user = await service.delete_user(user_id)

		return UserResponse.model_validate(deleted_user)
	except UserNotFoundException:
		return BaseResponse.response(result=False, status_code=status.HTTP_404_NOT_FOUND, detail="USER_NOT_FOUND_ERROR")
	except SQLAlchemyError:
		return BaseResponse.response(result=False, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="SERVER_ERROR")
