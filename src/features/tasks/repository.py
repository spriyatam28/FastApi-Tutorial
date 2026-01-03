from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from starlette.responses import JSONResponse

from src.core.response import BaseResponse
from src.features.tasks.exception import TaskNotFoundException
from src.features.tasks.model import Task
from src.features.tasks.schema import TaskCreate, TaskUpdate, TaskResponse
from src.features.users.exception import UserNotFoundException
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
        db_user = await self.db.execute(select(User).where(User.id == task.user_id))

        if not db_user.scalar_one_or_none():
            raise UserNotFoundException()

        try:
            new_task = Task(**task.model_dump())

            self.db.add(new_task)
            await self.db.commit()
            await self.db.refresh(new_task)

            return new_task
        except IntegrityError as err:
            raise AttributeError() from err

    async def all_tasks(self, user_id: int) -> list[Task]:
        """
        Get all the tasks of a user
        :param user_id:
        :return: list[Task] - A list of tasks
        """
        db_user = await self.db.execute(select(User).where(User.id == user_id))

        if not db_user.scalar_one_or_none():
            raise UserNotFoundException()

        tasks = await self.db.execute(select(Task).where(Task.user_id == user_id).limit(10).offset(0))

        return list(tasks.scalars().unique().all())

    async def task_by_id(self, user_id: int, task_id: int) -> TaskResponse:
        """
        Get task by its id of a user
        :param user_id: user id
        :param task_id: task id
        :return: Task details
        """
        result = await self.db.execute(select(Task).where(Task.user_id == user_id, Task.id == task_id))

        task = result.scalar_one_or_none()

        if not task:
            raise TaskNotFoundException()

        return task

    async def update(self, task: TaskUpdate) -> TaskResponse:
        """
        Update the task
        :param task: Task details
        :return: Updated task details
        """
        result = await self.db.execute(select(Task).where(Task.user_id == task.user_id, Task.id == task.id))

        db_task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail="Either user or task not found!")

        for field, value in task.model_dump(exclude_unset=True).items():
            setattr(db_task, field, value)

        try:
            await self.db.commit()
            await self.db.refresh(db_task)

            return db_task
        except IntegrityError as err:
            await self.db.rollback()
            raise TaskNotFoundException() from err

    async def delete(self, user_id: int, task_id: int) -> TaskResponse:
        """
        Delete a task by its `id`
        :param user_id: User id
        :param task_id: Task id
        :return: Deleted task details
        """
        result = await self.db.execute(delete(Task).where(Task.user_id == user_id, Task.id == task_id).returning(Task))

        deleted_task = result.scalar_one_or_none()

        if not deleted_task:
            raise TaskNotFoundException()

        try:
            await self.db.commit()

            return deleted_task
        except IntegrityError as err:
            await self.db.rollback()
            raise TaskNotFoundException() from err

    async def delete_all(self, user_id: int) -> JSONResponse:
        """
        Delete all the tasks
        :param user_id: User id
        :return: A JSON response with `successful` as a key and true if successful otherwise false
        """
        result = await self.db.execute(select(Task).where(Task.user_id == user_id))

        db_user = result.scalar_one_or_none()

        if not db_user:
            raise UserNotFoundException()

        try:
            await self.db.execute(delete(Task).where(Task.user_id == user_id))

            await self.db.commit()

            return BaseResponse.response(True)
        except IntegrityError as err:
            await self.db.rollback()

            return BaseResponse.response(False)
