from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.features.tasks.repository import TaskRepository
from src.features.tasks.schema import TaskResponse
from src.features.tasks.service import TaskService

router = APIRouter()


@router.get("/{user_id}", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
async def get_tasks(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get all tasks of a user
    :param user_id: id of a user
    :param db: database instance(?)
    :return: A list of tasks
    """
    task_repo = TaskRepository(db)
    service = TaskService(task_repo)

    return await service.get_all_tasks(user_id)
