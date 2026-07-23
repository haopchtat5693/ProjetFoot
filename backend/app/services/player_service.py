from sqlalchemy.orm import Session
from app import crud


def ensure_player_exists(
    db: Session, player_id: int, player_data: dict, stats_data: dict = None
):
    player = crud.player.get_player(db, player_id)

    if not player:
        print(f"Création automatique du joueur : {player_data.get('name')}")
        player = crud.player.create_player(
            db,
            {
                "id": player_id,
                "name": player_data.get("name", "Unknown"),
                "position": stats_data.get("games", {}).get("position", "Attacker")
                if stats_data
                else "Attacker",
                "age": player_data.get("age"),
                "salary": 0,
            },
        )

    return player
