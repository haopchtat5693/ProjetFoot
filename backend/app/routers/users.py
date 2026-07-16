from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.services import user_service
from app.database import get_db
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_new_user(db, user)

@router.get("/me", response_model=schemas.User)
def get_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/" , response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)

@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int, 
    user_in: schemas.UserUpdate, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user) 
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Vous n'avez pas le droit de modifier ce compte")
    
    user = crud.user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user.update_user(db, user_id, user_in)

@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user) 
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Vous n'avez pas le droit de supprimer ce compte")
        
    user = crud.user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user.delete_user(db, user_id)