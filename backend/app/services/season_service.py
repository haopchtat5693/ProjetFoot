from sqlalchemy.orm import Session
from app import crud


def ensure_season_exists(db: Session, season_id: int):
    season = crud.season_crud.get_season(db, season_id)
    if not season:
        return crud.season_crud.create_season(db, {"id": season_id})
    return season
