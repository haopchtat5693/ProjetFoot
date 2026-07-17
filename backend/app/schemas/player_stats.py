from pydantic import BaseModel, ConfigDict
from typing import Optional


class PlayerStatsBase(BaseModel):
    player_id: int
    match_id: int
    season_id: int
    goals: Optional[int] = 0
    assists: Optional[int] = 0
    yellow_cards: Optional[int] = 0
    minutes_played: Optional[int] = 0


class PlayerStatsCreate(PlayerStatsBase):
    pass


class PlayerStatsUpdate(BaseModel):
    player_id: Optional[int] = None
    match_id: Optional[int] = None
    season_id: Optional[int] = None
    goals: Optional[int] = None
    assists: Optional[int] = None
    yellow_cards: Optional[int] = None
    minutes_played: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class PlayerStats(PlayerStatsBase):
    id: int

    model_config = ConfigDict(from_attributes=True)