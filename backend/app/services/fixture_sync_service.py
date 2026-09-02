from app import schemas
from app.crud import fixture_crud
from app.services.football_api_client import fetch_from_api
from app.services.league_service import (
    ensure_league_exists,
    map_league_api_data_to_payload,
)
from app.services.stadium_service import (
    ensure_stadium_exists,
    map_stadium_api_data_to_payload,
)
from app.services.team_service import ensure_team_exists, map_team_api_data_to_payload
from sqlalchemy.orm import Session


def map_fixture_api_data_to_payload(
    fixture_raw: dict, league_raw: dict, teams_raw: dict, goals: dict = None
):
    """Map API fixture data to FixtureCreate payload"""
    if goals is None:
        goals = {}
    home_team = teams_raw.get("home", {})
    away_team = teams_raw.get("away", {})
    venue_data = fixture_raw.get("venue", {})
    status = fixture_raw.get("status", {})
    fixture_id = fixture_raw.get("id")

    print(f"[FIXTURE MAP] ID={fixture_id} - RAW GOALS: {goals}")
    print(f"[FIXTURE MAP] ID={fixture_id} - home_goals={goals.get('home')}, away_goals={goals.get('away')}")

    payload = {
        "id": fixture_id,
        "home_team_id": home_team.get("id"),
        "away_team_id": away_team.get("id"),
        "league_id": league_raw.get("id"),
        "season_id": league_raw.get("season"),
        "stadium_id": venue_data.get("id"),
        "date": fixture_raw.get("date"),
        "location": venue_data.get("name", "Unknown"),
        "status": status.get("short"),
        "timezone": fixture_raw.get("timezone"),
        "home_goals": goals.get("home"),
        "away_goals": goals.get("away"),
        "result": f"{goals.get('home', 0)}-{goals.get('away', 0)}",
        "statistics": None,
    }
    print(f"[FIXTURE MAP] ID={fixture_id} - PAYLOAD GOALS: home_goals={payload['home_goals']}, away_goals={payload['away_goals']}")
    return payload


async def sync_fixture_statistics(db: Session, fixture_id: int):
    """Fetch and save fixture statistics"""
    data = await fetch_from_api("/fixtures/statistics", {"fixture": fixture_id})

    if not data or not data.get("response"):
        return None

    statistics = data.get("response", [])
    fixture = fixture_crud.get_fixture(db, fixture_id)

    if fixture and statistics:
        return fixture_crud.update_fixture(
            db,
            fixture_id,
            schemas.FixtureUpdate(statistics=statistics),
        )

    return fixture


async def sync_and_save_fixture(db: Session, fixture_id: int):
    """Fetch fixture from API and save to database"""
    try:
        data = await fetch_from_api("/fixtures", {"id": fixture_id})

        if not data or not data.get("response"):
            return None

        fixture_data = data["response"][0]
        return await _save_fixture_from_data(db, fixture_data)
    
    except Exception as e:
        print(f"[FIXTURE SYNC] Error fetching fixture {fixture_id}: {str(e)}")
        raise


async def _save_fixture_from_data(db: Session, fixture_data: dict):
    """Save fixture data to database (extracted from API response)"""
    fixture_raw = fixture_data.get("fixture", {})
    fixture_id = fixture_raw.get("id")
    
    if not fixture_id:
        return None
    
    
    league_raw = fixture_data.get("league", {})
    teams_raw = fixture_data.get("teams", {})

    venue_data = fixture_raw.get("venue", {})
    if venue_data.get("id"):
        stadium_payload = map_stadium_api_data_to_payload(venue_data)
        ensure_stadium_exists(db, venue_data.get("id"), stadium_payload)

    if league_raw.get("id"):
        league_payload = map_league_api_data_to_payload(league_raw)
        ensure_league_exists(db, league_raw.get("id"), league_payload)

    home_team = teams_raw.get("home", {})
    away_team = teams_raw.get("away", {})

    if home_team.get("id"):
        team_payload = map_team_api_data_to_payload(
            home_team, None, home_team.get("id")
        )
        ensure_team_exists(db, schemas.TeamCreate(**team_payload))

    if away_team.get("id"):
        team_payload = map_team_api_data_to_payload(
            away_team, None, away_team.get("id")
        )
        ensure_team_exists(db, schemas.TeamCreate(**team_payload))

    fixture_payload = map_fixture_api_data_to_payload(
        fixture_raw, league_raw, teams_raw, fixture_data.get("goals", {})
    )
    print(f"[FIXTURE SAVE] ID={fixture_id} - BEFORE SCHEMA: home_goals={fixture_payload.get('home_goals')}, away_goals={fixture_payload.get('away_goals')}")
    
    fixture_create_schema = schemas.FixtureCreate(**fixture_payload)
    print(f"[FIXTURE SAVE] ID={fixture_id} - AFTER SCHEMA CREATE: home_goals={fixture_create_schema.home_goals}, away_goals={fixture_create_schema.away_goals}")

    existing_fixture = fixture_crud.get_fixture(db, fixture_id)
    if existing_fixture:
        print(f"[FIXTURE SAVE] ID={fixture_id} - UPDATING (existing): home_goals={fixture_payload.get('home_goals')}, away_goals={fixture_payload.get('away_goals')}")
        result = fixture_crud.update_fixture(
            db, fixture_id, schemas.FixtureUpdate(**fixture_payload)
        )
        print(f"[FIXTURE SAVE] ID={fixture_id} - AFTER UPDATE: home_goals={result.home_goals}, away_goals={result.away_goals}")
        return result
    else:
        print(f"[FIXTURE SAVE] ID={fixture_id} - CREATING (new): home_goals={fixture_payload.get('home_goals')}, away_goals={fixture_payload.get('away_goals')}")
        result = fixture_crud.create_fixture(db, fixture_create_schema)
        print(f"[FIXTURE SAVE] ID={fixture_id} - AFTER CREATE: home_goals={result.home_goals}, away_goals={result.away_goals}")
        return result


