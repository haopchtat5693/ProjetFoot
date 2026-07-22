from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/referees", tags=["Referees"])


@router.post("/", response_model=schemas.Referee)
def create_referee(referee: schemas.RefereeCreate, db: Session = Depends(get_db)):
    return crud.referee.createReferee(db, referee)


@router.get("/{referee_id}", response_model=schemas.Referee)
def get_referee(referee_id: int, db: Session = Depends(get_db)):
    referee = crud.referee.getReferee(db, referee_id)
    if not referee:
        raise HTTPException(status_code=404, detail="Referee not found")
    return referee


@router.get("/", response_model=list[schemas.Referee])
def get_referees(db: Session = Depends(get_db)):
    return crud.referee.getReferees(db)


@router.put("/{referee_id}", response_model=schemas.Referee)
def update_referee(
    referee_id: int, referee_in: schemas.RefereeUpdate, db: Session = Depends(get_db)
):
    referee = crud.referee.getReferee(db, referee_id)
    if not referee:
        raise HTTPException(status_code=404, detail="Referee not found")
    return crud.referee.updateReferee(db, referee_id, referee_in)


@router.delete("/{referee_id}", response_model=schemas.Referee)
def delete_referee(referee_id: int, db: Session = Depends(get_db)):
    referee = crud.referee.getReferee(db, referee_id)
    if not referee:
        raise HTTPException(status_code=404, detail="Referee not found")
    return crud.referee.deleteReferee(db, referee_id)
