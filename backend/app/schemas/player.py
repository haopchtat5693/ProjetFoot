from app.schemas.contract import Contract
from app.schemas.player_match_stats import PlayerMatchStats
from app.schemas.player_season_stats import PlayerSeasonStats
from pydantic import BaseModel, ConfigDict
from typing import Optional


class PlayerBase(BaseModel):
    name: str
    position: str
    age: int
    salary: Optional[int] = None


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(PlayerBase):
    name: Optional[str] = None
    position: Optional[str] = None
    age: Optional[int] = None
    salary: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class Player(PlayerBase):
    id: int
    contracts: list[Contract] = []
    match_stats: list[PlayerMatchStats] = []
    season_stats: list[PlayerSeasonStats] = []

    model_config = ConfigDict(from_attributes=True)
