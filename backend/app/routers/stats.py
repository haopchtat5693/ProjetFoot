from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.services.stats_sync_service import sync_and_save_season_stats

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/player/{player_id}/season/{season_id}", response_model=schemas.PlayerSeasonStats)
async def get_player_stats_for_season(player_id: int, season_id: int, db: Session = Depends(get_db)):
    stats = crud.player_season_stats.get_season_stats_by_player_and_season(db, player_id=player_id, season_id=season_id)
    
    if not stats:

        try:
            stats =  await sync_and_save_season_stats(db, player_id=player_id, season_id=season_id)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Stats non trouvées en base et échec de synchronisation API : {str(e)}"
            )
        
    if not stats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail="Stats introuvables"
        )
    
    return stats