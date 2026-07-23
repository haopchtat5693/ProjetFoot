from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


coach_crud = CRUDBase(models.Coach)


def get_coach(db: Session, coach_id: int):
    return coach_crud.get(db, coach_id)


def get_coaches(db: Session, skip: int = 0, limit: int = 100):
    return coach_crud.get_multi(db, skip=skip, limit=limit)


def create_coach(db: Session, coach: schemas.CoachCreate):
    return coach_crud.create(db, coach)


def update_coach(db: Session, coach_id: int, coach_update: schemas.CoachUpdate):
    return coach_crud.update(db, coach_id, coach_update)


def delete_coach(db: Session, coach_id: int):
    return coach_crud.delete(db, coach_id)
