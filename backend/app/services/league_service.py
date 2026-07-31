from sqlalchemy.orm import Session

from app import crud


def map_league_api_data_to_payload(league_raw: dict) -> dict:
    return {
        "id": league_raw.get("id"),
        "name": league_raw.get("name", "Unknown"),
        "country": league_raw.get("country", "Unknown"),
    }


def ensure_league_exists(db: Session, league_id: int, league_data: dict):
    league = crud.league_crud.get_league(db, league_id)

    if not league:
        return crud.league_crud.create_league(db, league_data)

    league.name = league_data["name"]
    league.country = league_data["country"]
    db.commit()
    db.refresh(league)
    return league
