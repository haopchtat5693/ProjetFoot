from sqlalchemy.orm import Session

from app import models


def ensure_league_exists(db: Session, league_id: int, league_data: dict):
    league = db.query(models.League).filter(models.League.id == league_id).first()

    if not league:
        league = models.League(
            id=league_id,
            name=league_data.get('name', f'League {league_id}'),
            country=league_data.get('country', 'Unknown'),
        )
        db.add(league)
        db.commit()
        db.refresh(league)
        return league

    league.name = league_data.get('name', league.name)
    league.country = league_data.get('country', league.country)
    db.commit()
    db.refresh(league)
    return league