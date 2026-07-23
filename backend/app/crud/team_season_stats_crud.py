from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


team_season_stats_crud = CRUDBase(models.TeamSeasonStats)


def get_team_season_stats(db: Session, team_season_stats_id: int):
    return team_season_stats_crud.get(db, team_season_stats_id)


def get_team_season_stats_list(db: Session, skip: int = 0, limit: int = 100):
    return team_season_stats_crud.get_multi(db, skip=skip, limit=limit)


def get_team_season_stats_by_team_league_and_season(
    db: Session, team_id: int, league_id: int, season_id: int
):
    return (
        db.query(models.TeamSeasonStats)
        .filter(
            models.TeamSeasonStats.team_id == team_id,
            models.TeamSeasonStats.league_id == league_id,
            models.TeamSeasonStats.season_id == season_id,
        )
        .first()
    )


def create_team_season_stats(db: Session, team_stats: schemas.TeamSeasonStatsCreate):
    return team_season_stats_crud.create(db, team_stats)


def update_team_season_stats(
    db: Session,
    team_season_stats_id: int,
    team_stats_update: schemas.TeamSeasonStatsUpdate,
):
    return team_season_stats_crud.update(db, team_season_stats_id, team_stats_update)


def delete_team_season_stats(db: Session, team_season_stats_id: int):
    return team_season_stats_crud.delete(db, team_season_stats_id)
