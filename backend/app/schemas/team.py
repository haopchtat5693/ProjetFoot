from pydantic import BaseModel, ConfigDict
from typing import Optional

from app.schemas.match import Match


class TeamBase(BaseModel):
    name: str
    city: str
    coach_id: Optional[int] = None
    stadium_id: Optional[int] = None
    logo: Optional[str] = None


class TeamCreate(TeamBase):
    id: int


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    logo: Optional[str] = None
    coach_id: Optional[int] = None
    stadium_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class Team(TeamBase):
    id: int
    home_matches: list[Match] = []
    away_matches: list[Match] = []

    model_config = ConfigDict(from_attributes=True)
