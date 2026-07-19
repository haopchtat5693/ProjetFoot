import string

from pydantic import BaseModel, ConfigDict
from typing import Optional


class PlayerSeasonStatsBase(BaseModel):
    player_id: int
    season_id: int
    total_goals: Optional[int] = 0
    total_assists: Optional[int] = 0
    total_minutes: Optional[int] = 0
    avg_rating: Optional[str] = None


class PlayerSeasonStatsCreate(PlayerSeasonStatsBase):
    pass


class PlayerSeasonStatsUpdate(BaseModel):
    player_id: Optional[int] = None
    season_id: Optional[int] = None
    total_goals: Optional[int] = None
    total_assists: Optional[int] = None
    total_minutes: Optional[int] = None
    avg_rating: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PlayerSeasonStats(PlayerSeasonStatsBase):
    id: int

    model_config = ConfigDict(from_attributes=True)