from sqlalchemy.orm import Session

from app import crud, models


def ensure_league_exists(db: Session, league_id: int, league_data: dict):
    league = db.query(models.League).filter(models.League.id == league_id).first()

    if not league:
        return crud.league.create_league(
            db,
            {
                "id": league_id,
                "name": league_data.get("name", f"League {league_id}"),
                "country": league_data.get("country", "Unknown"),
            },
        )

    league.name = league_data.get("name", league.name)
    league.country = league_data.get("country", league.country)
    db.commit()
    db.refresh(league)
    return league
