from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.services import stats_service

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/player/{player_id}/season/{season_id}", response_model=schemas.PlayerSeasonSummary)
def get_player_stats_for_season(player_id: int, season_id: int, db: Session = Depends(get_db)):
    stats = stats_service.get_season_stats_for_player(db, player_id, season_id)
    
    if not stats:
        raise HTTPException(status_code=404, detail="Stats not found for the given player and season")
    
    return stats