from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.features.users.repository import UserRepository
from src.features.users.schema import UserResponse, UserCreate
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


@router.get("", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    """Get all users"""
    repo = UserRepository(db)
    service = UserService(repo)

    users = await service.get_all_users()

    return users
