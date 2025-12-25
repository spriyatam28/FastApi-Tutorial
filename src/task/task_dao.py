from sqlalchemy.orm import Session

from src.task.task_model import Task, TaskCreate


def create_task(db: Session, user_id: int, task: TaskCreate):
    new_task = Task(user_id=user_id, task_title=task.task_title, task_body=task.task_body)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


async def get_all_tasks(db: Session, user_id: int):
    return db.query(Task).filter(user_id == Task.user_id).all()
