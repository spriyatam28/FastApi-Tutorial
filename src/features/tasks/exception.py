from src.core.exceptions import AppException


class TaskException(AppException):
	"""Base Task Exception"""

	pass


class TaskNotFoundException(TaskException):
	def __init__(self):
		super().__init__("Task not found!", status_code=404)
