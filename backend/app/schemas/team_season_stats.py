from typing import Optional

from pydantic import BaseModel, ConfigDict


class TeamSeasonStatsBase(BaseModel):
    team_id: int
    league_id: int
    season_id: int
    fixtures: Optional[dict] = None
    goals: Optional[dict] = None
    clean_sheet: Optional[dict] = None
    failed_to_score: Optional[dict] = None
    penalty: Optional[dict] = None
    cards: Optional[dict] = None


class TeamSeasonStatsCreate(TeamSeasonStatsBase):
    pass


class TeamSeasonStatsUpdate(BaseModel):
    team_id: Optional[int] = None
    league_id: Optional[int] = None
    season_id: Optional[int] = None
    fixtures: Optional[dict] = None
    goals: Optional[dict] = None
    clean_sheet: Optional[dict] = None
    failed_to_score: Optional[dict] = None
    penalty: Optional[dict] = None
    cards: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


class TeamSeasonStats(TeamSeasonStatsBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
