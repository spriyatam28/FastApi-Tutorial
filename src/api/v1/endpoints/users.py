from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.features.users.repository import UserRepository
from src.features.users.schema import UserResponse, UserCreate, UserUpdate
from src.features.users.service import UserService

router = APIRouter()


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user"""
    repo = UserRepository(db)
    service = UserService(repo)

    try:
        new_user = await service.create_user(user)

        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get user by their id
    :return: User details by their id
    """
    repo = UserRepository(db)
    service = UserService(repo)

    user = await service.get_user(user_id)

    return user


@router.get("", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(get_db)):
    """Get all users"""
    repo = UserRepository(db)
    service = UserService(repo)

    users = await service.get_all_users()

    return users

@router.patch("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def update_user_details(user: UserUpdate, db: AsyncSession = Depends(get_db)):
    """
    Updates user details, if email doesn't exist
    :param user: User details
    :param db: Database
    :return: Returns updated user details
    """
    repo = UserRepository(db)
    service = UserService(repo)

    updated_user = await service.update_user(user)

    return updated_user

@router.delete("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete the user by their id
    :param user_id:
    :param db:
    :return: Returns the deleted user details
    """
    repo=UserRepository(db)
    service=UserService(repo)

    deleted_user = await service.delete_user(user_id)

    return deleted_user