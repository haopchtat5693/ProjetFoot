from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


match_crud = CRUDBase(models.Match)


def getMatch(db: Session, match_id: int):
    return match_crud.get(db, match_id)


def getMatches(db: Session, skip: int = 0, limit: int = 100):
    return match_crud.get_multi(db, skip=skip, limit=limit)


def createMatch(db: Session, match: schemas.MatchCreate):
    return match_crud.create(db, match)


def updateMatch(db: Session, match_id: int, match_update: schemas.MatchUpdate):
    return match_crud.update(db, match_id, match_update)


def deleteMatch(db: Session, match_id: int):
    return match_crud.delete(db, match_id)