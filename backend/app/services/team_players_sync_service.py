from sqlalchemy.orm import Session

from app import crud
from app.services.football_api_client import fetch_from_api
from app.services.contract_service import ensure_contract_exists
from app.services.player_service import (
    ensure_player_exists,
    map_player_api_data_to_payload,
)


def map_player_api_data_to_payload(player_raw: dict, stats_block: dict) -> dict:
    return {
        "id": player_raw.get("id"),
        "name": player_raw.get("name", "Unknown"),
        "nationality": player_raw.get("nationality", "Unknown"),
        "position": stats_block.get("games", {}).get("position", "Attacker"),
        "age": player_raw.get("age"),
        "photo": player_raw.get("photo", None),
    }


async def sync_and_get_team_players_for_season(
    db: Session, team_id: int, season_id: int
):
    players = crud.player_crud.get_players_by_team_and_season(
        db, team_id=team_id, season_id=season_id
    )

    if players:
        return players

    current_page = 1
    max_free_pages = 3  # LIMITED TO 3 PAGES DUE TO API LIMITATIONS

    while current_page <= max_free_pages:
        data = await fetch_from_api(
            "/players", {"season": season_id, "team": team_id, "page": current_page}
        )

        if not data:
            break

        response = data.get("response")
        if not response:
            break

        for player in response:
            player_raw = player.get("player", {})
            player_id = player_raw.get("id")
            if not player_id:
                continue

            stats_block = (player.get("statistics") or [{}])[0]
            player_payload = map_player_api_data_to_payload(player_raw, stats_block)
            ensure_player_exists(db, player_payload["id"], player_payload)
            ensure_contract_exists(db, player_id, team_id, season_id)

        current_page += 1

    return crud.player_crud.get_players_by_team_and_season(
        db, team_id=team_id, season_id=season_id
    )