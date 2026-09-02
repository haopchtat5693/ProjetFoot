from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.player_match_stats import PlayerMatchStats


class FixtureBase(BaseModel):
    home_team_id: int
    away_team_id: int
    date: str
    location: str
    league_id: Optional[int] = None
    season_id: Optional[int] = None
    stadium_id: Optional[int] = None
    result: Optional[str] = None
    status: Optional[str] = None
    timezone: Optional[str] = None
    home_goals: Optional[int] = None
    away_goals: Optional[int] = None
    referee_id: Optional[int] = None
    statistics: Optional[dict] = None


class FixtureCreate(FixtureBase):
    pass


class FixtureUpdate(BaseModel):
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
    date: Optional[str] = None
    location: Optional[str] = None
    league_id: Optional[int] = None
    season_id: Optional[int] = None
    stadium_id: Optional[int] = None
    result: Optional[str] = None
    status: Optional[str] = None
    timezone: Optional[str] = None
    home_goals: Optional[int] = None
    away_goals: Optional[int] = None
    referee_id: Optional[int] = None
    statistics: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


class Fixture(FixtureBase):
    id: int
    players_stats: list[PlayerMatchStats] = []

    model_config = ConfigDict(from_attributes=True)
