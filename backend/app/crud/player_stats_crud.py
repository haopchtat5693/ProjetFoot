from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


player_stats_crud = CRUDBase(models.PlayerStats)


def getPlayerStats(db: Session, player_stats_id: int):
    return player_stats_crud.get(db, player_stats_id)


def getPlayerStatsList(db: Session, skip: int = 0, limit: int = 100):
    return player_stats_crud.get_multi(db, skip=skip, limit=limit)


def createPlayerStats(db: Session, player_stats: schemas.PlayerStatsCreate):
    return player_stats_crud.create(db, player_stats)


def updatePlayerStats(
    db: Session,
    player_stats_id: int,
    player_stats_update: schemas.PlayerStatsUpdate,
):
    return player_stats_crud.update(db, player_stats_id, player_stats_update)


def deletePlayerStats(db: Session, player_stats_id: int):
    return player_stats_crud.delete(db, player_stats_id)