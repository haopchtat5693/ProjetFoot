from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


player_match_stats_crud = CRUDBase(models.PlayerMatchStats)


def get_player_match_stats(db: Session, player_stats_id: int):
    return player_match_stats_crud.get(db, player_stats_id)


def get_player_match_stats_list(db: Session, skip: int = 0, limit: int = 100):
    return player_match_stats_crud.get_multi(db, skip=skip, limit=limit)


def get_matches_stats_by_player_and_season(db: Session, player_id: int, season_id: int):
    return (
        db.query(models.PlayerMatchStats)
        .filter(
            models.PlayerMatchStats.player_id == player_id,
            models.PlayerMatchStats.season_id == season_id,
        )
        .all()
    )


def get_stats_by_player_and_match(db: Session, player_id: int, match_id: int):
    return (
        db.query(models.PlayerMatchStats)
        .filter(
            models.PlayerMatchStats.player_id == player_id,
            models.PlayerMatchStats.match_id == match_id,
        )
        .first()
    )


def create_player_match_stats(db: Session, player_stats: schemas.PlayerMatchStatsCreate):
    return player_match_stats_crud.create(db, player_stats)


def update_player_match_stats(
    db: Session,
    player_stats_id: int,
    player_stats_update: schemas.PlayerMatchStatsUpdate,
):
    return player_match_stats_crud.update(db, player_stats_id, player_stats_update)


def delete_player_match_stats(db: Session, player_stats_id: int):
    return player_match_stats_crud.delete(db, player_stats_id)
