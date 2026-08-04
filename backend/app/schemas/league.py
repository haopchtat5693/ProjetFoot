from pydantic import BaseModel, ConfigDict
from typing import Optional

from app.schemas.season import Season
from app.schemas.team import Team


class LeagueBase(BaseModel):
    name: str
    country: str
    league_type: Optional[str] = None
    logo: Optional[str] = None


class LeagueCreate(LeagueBase):
    pass


class LeagueUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    league_type: Optional[str] = None
    logo: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class League(LeagueBase):
    id: int
    teams: list[Team] = []
    seasons: list[Season] = []

    model_config = ConfigDict(from_attributes=True)
