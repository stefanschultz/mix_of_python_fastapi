from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from enum import Enum
from typing import Optional

class Roles(str, Enum):
    """Enum for User roles"""
    user = "user"
    admin = "admin"

class BaseUser(SQLModel):
    """Base SQLModel for User"""
    email: EmailStr
    username: str
    is_active: bool = False
    role: Roles

class User(BaseUser, table=True):
    """SQLModel for User"""
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str # Hashed password

class UserSchema(BaseUser):
    """Pydantic schema for User"""
    password: str # Password
