from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/stadiums", tags=["Stadiums"])


@router.post("/", response_model=schemas.Stadium)
def create_stadium(stadium: schemas.StadiumCreate, db: Session = Depends(get_db)):
    return crud.stadium.createStadium(db, stadium)


@router.get("/{stadium_id}", response_model=schemas.Stadium)
def get_stadium(stadium_id: int, db: Session = Depends(get_db)):
    stadium = crud.stadium.getStadium(db, stadium_id)
    if not stadium:
        raise HTTPException(status_code=404, detail="Stadium not found")
    return stadium


@router.get("/", response_model=list[schemas.Stadium])
def get_stadiums(db: Session = Depends(get_db)):
    return crud.stadium.getStadiums(db)


@router.put("/{stadium_id}", response_model=schemas.Stadium)
def update_stadium(stadium_id: int, stadium_in: schemas.StadiumUpdate, db: Session = Depends(get_db)):
    stadium = crud.stadium.getStadium(db, stadium_id)
    if not stadium:
        raise HTTPException(status_code=404, detail="Stadium not found")
    return crud.stadium.updateStadium(db, stadium_id, stadium_in)


@router.delete("/{stadium_id}", response_model=schemas.Stadium)
def delete_stadium(stadium_id: int, db: Session = Depends(get_db)):
    stadium = crud.stadium.getStadium(db, stadium_id)
    if not stadium:
        raise HTTPException(status_code=404, detail="Stadium not found")
    return crud.stadium.deleteStadium(db, stadium_id)