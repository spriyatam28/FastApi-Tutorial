from datetime import date

from pydantic import BaseModel


class TaskCreate(BaseModel):
    task_title: str
    task_body: str | None = None

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    task_title: str
    task_body: str
    due_date: date
    completed: bool = False

    class Config:
        from_attributes = True


class TaskResponse(BaseModel):
    user_id: int
    id: int
    task_title: str
    task_body: str
    due_date: date
    completed: bool
    created_at: date
    edited_at: date

    class Config:
        from_attributes = True
