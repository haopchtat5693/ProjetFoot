from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/leagues", tags=["Leagues"])


@router.post("/", response_model=schemas.League)
def create_league(league: schemas.LeagueCreate, db: Session = Depends(get_db)):
    return crud.league.create_league(db, league)


@router.get("/{league_id}", response_model=schemas.League)
def get_league(league_id: int, db: Session = Depends(get_db)):
    league = crud.league.get_league(db, league_id)
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    return league


@router.get("/", response_model=list[schemas.League])
def get_leagues(db: Session = Depends(get_db)):
    return crud.league.get_leagues(db)


@router.put("/{league_id}", response_model=schemas.League)
def update_league(
    league_id: int, league_in: schemas.LeagueUpdate, db: Session = Depends(get_db)
):
    league = crud.league.get_league(db, league_id)
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    return crud.league.update_league(db, league_id, league_in)


@router.delete("/{league_id}", response_model=schemas.League)
def delete_league(league_id: int, db: Session = Depends(get_db)):
    league = crud.league.get_league(db, league_id)
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    return crud.league.delete_league(db, league_id)
