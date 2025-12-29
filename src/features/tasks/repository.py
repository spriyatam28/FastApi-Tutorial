from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.features.tasks.model import Task
from src.features.tasks.schema import TaskUpdate, TaskCreate


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int, task: TaskCreate) -> Task:
        """Create a task for a user"""
        new_task = Task(user_id=user_id, **task.model_dump())

        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)

        return new_task


def get_all_tasks(db: Session, user_id: int):
    return db.query(Task).filter(user_id == Task.user_id).all()
