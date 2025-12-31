from src.features.tasks.repository import TaskRepository
from src.features.tasks.model import Task
from src.features.tasks.schema import TaskCreate, TaskResponse, TaskUpdate


class TaskService:
	def __init__(self, repo: TaskRepository):
		self.repo = repo

	async def get_all_tasks(self, user_id: int) -> list[Task]:
		"""
		Get all the tasks of a user
		:param user_id:
		:return: list[Task] - All tasks of a user
		"""
		tasks = await self.repo.all_tasks(user_id)

		return tasks

	async def create_task(self, task: TaskCreate) -> TaskResponse:
		"""
		Creates a new task for a user
		:param task: Create a new task
		:return: Details of the task
		"""
		new_task = await self.repo.create(task)

		return new_task

	async def get_task_by_id(self, user_id: int, task_id: int) -> TaskResponse:
		"""
		Get task based on its id of a user
		:param user_id: id of the user
		:param task_id: id of the task
		:return: Details of the Task
		"""
		task = await self.repo.task_by_id(user_id, task_id)

		return task

	async def update_task(self, task: TaskUpdate) -> TaskResponse:
		"""
		Updates the task, if it exists
		:param task: Task details
		:return: Updated task details
		"""
		updated_task = await self.repo.update(task)

		return updated_task

	async def delete_task(self, user_id: int, task_id: int) -> TaskResponse:
		deleted_task = await self.repo.delete(user_id, task_id)

		return deleted_task
