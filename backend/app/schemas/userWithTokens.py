from pydantic import ConfigDict, Field

from backend.app.schemas.auth_token import Token
from backend.app.schemas.user import UserBase


class UserWithTokens(UserBase):
	id: int
	tokens: list[Token] = Field(default_factory=list)

	model_config = ConfigDict(from_attributes=True)
