from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional


class TokenBase(BaseModel):
    token: str
    user_id: int
    expires_at: datetime


class TokenCreate(TokenBase):
    pass


class TokenUpdate(TokenBase):
    token: Optional[str] = None
    user_id: Optional[int] = None
    expires_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class Token(TokenBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
