from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/players", tags=["Players"])


@router.post("/", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    return crud.player.create_player(db, player)


@router.get("/{player_id}", response_model=schemas.Player)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = crud.player.get_player(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("/", response_model=list[schemas.Player])
def get_players(db: Session = Depends(get_db)):
    return crud.player.get_players(db)


@router.put("/{player_id}", response_model=schemas.Player)
def update_player(
    player_id: int, player_in: schemas.PlayerUpdate, db: Session = Depends(get_db)
):
    player = crud.player.get_player(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return crud.player.update_player(db, player_id, player_in)


@router.delete("/{player_id}", response_model=schemas.Player)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = crud.player.get_player(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return crud.player.delete_player(db, player_id)
