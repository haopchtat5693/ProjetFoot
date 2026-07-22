from pydantic import BaseModel, ConfigDict
from typing import Optional


class SeasonBase(BaseModel):
    name: str


class SeasonCreate(SeasonBase):
    pass


class SeasonUpdate(BaseModel):
    name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Season(SeasonBase):
    id: int
    contracts: list = []
    match_stats: list = []
    season_stats: list = []

    model_config = ConfigDict(from_attributes=True)
