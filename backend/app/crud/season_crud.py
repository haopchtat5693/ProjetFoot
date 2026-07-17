from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


season_crud = CRUDBase(models.Season)


def getSeason(db: Session, season_id: int):
    return season_crud.get(db, season_id)


def getSeasons(db: Session, skip: int = 0, limit: int = 100):
    return season_crud.get_multi(db, skip=skip, limit=limit)


def createSeason(db: Session, season: schemas.SeasonCreate):
    return season_crud.create(db, season)


def updateSeason(db: Session, season_id: int, season_update: schemas.SeasonUpdate):
    return season_crud.update(db, season_id, season_update)


def deleteSeason(db: Session, season_id: int):
    return season_crud.delete(db, season_id)