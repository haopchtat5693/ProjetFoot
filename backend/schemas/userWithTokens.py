from pydantic import ConfigDict, Field

from auth_token import Token
from user import UserBase


class UserWithTokens(UserBase):
	id: int
	tokens: list[Token] = Field(default_factory=list)

	model_config = ConfigDict(from_attributes=True)
