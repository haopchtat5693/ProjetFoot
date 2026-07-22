from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


player_season_stats_crud = CRUDBase(models.PlayerSeasonStats)


def getPlayerSeasonStats(db: Session, player_season_stats_id: int):
    return player_season_stats_crud.get(db, player_season_stats_id)


def getPlayerSeasonStatsList(db: Session, skip: int = 0, limit: int = 100):
    return player_season_stats_crud.get_multi(db, skip=skip, limit=limit)


def get_season_stats_by_player_and_season(db: Session, player_id: int, season_id: int):
    return (
        db.query(models.PlayerSeasonStats)
        .filter(
            models.PlayerSeasonStats.player_id == player_id,
            models.PlayerSeasonStats.season_id == season_id,
        )
        .first()
    )


def get_stats_by_player(db: Session, player_id: int):
    return (
        db.query(models.PlayerSeasonStats)
        .filter(models.PlayerSeasonStats.player_id == player_id)
        .all()
    )


def createPlayerSeasonStats(db: Session, player_stats: schemas.PlayerSeasonStatsCreate):
    return player_season_stats_crud.create(db, obj_in=player_stats)


def updatePlayerSeasonStats(
    db: Session,
    player_season_stats_id: int,
    player_stats_update: schemas.PlayerSeasonStatsUpdate,
):
    return player_season_stats_crud.update(
        db, player_season_stats_id, obj_in=player_stats_update
    )


def deletePlayerSeasonStats(db: Session, player_season_stats_id: int):
    return player_season_stats_crud.delete(db, player_season_stats_id)
