from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


team_crud = CRUDBase(models.Team)


def get_team(db: Session, team_id: int):
    return team_crud.get(db, team_id)


def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return team_crud.get_multi(db, skip=skip, limit=limit)


def create_team(db: Session, team: schemas.TeamCreate):
    return team_crud.create(db, team)


def update_team(db: Session, team_id: int, team_update: schemas.TeamUpdate):
    return team_crud.update(db, team_id, team_update)


def delete_team(db: Session, team_id: int):
    return team_crud.delete(db, team_id)
