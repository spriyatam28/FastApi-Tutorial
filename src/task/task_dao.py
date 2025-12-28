from sqlalchemy import func
from sqlalchemy.orm import Session

from src.task.task_model import Task, TaskCreate, TaskUpdate


def create_task(db: Session, user_id: int, task: TaskCreate):
    new_task = Task(user_id=user_id, task_title=task.task_title, task_body=task.task_body)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def update_task(db: Session, user_id: int, task_id: int, task: TaskUpdate):
    present_task = db.query(Task).filter(Task.user_id == user_id, Task.id == task_id).first()

    if not present_task:
        return None

    present_task.task_title = task.task_title
    present_task.task_body = task.task_body
    present_task.completed = task.completed
    present_task.edited_at = func.now()
    present_task.due_date = task.due_date

    db.commit()
    db.refresh(present_task)

    return present_task


async def get_all_tasks(db: Session, user_id: int):
    return db.query(Task).filter(user_id == Task.user_id).all()
