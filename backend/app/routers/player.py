from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/players", tags=["Players"])


@router.post("/", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    return crud.player.createPlayer(db, player)


@router.get("/{player_id}", response_model=schemas.Player)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = crud.player.getPlayer(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("/", response_model=list[schemas.Player])
def get_players(db: Session = Depends(get_db)):
    return crud.player.getPlayers(db)


@router.put("/{player_id}", response_model=schemas.Player)
def update_player(
    player_id: int, player_in: schemas.PlayerUpdate, db: Session = Depends(get_db)
):
    player = crud.player.getPlayer(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return crud.player.updatePlayer(db, player_id, player_in)


@router.delete("/{player_id}", response_model=schemas.Player)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = crud.player.getPlayer(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return crud.player.deletePlayer(db, player_id)
