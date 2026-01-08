import datetime
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base


class Task(Base):
	__tablename__ = "tasks"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
	task_title: Mapped[str] = mapped_column(nullable=False)
	task_body: Mapped[Optional[str]] = mapped_column(nullable=True)
	completed: Mapped[bool] = mapped_column(nullable=False, default=False)
	created_at: Mapped[datetime.date] = mapped_column(nullable=False, default=func.now())
	edited_at: Mapped[datetime.date] = mapped_column(nullable=False, default=func.now())
	due_date: Mapped[datetime.date] = mapped_column(nullable=False, default=func.now())

	user = relationship("User", back_populates="tasks")

	def __repr__(self) -> str:
		return (
			f"Task("
			f"id={self.id!r}, "
			f"user_id={self.user_id!r}, "
			f"task_title={self.task_title!r}, "
			f"task_body={self.task_body!r}, "
			f"completed={self.completed!r}, "
			f"created_at={self.created_at!r}, "
			f"edited_at={self.edited_at!r}, "
			f"due_date={self.due_date!r})"
		)
