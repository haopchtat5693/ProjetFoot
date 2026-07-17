from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.schemas.auth_token import Token
from app.core.constants import VIEWER

class UserBase(BaseModel):
    username: str
    email: str
    role: str = VIEWER

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

class User(UserBase):
    id: int
    tokens: list[Token] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)