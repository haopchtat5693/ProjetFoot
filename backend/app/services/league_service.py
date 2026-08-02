from sqlalchemy.orm import Session

from app import crud, schemas
from app.services.football_api_client import fetch_from_api
from app.services.season_service import ensure_season_exists


def map_league_api_data_to_payload(
    league_raw: dict,
    country_raw: dict | None = None,
) -> schemas.LeagueCreate:
    return schemas.LeagueCreate(
        name=league_raw.get("name", "Unknown"),
        country=(country_raw or {}).get("name", league_raw.get("country", "Unknown")),
        league_type=league_raw.get("type"),
    )


def ensure_league_exists(db: Session, league_id: int, league_data: schemas.LeagueCreate):
    league = crud.league_crud.get_league(db, league_id)

    if not league:
        return crud.league_crud.create_league(db, {"id": league_id, **league_data.model_dump()})

    league.name = league_data.name
    league.country = league_data.country
    league.league_type = league_data.league_type
    db.commit()
    db.refresh(league)
    return league


async def lookup_leagues(
    db: Session,
    *,
    league_id: int | None = None,
    search: str | None = None,
    season: int | None = None,
    league_type: str | None = None,
) -> list[schemas.League]:
    params: dict[str, str | int | bool] = {}

    if league_id is not None:
        params["id"] = league_id
    if search:
        params["search"] = search
    if season is not None:
        params["season"] = season
    if league_type:
        params["type"] = league_type

    data = await fetch_from_api("/leagues", params or None)
    response = data.get("response", []) if data else []

    mapped_leagues: list[schemas.League] = []
    for item in response:
        league_raw = item.get("league", {})
        country_raw = item.get("country", {})
        league_payload = map_league_api_data_to_payload(league_raw, country_raw)

        league_id_value = league_raw.get("id")
        if league_id_value is not None:
            ensure_league_exists(db, league_id_value, league_payload)

        mapped_leagues.append(
            schemas.League(
                id=league_id_value,
                name=league_payload.name,
                country=league_payload.country,
                league_type=league_payload.league_type,
                teams=[],
                seasons=[
                    schemas.Season(id=season.get("year"))
                    for season in item.get("seasons", [])
                    if season.get("year") is not None
                ],
            )
        )

        for season in item.get("seasons", []):
            season_year = season.get("year")
            if season_year is not None:
                ensure_season_exists(db, season_year)

    return mapped_leagues
