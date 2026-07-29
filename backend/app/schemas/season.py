from pydantic import BaseModel, ConfigDict
from app.schemas.contract import Contract
from app.schemas.player_season_stats import PlayerSeasonStats


class SeasonCreate(BaseModel):
    id: int


class SeasonUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Season(BaseModel):
    id: int
    contracts: list[Contract] = []
    player_season_stats: list[PlayerSeasonStats] = []

    model_config = ConfigDict(from_attributes=True)
