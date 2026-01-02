from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
	"""Base user model with common fields"""
	name: str
	email: EmailStr


class UserCreate(UserBase):
	"""Model for creating new user"""
	pass


class UserUpdate(BaseModel):
	id: int
	name: str | None = None
	email: EmailStr | None = None


class UserResponse(UserBase):
	model_config = ConfigDict(from_attributes=True)

	id: int
