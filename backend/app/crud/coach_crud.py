from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


coach_crud = CRUDBase(models.Coach)


def get_coach(db: Session, coach_id: int):
    return coach_crud.get(db, coach_id)


def get_coaches(db: Session, skip: int = 0, limit: int = 100):
    return coach_crud.get_multi(db, skip=skip, limit=limit)


def get_coaches_by_name(db: Session, name: str, limit: int = 50):
    search_term = name.strip()
    if not search_term:
        return []

    normalized_search = f"%{search_term.lower()}%"

    return (
        db.query(models.Coach)
        .filter(func.lower(models.Coach.name).like(normalized_search))
        .order_by(models.Coach.name.asc())
        .limit(limit)
        .all()
    )


def get_coaches_by_team(db: Session, team_id: int):
    return (
        db.query(models.Coach)
        .join(models.CoachCareer, models.Coach.id == models.CoachCareer.coach_id)
        .filter(models.CoachCareer.team_id == team_id)
        .distinct()
        .all()
    )


def create_coach(db: Session, coach: schemas.CoachCreate):
    return coach_crud.create(db, coach)


def update_coach(db: Session, coach_id: int, coach_update: schemas.CoachUpdate):
    return coach_crud.update(db, coach_id, coach_update)


def delete_coach(db: Session, coach_id: int):
    return coach_crud.delete(db, coach_id)
