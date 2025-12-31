from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Date, func
from sqlalchemy.orm import relationship

from src.database import Base


class Task(Base):
	__tablename__ = "tasks"

	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	task_title = Column(String, nullable=False)
	task_body = Column(String, nullable=True)
	completed = Column(Boolean, nullable=False, default=False)
	created_at = Column(Date, nullable=False, default=func.now())
	edited_at = Column(Date, nullable=False, default=func.now())
	due_date = Column(Date, nullable=False, default=func.now())

	user = relationship("User", back_populates="tasks")
