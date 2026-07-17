from pydantic import BaseModel, ConfigDict
from typing import Optional


class ContractBase(BaseModel):
    player_id: int
    team_id: int
    season_id: int


class ContractCreate(ContractBase):
    pass


class ContractUpdate(BaseModel):
    player_id: Optional[int] = None
    team_id: Optional[int] = None
    season_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class Contract(ContractBase):
    id: int

    model_config = ConfigDict(from_attributes=True)