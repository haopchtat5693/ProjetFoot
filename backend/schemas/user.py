from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from .auth_token import Token

class UserBase(BaseModel):
    username: str
    email: str
    is_admin: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

class User(UserBase):
    id: int
    tokens: list[Token] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)