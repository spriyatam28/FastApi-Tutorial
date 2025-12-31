from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.features.tasks.repository import TaskRepository
from src.features.tasks.schema import TaskResponse, TaskCreate, TaskUpdate
from src.features.tasks.service import TaskService

router = APIRouter()
DB_SESSION = Depends(get_db)


@router.get("/{user_id}", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
async def get_tasks(user_id: int, db: AsyncSession = DB_SESSION):
    """
    Get all tasks of a user
    :param user_id: id of the user
    :param db: database
    :return: list of all the tasks of a user
    """
    task_repo = TaskRepository(db)
    service = TaskService(task_repo)

    tasks = await service.get_all_tasks(user_id)

    return tasks


@router.get("/{user_id}/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task_by_id(user_id: int, task_id: int, db: AsyncSession = DB_SESSION):
    """
    Get a task of a user by its id
    :param user_id: User id
    :param task_id: Task id
    :param db: Database
    :return: Task details
    """
    repo = TaskRepository(db)
    service = TaskService(repo)

    task = await service.get_task_by_id(user_id, task_id)

    return task


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: AsyncSession = DB_SESSION):
    """
    Create a new task for a user
    :param task: Task details
    :param db: Database
    :return: Task details
    """
    repo = TaskRepository(db)
    service = TaskService(repo)

    new_task = await service.create_task(task)

    return new_task


@router.patch("", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def update_task(task: TaskUpdate, db: AsyncSession = DB_SESSION):
    """
    Update a task of a user
    :param task: Task details
    :param db: Database
    :return: Updated task details
    """
    repo = TaskRepository(db)
    service = TaskService(repo)

    updated_task = await service.update_task(task)

    return updated_task


@router.delete("/{user_id}/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def delete_task(user_id: int, task_id: int, db: AsyncSession = DB_SESSION):
    """
    Returns deleted task details of a user by its id
    :param user_id: User id
    :param task_id: Task id
    :param db: Database
    :return: Deleted task details
    """
    repo = TaskRepository(db)
    service = TaskService(repo)

    deleted_task = await service.delete_task(user_id, task_id)

    return deleted_task
