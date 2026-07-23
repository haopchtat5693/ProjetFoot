from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


season_crud = CRUDBase(models.Season)


def get_season(db: Session, season_id: int):
    return season_crud.get(db, season_id)


def get_seasons(db: Session, skip: int = 0, limit: int = 100):
    return season_crud.get_multi(db, skip=skip, limit=limit)


def create_season(db: Session, season: schemas.SeasonCreate):
    return season_crud.create(db, season)


def update_season(db: Session, season_id: int, season_update: schemas.SeasonUpdate):
    return season_crud.update(db, season_id, season_update)


def delete_season(db: Session, season_id: int):
    return season_crud.delete(db, season_id)
