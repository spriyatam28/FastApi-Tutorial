from datetime import date

from pydantic import BaseModel


class TaskCreate(BaseModel):
    task_title:str
    task_body: str | None=None

    class Config:
        from_attributes=True

class TaskUpdate(BaseModel):
    task_title: str
    task_body: str
    due_date: date
    completed: bool = False

    class Config:
        from_attributes=True