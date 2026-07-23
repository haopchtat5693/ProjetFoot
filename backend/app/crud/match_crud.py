from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


match_crud = CRUDBase(models.Match)


def get_match(db: Session, match_id: int):
    return match_crud.get(db, match_id)


def get_matches(db: Session, skip: int = 0, limit: int = 100):
    return match_crud.get_multi(db, skip=skip, limit=limit)


def create_match(db: Session, match: schemas.MatchCreate):
    return match_crud.create(db, match)


def update_match(db: Session, match_id: int, match_update: schemas.MatchUpdate):
    return match_crud.update(db, match_id, match_update)


def delete_match(db: Session, match_id: int):
    return match_crud.delete(db, match_id)
