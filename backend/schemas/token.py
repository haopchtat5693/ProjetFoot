from pydantic import BaseModel, Field
from typing import Optional

class TokenBase(BaseModel):
    token: str
    user_id: int

class TokenCreate(TokenBase):
    pass

class TokenUpdate(TokenBase):
    token: Optional[str] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class Token(TokenBase):
    id: int

    class Config:
        from_attributes = True