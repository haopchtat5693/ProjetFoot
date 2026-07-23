from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/seasons", tags=["Seasons"])


@router.post("/", response_model=schemas.Season)
def create_season(season: schemas.SeasonCreate, db: Session = Depends(get_db)):
    return crud.season.create_season(db, season)


@router.get("/{season_id}", response_model=schemas.Season)
def get_season(season_id: int, db: Session = Depends(get_db)):
    season = crud.season.get_season(db, season_id)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return season


@router.get("/", response_model=list[schemas.Season])
def get_seasons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.season.get_seasons(db, skip=skip, limit=limit)


@router.put("/{season_id}", response_model=schemas.Season)
def update_season(
    season_id: int, season_in: schemas.SeasonUpdate, db: Session = Depends(get_db)
):
    season = crud.season.get_season(db, season_id)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return crud.season.update_season(db, season_id, season_in)


@router.delete("/{season_id}", response_model=schemas.Season)
def delete_season(season_id: int, db: Session = Depends(get_db)):
    season = crud.season.get_season(db, season_id)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return crud.season.delete_season(db, season_id)
