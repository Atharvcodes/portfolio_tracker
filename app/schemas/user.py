from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: Optional[str] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if len(v) < 2 or len(v) > 100:
            raise ValueError('Name must be between 2 and 100 characters')
        return v

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str
