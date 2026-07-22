from sqlalchemy.orm import Session
from app import crud, models


def ensure_season_exists(db: Session, season_id: int):
    season = db.query(models.Season).filter(models.Season.id == season_id).first()
    if not season:
        return crud.season.createSeason(db, {"id": season_id, "name": str(season_id)})
    return season
