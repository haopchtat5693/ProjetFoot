from sqlalchemy.orm import Session

import models, schemas

from .base import CRUDBase


team_crud = CRUDBase(models.Team)


def getTeam(db: Session, team_id: int):
    return team_crud.get(db, team_id)


def getTeams(db: Session, skip: int = 0, limit: int = 100):
    return team_crud.get_multi(db, skip=skip, limit=limit)


def createTeam(db: Session, team: schemas.TeamCreate):
    return team_crud.create(db, team)


def updateTeam(db: Session, team_id: int, team_update: schemas.TeamUpdate):
    return team_crud.update(db, team_id, team_update)


def deleteTeam(db: Session, team_id: int):
    return team_crud.delete(db, team_id)