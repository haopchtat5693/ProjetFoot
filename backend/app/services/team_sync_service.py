
from app import schemas
from app.services.football_api_client import fetch_from_api
from app.services.team_service import ensure_team_exists, map_team_api_data_to_payload

from app.services.stadium_service import (
    ensure_stadium_exists,
    map_stadium_api_data_to_payload,
)
from sqlalchemy.orm import Session


async def sync_and_save_team(db: Session, team_id: int):

    data = await fetch_from_api("/teams", {"id": team_id})

    if not data or not data.get("response"):
        return None

    item = data["response"][0]
    team_raw = item["team"]
    venue_raw = item["venue"]

    stadium_id = venue_raw.get("id")
    if stadium_id:
        stadium_payload = map_stadium_api_data_to_payload(venue_raw)
        ensure_stadium_exists(db, stadium_id, stadium_payload)

    team_create_schema = schemas.TeamCreate(
        **map_team_api_data_to_payload(team_raw, venue_raw, team_id)
    )

    saved_team = ensure_team_exists(db, team_create_schema)

    return saved_team
