from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.USER

class UserUpdate(UserBase):
    password: str | None = None

class UserRoleUpdate(BaseModel):
    role: UserRole

class UserResponse(UserBase):
    id: int
    role: UserRole
    
    model_config = ConfigDict(from_attributes=True)
