# app/services/player_service.py
from sqlalchemy.orm import Session
from app import models

def ensure_player_exists(db: Session, player_id: int, player_data: dict, stats_data: dict = None):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    
    if not player:
        print(f"Création automatique du joueur : {player_data.get('name')}")
        player = models.Player(
            id=player_id,
            name=player_data.get('name', 'Unknown'),
            position=stats_data.get('games', {}).get('position', 'Attacker') if stats_data else 'Attacker',
            age=player_data.get('age'),
            salary=0,
            main_foot=None,
            team_id=None
        )
        db.add(player)
        db.commit()
        db.refresh(player)
        
    return player