from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


coach_crud = CRUDBase(models.Coach)


def getCoach(db: Session, coach_id: int):
    return coach_crud.get(db, coach_id)


def getCoaches(db: Session, skip: int = 0, limit: int = 100):
    return coach_crud.get_multi(db, skip=skip, limit=limit)


def createCoach(db: Session, coach: schemas.CoachCreate):
    return coach_crud.create(db, coach)


def updateCoach(db: Session, coach_id: int, coach_update: schemas.CoachUpdate):
    return coach_crud.update(db, coach_id, coach_update)


def deleteCoach(db: Session, coach_id: int):
    return coach_crud.delete(db, coach_id)