async def sync_fixtures_by_league(db: Session, league_id: int, season_id: int):
    """Fetch all fixtures for a league and save directly from list response"""
    params = {"league": league_id, "season": season_id}
    print(f"[FIXTURE SYNC] Fetching fixtures with params: {params}")
    data = await fetch_from_api("/fixtures", params)

    if not data or not data.get("response"):
        print(f"[FIXTURE SYNC] No fixtures returned from API")
        return []

    api_fixtures = data.get("response", [])
    print(f"[FIXTURE SYNC] API returned {len(api_fixtures)} fixtures for league {league_id}, season {season_id}")

    fixtures = []
    for idx, fixture_data in enumerate(api_fixtures):
        fixture_id = fixture_data.get("fixture", {}).get("id")
        
        if fixture_id:
            try:
                saved_fixture = await _save_fixture_from_data(db, fixture_data)
                if saved_fixture:
                    fixtures.append(saved_fixture)
            except Exception as e:
                print(f"[FIXTURE SYNC] Error saving fixture {fixture_id}: {str(e)}")

    print(f"[FIXTURE SYNC] Total saved: {len(fixtures)} fixtures for league {league_id}, season {season_id}")
    return fixtures


async def sync_fixtures_by_team(db: Session, team_id: int, season_id: int = None, league_id: int = None):
    """Fetch all fixtures for a team and filter by league if provided"""
    params = {"team": team_id}
    if season_id:
        params["season"] = season_id

    print(f"[FIXTURE SYNC] Fetching fixtures with params: {params}")
    data = await fetch_from_api("/fixtures", params)

    if not data or not data.get("response"):
        print(f"[FIXTURE SYNC] No fixtures returned from API")
        return []

    api_fixtures = data.get("response", [])
    print(f"[FIXTURE SYNC] API returned {len(api_fixtures)} fixtures for team {team_id}, season {season_id}")
    
    fixtures = []
    for idx, fixture_data in enumerate(api_fixtures):
        fixture_id = fixture_data.get("fixture", {}).get("id")
        fixture_league_id = fixture_data.get("league", {}).get("id")
        
        if league_id and fixture_league_id != league_id:
            continue
        
        print(f"[FIXTURE SYNC]   [{idx+1}/{len(api_fixtures)}] fixture_id={fixture_id}, league_id={fixture_league_id}")
        
        if fixture_id:
            try:
                saved_fixture = await _save_fixture_from_data(db, fixture_data)
                if saved_fixture:
                    fixtures.append(saved_fixture)
                    print(f"[FIXTURE SYNC]     ✓ Saved fixture {fixture_id}")
                else:
                    print(f"[FIXTURE SYNC]     ✗ Failed to save fixture {fixture_id}")
            except Exception as e:
                print(f"[FIXTURE SYNC]     ✗ Error saving fixture {fixture_id}: {str(e)}")
        else:
            print(f"[FIXTURE SYNC]     ✗ No fixture_id found")

    print(f"[FIXTURE SYNC] Total saved: {len(fixtures)} fixtures (filtered by league_id={league_id})")
    return fixtures
