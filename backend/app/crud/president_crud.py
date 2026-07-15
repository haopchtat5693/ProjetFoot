from sqlalchemy.orm import Session

import models, schemas

from .base import CRUDBase


president_crud = CRUDBase(models.President)


def getPresident(db: Session, president_id: int):
    return president_crud.get(db, president_id)


def getPresidents(db: Session, skip: int = 0, limit: int = 100):
    return president_crud.get_multi(db, skip=skip, limit=limit)


def createPresident(db: Session, president: schemas.PresidentCreate):
    return president_crud.create(db, president)


def updatePresident(db: Session, president_id: int, president_update: schemas.PresidentUpdate):
    return president_crud.update(db, president_id, president_update)


def deletePresident(db: Session, president_id: int):
    return president_crud.delete(db, president_id)