from pydantic import BaseModel, ConfigDict
from typing import Optional


class MatchBase(BaseModel):
    home_team_id: int
    away_team_id: int
    date: str
    location: str
    result: Optional[str] = None
    referee_id: Optional[int] = None


class MatchCreate(MatchBase):
    pass


class MatchUpdate(MatchBase):
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
    date: Optional[str] = None
    location: Optional[str] = None
    result: Optional[str] = None
    referee_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class Match(MatchBase):
    id: int
    stats: list = []

    model_config = ConfigDict(from_attributes=True)
