from src.core.exceptions import AppException


class UserException(AppException):
	"""Base Exception class to handle User"""

	pass


class UserNotFoundException(UserException):
	def __init__(self):
		super().__init__("User not found!", status_code=404)


class EmailNotFoundException(UserException):
	def __init__(self):
		super().__init__("Email  not found!", status_code=404)


class DuplicateEmailException(UserException):
	def __init__(self):
		super().__init__("Email already in use. Try with a different one.", status_code=400)
