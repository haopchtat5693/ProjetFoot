from pydantic import BaseModel, ConfigDict
from typing import Optional

class TokenBase(BaseModel):
    token: str
    user_id: int

class TokenCreate(TokenBase):
    pass

class TokenUpdate(TokenBase):
    token: Optional[str] = None
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class Token(TokenBase):
    id: int

    model_config = ConfigDict(from_attributes=True)