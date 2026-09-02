from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


fixture_crud = CRUDBase(models.Fixture)


def get_fixture(db: Session, fixture_id: int):
    return fixture_crud.get(db, fixture_id)


def get_fixtures(db: Session, skip: int = 0, limit: int = 100):
    return fixture_crud.get_multi(db, skip=skip, limit=limit)


def get_fixtures_by_league(db: Session, league_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Fixture)
        .filter(models.Fixture.league_id == league_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_fixtures_by_league_and_season(db: Session, league_id: int, season_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Fixture)
        .filter(
            models.Fixture.league_id == league_id,
            models.Fixture.season_id == season_id
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_fixtures_by_team(db: Session, team_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Fixture)
        .filter(
            (models.Fixture.home_team_id == team_id)
            | (models.Fixture.away_team_id == team_id)
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_fixtures_by_team_league_and_season(db: Session, team_id: int, season_id: int, league_id: int, skip: int = 0, limit: int = 100):
    print(f"[CRUD] get_fixtures_by_team_league_and_season: team_id={team_id}, season_id={season_id}, league_id={league_id}, skip={skip}, limit={limit}")
    fixtures = (
        db.query(models.Fixture)
        .filter(
            ((models.Fixture.home_team_id == team_id) |
             (models.Fixture.away_team_id == team_id)),
            models.Fixture.season_id == season_id,
            models.Fixture.league_id == league_id
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
    print(f"[CRUD] Found {len(fixtures)} fixtures for team_id={team_id}, season_id={season_id}, league_id={league_id}")
    for idx, f in enumerate(fixtures):
        print(f"  [{idx}] Fixture ID={f.id}, home_team={f.home_team_id}, away_team={f.away_team_id}, league={f.league_id}, season={f.season_id}")
    return fixtures


def get_fixtures_by_date(db: Session, date: str, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Fixture)
        .filter(models.Fixture.date.like(f"{date}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_fixture_statistics(db: Session, fixture_id: int):
    fixture = get_fixture(db, fixture_id)
    if fixture:
        return fixture.statistics
    return None


def create_fixture(db: Session, fixture: schemas.FixtureCreate):
    return fixture_crud.create(db, fixture)


def update_fixture(db: Session, fixture_id: int, fixture_update: schemas.FixtureUpdate):
    return fixture_crud.update(db, fixture_id, fixture_update)


def delete_fixture(db: Session, fixture_id: int):
    return fixture_crud.delete(db, fixture_id)
