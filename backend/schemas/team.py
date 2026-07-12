from pydantic import BaseModel
from typing import Optional


class TeamBase(BaseModel):
	name: str
	city: str
	president_id: Optional[int] = None
	coach_id: Optional[int] = None
	stadium_id: Optional[int] = None
	league_id: Optional[int] = None


class TeamCreate(TeamBase):
	pass


class TeamUpdate(BaseModel):
	name: Optional[str] = None
	city: Optional[str] = None
	president_id: Optional[int] = None
	coach_id: Optional[int] = None
	stadium_id: Optional[int] = None
	league_id: Optional[int] = None

	class Config:
		from_attributes = True


class Team(TeamBase):
	id: int

	class Config:
		from_attributes = True
