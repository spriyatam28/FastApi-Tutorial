from sqlalchemy.orm import Session

from src.task.task_model import Task


async def create_task(db: Session, user_id: int, title: str):
    task = Task(title=title, user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


async def get_all_tasks(db: Session, user_id: int):
    return db.query(Task).filter(user_id == Task.user_id).all()
