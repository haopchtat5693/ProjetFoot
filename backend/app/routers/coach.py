from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/coaches", tags=["Coaches"])


@router.post("/", response_model=schemas.Coach)
def create_coach(coach: schemas.CoachCreate, db: Session = Depends(get_db)):
    return crud.coach_crud.create_coach(db, coach)


@router.get("/{coach_id}", response_model=schemas.Coach)
def get_coach(coach_id: int, db: Session = Depends(get_db)):
    coach = crud.coach_crud.get_coach(db, coach_id)
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")
    return coach


@router.get("/", response_model=list[schemas.Coach])
def get_coaches(db: Session = Depends(get_db)):
    return crud.coach_crud.get_coaches(db)


@router.put("/{coach_id}", response_model=schemas.Coach)
def update_coach(
    coach_id: int, coach_in: schemas.CoachUpdate, db: Session = Depends(get_db)
):
    coach = crud.coach_crud.get_coach(db, coach_id)
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")
    return crud.coach_crud.update_coach(db, coach_id, coach_in)


@router.delete("/{coach_id}", response_model=schemas.Coach)
def delete_coach(coach_id: int, db: Session = Depends(get_db)):
    coach = crud.coach_crud.get_coach(db, coach_id)
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")
    return crud.coach_crud.delete_coach(db, coach_id)
