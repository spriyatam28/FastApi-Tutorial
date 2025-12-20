from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from src.storage.storage import Base


class Task(Base):
    __tablename__="tasks"

    id=Column(Integer, primary_key=True, autoincrement=True)
    user_id=Column(Integer, ForeignKey("users.id"), nullable=False)
    task_title=Column(String, nullable=False)
    task_body=Column(String, nullable=True)
    completed=Column(Boolean, nullable=False, default=False)
    created_at=Column(Date, nullable=False)
    edited_at=Column(Date, nullable=False)
    due_date=Column(Date, nullable=False)

    user=relationship("User", back_populates="tasks")


class TaskCreate(BaseModel):
    id:int
    task_title:str
    task_body: str | None=None

    class Config:
        from_attributes=True
