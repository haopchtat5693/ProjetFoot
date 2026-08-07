from sqlalchemy.orm import Session

from app import crud
from app.services.football_api_client import fetch_from_api


def map_player_api_data_to_payload(player_raw: dict, stats_block: dict | None = None):

    return {
        "id": player_raw.get("id"),
        "name": player_raw.get("name", "Unknown"),
        "nationality": player_raw.get("nationality", "Unknown"),
        "position": (stats_block or {}).get("games", {}).get("position", "Unknown"),
        "age": player_raw.get("age") or 0,
        "photo": player_raw.get("photo", None),
    }


def ensure_player_exists(db: Session, player_id: int, player_data: dict):
    player = crud.player_crud.get_player(db, player_id)

    if not player:
        print(f"Création automatique du joueur : {player_data.get('name')}")
        player = crud.player_crud.create_player(db, player_data)
    else:
        player.name = player_data.get("name", player.name)
        player.nationality = player_data.get("nationality", player.nationality)
        player.position = player_data.get("position", player.position)
        player.age = player_data.get("age", player.age)
        player.photo = player_data.get("photo", player.photo)
        db.commit()
        db.refresh(player)

    return player


async def search_players_by_name(
    db: Session,
    name: str,
    limit: int = 100,
):
    search_term = name.strip()
    if not search_term:
        return []

    print(f"Recherche joueur par nom: '{search_term}'")

    players = crud.player_crud.get_players_by_name(db, search_term, limit=limit)
    if players:
        print(f"Résultats trouvés en base: {len(players)}")
        return players

    print("Aucun résultat en base, appel de l'API externe")
    data = await fetch_from_api("/players/profiles", {"search": search_term})
    response = data.get("response") if data else []
    if not response:
        print("Aucun résultat côté API externe")
        return []

    matched_players = []
    for item in response[:limit]:
        player_raw = item.get("player", {})
        stats_block = (item.get("statistics") or [{}])[0]
        player_id = player_raw.get("id")
        if not player_id:
            continue

        payload = map_player_api_data_to_payload(player_raw, stats_block)
        player = ensure_player_exists(db, player_id, payload)

        if player:
            player.name = payload["name"]
            player.nationality = payload["nationality"]
            player.position = payload["position"]
            player.age = payload["age"]
            player.photo = payload["photo"]
            db.commit()
            db.refresh(player)

        if player:
            matched_players.append(player)

    return matched_players
