from typing import Optional

from app import schemas
from app.crud import player_season_stats_crud, team_season_stats_crud
from app.services.football_api_client import fetch_from_api
from app.services.league_service import ensure_league_exists
from app.services.player_service import ensure_player_exists
from app.services.season_service import ensure_season_exists
from app.services.team_service import ensure_team_exists

from app.services.stadium_service import ensure_stadium_exists
from sqlalchemy.orm import Session

def map_team_api_data_to_schema(
    team_raw: dict, 
    venue_raw: Optional[dict] = None, 
    team_id: int = None,
    coach_id: Optional[int] = None
):
    stadium_id = venue_raw.get('id') if venue_raw else None
    city = venue_raw.get('city', 'Unknown') if venue_raw else 'Unknown'
    

    return schemas.TeamCreate(
        id=team_id,
        name=team_raw.get('name', f'Team {team_id}'),
        city=city,
        logo=team_raw.get('logo', None),
        coach_id=coach_id,
        stadium_id=stadium_id,
    )

async def sync_and_save_team(db: Session, team_id: int):

    data = await fetch_from_api("/teams", {"id": team_id})
    
    if not data or not data.get("response"):
        return None

    item = data["response"][0]
    team_raw = item["team"]
    venue_raw = item["venue"] 

    stadium_id = venue_raw.get("id")
    if stadium_id:
        ensure_stadium_exists(db, stadium_id, venue_raw)

    
    team_create_schema = map_team_api_data_to_schema(
        team_raw=team_raw,
        venue_raw=venue_raw,
        team_id=team_id
    )

    saved_team = ensure_team_exists(db, team_create_schema)

    return saved_team