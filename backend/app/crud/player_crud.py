from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


player_crud = CRUDBase(models.Player)


def get_player(db: Session, id: int):
    return player_crud.get(db, id)


def get_players(db: Session, skip: int = 0, limit: int = 400):
    return player_crud.get_multi(db, skip=skip, limit=limit)


def get_players_by_name(db: Session, name: str, limit: int = 20):
    search_term = name.strip()
    if not search_term:
        return []

    normalized_search = f"%{search_term.lower()}%"

    return (
        db.query(models.Player)
        .filter(func.lower(models.Player.name).like(normalized_search))
        .order_by(models.Player.name.asc())
        .limit(limit)
        .all()
    )


def get_players_by_team_and_season(db: Session, team_id: int, season_id: int):
    return (
        db.query(models.Player)
        .join(models.Contract, models.Player.id == models.Contract.player_id)
        .filter(
            models.Contract.team_id == team_id, models.Contract.season_id == season_id
        )
        .all()
    )


def create_player(db: Session, player: schemas.PlayerCreate):
    return player_crud.create(db, player)


def update_player(db: Session, player_id: int, player_update: schemas.PlayerUpdate):
    return player_crud.update(db, player_id, player_update)


def delete_player(db: Session, player_id: int):
    return player_crud.delete(db, player_id)
