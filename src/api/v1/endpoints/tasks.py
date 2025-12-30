from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.features.tasks.repository import TaskRepository
from src.features.tasks.schema import TaskResponse, TaskCreate, TaskUpdate
from src.features.tasks.service import TaskService

router = APIRouter()


@router.get("/{user_id}", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
async def get_tasks(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get all tasks of a user
    :param user_id: id of the user
    :param db: database
    :return: list of all the tasks of a user
    """
    task_repo = TaskRepository(db)
    service = TaskService(task_repo)

    return await service.get_all_tasks(user_id)

@router.get("/{user_id}/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task_by_id(user_id: int, task_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a task of a user by its id
    :param user_id: User id
    :param task_id: Task id
    :param db: Database
    :return: Task details
    """
    pass

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new task for a user
    :param task: Task details
    :param db: Database
    :return: Task details
    """
    pass

@router.patch("", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def update_task(task: TaskUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update a task of a user
    :param task: Task details
    :param db: Database
    :return: Updated task details
    """
    pass

