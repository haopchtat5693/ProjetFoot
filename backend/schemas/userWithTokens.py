from pydantic import Field

from .token import Token
from .user import UserBase


class UserWithTokens(UserBase):
	id: int
	tokens: list[Token] = Field(default_factory=list)

	class Config:
		from_attributes = True
