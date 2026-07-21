from app import schemas
from app.crud import player_season_stats_crud, team_season_stats_crud
from app.services.football_api_client import fetch_from_api
from app.services.league_service import ensure_league_exists
from app.services.player_service import ensure_player_exists
from app.services.season_service import ensure_season_exists
from app.services.team_service import ensure_team_exists

from app.services.team_sync_service import map_team_api_data_to_schema
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


def map_team_stats_api_data_to_schema(api_data: dict, team_id: int, league_id: int, season_id: int):
    return schemas.TeamSeasonStatsCreate(
        team_id=team_id,
        league_id=league_id,
        season_id=season_id,
        fixtures=api_data.get('fixtures'),
        goals=api_data.get('goals'),
        clean_sheet=api_data.get('clean_sheet'),
        failed_to_score=api_data.get('failed_to_score'),
        penalty=api_data.get('penalty'),
        cards=api_data.get('cards'),
    )


async def sync_and_save_team_stats(db: Session, team_id: int, league_id: int, season_id: int):
    params = {
        'team': team_id,
        'league': league_id,
        'season': season_id,
    }

    data = await fetch_from_api('/teams/statistics', params)

    response = data.get('response') if data else None
    if not response:
        return None

    league_raw = response.get('league', {})
    team_raw = response.get('team', {})

    ensure_league_exists(db, league_id, league_raw)
    ensure_season_exists(db, season_id)

    team_create_schema = map_team_api_data_to_schema(
        team_raw=team_raw,
        venue_raw=None, 
        team_id=team_id
    )
    ensure_team_exists(db, team_create_schema)

    schema_data = map_team_stats_api_data_to_schema(response, team_id, league_id, season_id)

    existing_stats = team_season_stats_crud.get_team_season_stats_by_team_league_and_season(
        db,
        team_id=team_id,
        league_id=league_id,
        season_id=season_id,
    )

    if existing_stats:
        return team_season_stats_crud.updateTeamSeasonStats(db, existing_stats.id, schema_data)

    return team_season_stats_crud.createTeamSeasonStats(db, team_stats=schema_data)