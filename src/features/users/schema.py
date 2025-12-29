from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    id: int
    name: str
    email: EmailStr | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True