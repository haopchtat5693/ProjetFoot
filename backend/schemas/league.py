from pydantic import BaseModel
from typing import Optional


class LeagueBase(BaseModel):
	name: str
	country: str


class LeagueCreate(LeagueBase):
	pass


class LeagueUpdate(BaseModel):
	name: Optional[str] = None
	country: Optional[str] = None

	class Config:
		from_attributes = True


class League(LeagueBase):
	id: int

	class Config:
		from_attributes = True
