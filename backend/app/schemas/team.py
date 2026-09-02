from pydantic import BaseModel, ConfigDict
from typing import Optional

from app.schemas.fixture import Fixture


class TeamBase(BaseModel):
    name: str
    country: Optional[str] = None
    city: str
    stadium_id: Optional[int] = None
    logo: Optional[str] = None


class TeamCreate(TeamBase):
    id: int


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    logo: Optional[str] = None
    stadium_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class Team(TeamBase):
    id: int
    home_fixtures: list[Fixture] = []
    away_fixtures: list[Fixture] = []

    model_config = ConfigDict(from_attributes=True)
