from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


player_stats_crud = CRUDBase(models.PlayerMatchStats)


def getPlayerMatchStats(db: Session, player_stats_id: int):
    return player_stats_crud.get(db, player_stats_id)


def getPlayerMatchStatsList(db: Session, skip: int = 0, limit: int = 100):
    return player_stats_crud.get_multi(db, skip=skip, limit=limit)

def get_stats_by_player_and_season(db: Session, player_id: int, season_id: int):
    return (
        db.query(models.PlayerMatchStats)
        .filter(
            models.PlayerMatchStats.player_id == player_id,
            models.PlayerMatchStats.season_id == season_id
        )
        .all()
    )

def createPlayerMatchStats(db: Session, player_stats: schemas.PlayerMatchStatsCreate):
    return player_stats_crud.create(db, player_stats)


def updatePlayerMatchStats(
    db: Session,
    player_stats_id: int,
    player_stats_update: schemas.PlayerMatchStatsUpdate,
):
    return player_stats_crud.update(db, player_stats_id, player_stats_update)


def deletePlayerMatchStats(db: Session, player_stats_id: int):
    return player_stats_crud.delete(db, player_stats_id)