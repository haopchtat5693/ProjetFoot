from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/presidents", tags=["Presidents"])


@router.post("/", response_model=schemas.President)
def create_president(president: schemas.PresidentCreate, db: Session = Depends(get_db)):
    return crud.president.createPresident(db, president)


@router.get("/{president_id}", response_model=schemas.President)
def get_president(president_id: int, db: Session = Depends(get_db)):
    president = crud.president.getPresident(db, president_id)
    if not president:
        raise HTTPException(status_code=404, detail="President not found")
    return president


@router.get("/", response_model=list[schemas.President])
def get_presidents(db: Session = Depends(get_db)):
    return crud.president.getPresidents(db)


@router.put("/{president_id}", response_model=schemas.President)
def update_president(president_id: int, president_in: schemas.PresidentUpdate, db: Session = Depends(get_db)):
    president = crud.president.getPresident(db, president_id)
    if not president:
        raise HTTPException(status_code=404, detail="President not found")
    return crud.president.updatePresident(db, president_id, president_in)


@router.delete("/{president_id}", response_model=schemas.President)
def delete_president(president_id: int, db: Session = Depends(get_db)):
    president = crud.president.getPresident(db, president_id)
    if not president:
        raise HTTPException(status_code=404, detail="President not found")
    return crud.president.deletePresident(db, president_id)