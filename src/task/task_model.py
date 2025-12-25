from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, func
from sqlalchemy.orm import relationship

from src.storage.database import Base


class Task(Base):
    __tablename__="tasks"

    id=Column(Integer, primary_key=True, autoincrement=True)
    user_id=Column(Integer, ForeignKey("users.id"), nullable=False)
    task_title=Column(String, nullable=False)
    task_body=Column(String, nullable=True)
    completed=Column(Boolean, nullable=False, default=False)
    created_at=Column(Date, nullable=False, default=func.now())
    edited_at=Column(Date, nullable=False, default=func.now())
    due_date=Column(Date, nullable=False, default=func.now())

    user=relationship("User", back_populates="tasks")


class TaskCreate(BaseModel):
    task_title:str
    task_body: str | None=None

    class Config:
        from_attributes=True

# class TaskGetAll(BaseModel):
#     user_id:int
#     id:int
#     task_title:str
#     task_body: str
#     completed: bool
#     due_date:Date
#
#     class Config:
#         from_attributes=True
