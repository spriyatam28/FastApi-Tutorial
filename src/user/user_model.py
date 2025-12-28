from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from src.storage.database import Base

class User(Base):
    __tablename__="users"

    id=Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String, nullable=False, default="User")
    email=Column(String, nullable=False, unique=True)

    tasks=relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan"
    )

class UserCreate(BaseModel):
    name:str
    email:EmailStr

    class Config:
        from_attributes=True