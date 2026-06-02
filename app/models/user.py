from pydantic import BaseModel, Field, BeforeValidator, EmailStr
from typing import Annotated, Optional, Literal

PyObjectId = Annotated[str, BeforeValidator(str)]

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Literal['admin', 'staff']
    status: Literal['active', 'inactive']
    createdAt: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Literal['admin', 'staff']] = None
    status: Optional[Literal['active', 'inactive']] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: Optional[PyObjectId] = Field(validation_alias="_id", serialization_alias="id", default=None)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "60d5ec4b9671d12345678912",
                "name": "Nguyễn Văn Admin",
                "email": "admin@realty.com",
                "role": "admin",
                "status": "active",
                "createdAt": "2026-01-15"
            }
        }
    }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str
    user: UserResponse
