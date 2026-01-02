from datetime import date

from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
	"""Base task model with common fields"""

	model_config = ConfigDict(from_attributes=True)

	task_title: str
	task_body: str | None = None
	due_date: date
	completed: bool = False


class TaskCreate(TaskBase):
	"""Model for creating a new task"""

	user_id: int


class TaskUpdate(TaskBase):
	user_id: int
	id: int
	task_title: str
	task_body: str
	due_date: date
	completed: bool = False


class TaskResponse(TaskBase):
	user_id: int
	id: int
	task_title: str
	task_body: str
	due_date: date
	completed: bool
	created_at: date
	edited_at: date
