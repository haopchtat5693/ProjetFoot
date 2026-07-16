from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


stadium_crud = CRUDBase(models.Stadium)


def getStadium(db: Session, stadium_id: int):
    return stadium_crud.get(db, stadium_id)


def getStadiums(db: Session, skip: int = 0, limit: int = 100):
    return stadium_crud.get_multi(db, skip=skip, limit=limit)


def createStadium(db: Session, stadium: schemas.StadiumCreate):
    return stadium_crud.create(db, stadium)


def updateStadium(db: Session, stadium_id: int, stadium_update: schemas.StadiumUpdate):
    return stadium_crud.update(db, stadium_id, stadium_update)


def deleteStadium(db: Session, stadium_id: int):
    return stadium_crud.delete(db, stadium_id)