from sqlalchemy.orm import Session
from app import models

def ensure_season_exists(db: Session, season_id: int):
    season = db.query(models.Season).filter(models.Season.id == season_id).first()
    if not season:
        season = models.Season(
            id=season_id,
            name=str(season_id),
        )
        db.add(season)
        db.commit()
        db.refresh(season)
    return season