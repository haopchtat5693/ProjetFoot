from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


referee_crud = CRUDBase(models.Referee)


def getReferee(db: Session, referee_id: int):
    return referee_crud.get(db, referee_id)


def getReferees(db: Session, skip: int = 0, limit: int = 100):
    return referee_crud.get_multi(db, skip=skip, limit=limit)


def createReferee(db: Session, referee: schemas.RefereeCreate):
    return referee_crud.create(db, referee)


def updateReferee(db: Session, referee_id: int, referee_update: schemas.RefereeUpdate):
    return referee_crud.update(db, referee_id, referee_update)


def deleteReferee(db: Session, referee_id: int):
    return referee_crud.delete(db, referee_id)
