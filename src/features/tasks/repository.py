from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.features.tasks.model import Task
from src.features.tasks.schema import TaskCreate, TaskUpdate, TaskResponse
from src.features.users.model import User


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, task: TaskCreate) -> TaskResponse:
        """
        Create a task for a user
        :param: user_id, task
        :return: Task - A task
        """
        new_task = Task(**task.model_dump())

        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)

        return new_task

    async def all_tasks(self, user_id: int) -> list[Task]:
        """
        Get all the tasks of a user
        :param user_id:
        :return: list[Task] - A list of tasks
        """
        tasks = await self.db.execute(select(Task).where(Task.user_id == user_id))

        return list(tasks.scalars().unique().all())

    async def task_by_id(self, user_id: int, task_id: int) -> TaskResponse:
        """
        Get task by its id of a user
        :param user_id: user id
        :param task_id: task id
        :return: Task details
        """
        result = await self.db.execute(
            select(Task).where(Task.user_id == user_id, Task.id == task_id)
        )

        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Either user or task not found!"
            )

        return task

    async def update(self, task: TaskUpdate) -> TaskResponse:
        """

        :param task:
        :return:
        """
        result = await self.db.execute(
            select(Task).where(Task.user_id == task.user_id, Task.id == task.id)
        )

        db_task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Either user or task not found!"
            )

        for field, value in task.model_dump(exclude_unset=True).items():
            setattr(db_task, field, value)

        try:
            await self.db.commit()
            await self.db.refresh(db_task)

            return db_task
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=404,
                detail="Either user or task not found!"
            )

    async def delete(self, user_id: int, task_id: int) -> TaskResponse:
        result = await self.db.execute(
            delete(Task).where(Task.user_id == user_id, Task.id == task_id).returning(Task)
        )

        deleted_task = result.scalar_one_or_none()

        if not deleted_task:
            raise HTTPException(
                status_code=404,
                detail="Either user or task not found!"
            )

        try:
            await self.db.commit()

            return deleted_task
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=404,
                detail="Either user or task not found!"
            )
