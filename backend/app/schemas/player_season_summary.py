from pydantic import BaseModel, ConfigDict
from typing import List
from .player_match_stats import PlayerMatchStats 

class PlayerSeasonSummary(BaseModel):
    player_id: int
    total_goals: int
    total_assists: int
    total_yellow_cards: int
    total_red_cards: int
    average_goal: float
    average_assist: float
    details: List[PlayerMatchStats] 

    model_config = ConfigDict(from_attributes=True)