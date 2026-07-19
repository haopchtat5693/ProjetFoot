from pydantic import BaseModel, ConfigDict
from typing import Optional


class LeagueBase(BaseModel):
	name: str
	country: str


class LeagueCreate(LeagueBase):
	pass


class LeagueUpdate(BaseModel):
	name: Optional[str] = None
	country: Optional[str] = None

	model_config = ConfigDict(from_attributes=True)


class League(LeagueBase):
	id: int
	teams: list = []

	model_config = ConfigDict(from_attributes=True)
