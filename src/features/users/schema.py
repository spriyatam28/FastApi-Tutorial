from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: EmailStr | None = None

class UserResponse(BaseModel):
    id: int
    is_active: bool

    class Config:
        from_attributes = True