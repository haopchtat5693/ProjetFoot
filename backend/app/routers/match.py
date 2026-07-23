from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.post("/", response_model=schemas.Match)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    return crud.match.create_match(db, match)


@router.get("/{match_id}", response_model=schemas.Match)
def get_match(match_id: int, db: Session = Depends(get_db)):
    match = crud.match.get_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.get("/", response_model=list[schemas.Match])
def get_matches(db: Session = Depends(get_db)):
    return crud.match.get_matches(db)


@router.put("/{match_id}", response_model=schemas.Match)
def update_match(
    match_id: int, match_in: schemas.MatchUpdate, db: Session = Depends(get_db)
):
    match = crud.match.get_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return crud.match.update_match(db, match_id, match_in)


@router.delete("/{match_id}", response_model=schemas.Match)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    match = crud.match.get_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return crud.match.delete_match(db, match_id)
