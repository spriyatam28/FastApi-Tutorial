from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db

router = APIRouter()


@router.get("\{user_id}", response_model=list[TaskResponse])
async def get_tasks(user_id: int, db: AsyncSession=Depends(get_db)):
    """Get all tasks for a user"""
    task_repo=TaskRepositroy(db)
    service=TaskService(task_repo)

    return await service.get_all_tasks(user_id)
