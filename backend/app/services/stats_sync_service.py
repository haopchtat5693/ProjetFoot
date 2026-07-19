
from app import schemas
from app.crud import player_season_stats_crud
from app.services.football_api_client import fetch_from_api
from app.services.player_service import ensure_player_exists
from app.services.season_service import ensure_season_exists

from sqlalchemy.orm import Session

def map_api_data_to_schema(api_data: dict, player_id: int, season_id: int):

    return schemas.PlayerSeasonStatsCreate (
        player_id=player_id,
        season_id=season_id,
        total_goals=api_data.get('goals', {}).get('total', 0),
        total_assists=api_data.get('goals', {}).get('assists', 0),
        total_minutes=api_data.get('games', {}).get('minutes', 0),
        avg_rating=api_data.get('games', {}).get('rating', None)
    )

async def sync_and_save_season_stats(db: Session, player_id: int, season_id: int):
    data = await fetch_from_api("/players", {"id": player_id, "season": season_id})
    
    if not data or not data.get('response'):
        return None

    player_raw = data['response'][0].get('player', {})
    stats_block = data['response'][0].get('statistics', [])[0]
    
    ensure_player_exists(db, player_id, player_raw, stats_block)
    ensure_season_exists(db, season_id)
    
    schema_data = map_api_data_to_schema(stats_block, player_id, season_id)
    
    return player_season_stats_crud.createPlayerSeasonStats(db, player_stats=schema_data)