from sqlalchemy.orm import Session

import models, schemas

from .base import CRUDBase


player_crud = CRUDBase(models.Player)


def getPlayer(db: Session, id: int):
    return player_crud.get(db, id)


def getPlayers(db: Session, skip: int = 0, limit: int = 100):
    return player_crud.get_multi(db, skip=skip, limit=limit)


def createPlayer(db: Session, player: schemas.PlayerCreate):
    return player_crud.create(db, player)


def updatePlayer(db: Session, player_id: int, player_update: schemas.PlayerUpdate):
    return player_crud.update(db, player_id, player_update)


def deletePlayer(db: Session, player_id: int):
    return player_crud.delete(db, player_id)