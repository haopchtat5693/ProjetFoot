from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


league_crud = CRUDBase(models.League)


def get_league(db: Session, league_id: int):
    return league_crud.get(db, league_id)


def get_leagues(db: Session, skip: int = 0, limit: int = 100):
    return league_crud.get_multi(db, skip=skip, limit=limit)


def create_league(db: Session, league: schemas.LeagueCreate):
    return league_crud.create(db, league)


def update_league(db: Session, league_id: int, league_update: schemas.LeagueUpdate):
    return league_crud.update(db, league_id, league_update)


def delete_league(db: Session, league_id: int):
    return league_crud.delete(db, league_id)
