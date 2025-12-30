from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.tasks.model import Task
from src.features.tasks.schema import TaskCreate
from src.features.users.model import User


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int, task: TaskCreate) -> Task:
        """
        Create a task for a user
        :param: user_id, task
        :return: Task - A task
        """
        new_task = Task(user_id=user_id, **task.model_dump())

        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)

        return new_task

    async def get_all_tasks(self, user_id: int) -> list[Task]:
        """
        Get all the tasks of a user
        :param user_id:
        :return: list[Task] - A list of tasks
        """
        tasks = await self.db.execute(select(Task).where(User.id == user_id))

        return list(tasks.scalars().unique().all())
