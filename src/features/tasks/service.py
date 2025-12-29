from src.features.tasks.repository import TaskRepository
from src.features.tasks.model import Task


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def get_all_tasks(self, user_id: int)-> list[Task]:
        """
        Get all the tasks of a user
        :param user_id:
        :return: list[Task] - All tasks of a user
        """
        tasks = await self.repo.get_all_tasks(user_id)

        return tasks
