from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
	"""Base user model with common fields"""

	name: str
	email: EmailStr


class UserCreate(UserBase):
	"""Model for creating new user"""

	pass


class UserUpdate(UserBase):
	id: int
	name: Optional[str] = None
	email: Optional[EmailStr] = None


class UserResponse(UserBase):
	model_config = ConfigDict(from_attributes=True)

	id: int
