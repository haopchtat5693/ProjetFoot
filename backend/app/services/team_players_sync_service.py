from sqlalchemy.orm import Session

from app import crud
from app.services.football_api_client import fetch_from_api
from app.services.contract_service import ensure_contract_exists
from app.services.player_service import ensure_player_exists


def map_player_api_data_to_payload(player_raw: dict, stats_block: dict) -> dict:
    return {
        "id": player_raw.get("id"),
        "name": player_raw.get("name", "Unknown"),
        "position": stats_block.get("games", {}).get("position", "Attacker"),
        "age": player_raw.get("age"),
        "salary": 0,
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
    total_pages = 1

    while current_page <= total_pages:
        data = await fetch_from_api(
            "/players", {"season": season_id, "team": team_id, "page": current_page}
        )

        if not data:
            break

        paging = data.get("paging", {})
        total_pages = paging.get("total", 1)

        response = data.get("response")
        if not response:
            break

        for item in response:
            player_raw = item.get("player", {})
            player_id = player_raw.get("id")
            if not player_id:
                continue

            stats_block = (item.get("statistics") or [{}])[0]
            player_payload = map_player_api_data_to_payload(player_raw, stats_block)
            ensure_player_exists(db, player_payload["id"], player_payload, stats_block)
            ensure_contract_exists(db, player_id, team_id, season_id)

        current_page += 1

    return crud.player_crud.get_players_by_team_and_season(
        db, team_id=team_id, season_id=season_id
    )
