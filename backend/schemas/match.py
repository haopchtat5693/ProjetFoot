from pydantic import BaseModel, Field
from typing import Optional

class MatchBase(BaseModel):
    home_team_id: int
    away_team_id: int
    date: str
    location: str
    result : Optional[str] = None
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

    class Config:
        from_attributes = True

class Match(MatchBase):
    id: int

    class Config:
        from_attributes = True