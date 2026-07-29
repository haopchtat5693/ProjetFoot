from sqlalchemy.orm import Session

from app import crud, models


def ensure_league_exists(db: Session, league_id: int, league_data: dict):
    league = crud.league_crud.get_league(db, league_id)

    if not league:
        return crud.league_crud.create_league(
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
