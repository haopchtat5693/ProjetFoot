from sqlalchemy.orm import Session
from app import crud

def get_season_stats_for_player(db: Session, player_id: int, season_id: int):
    match_stats_list = crud.player_stats.get_stats_by_player_and_season(db, player_id, season_id)
    
    if not match_stats_list:
        return None
    
    total_goals = sum(s.goals for s in match_stats_list)
    total_assists = sum(s.assists for s in match_stats_list)
    average_goal= total_goals / len(match_stats_list) if match_stats_list else 0
    average_assist= total_assists / len(match_stats_list) if match_stats_list else 0
    total_yellow_cards = sum(s.yellow_cards for s in match_stats_list)
    total_red_cards = sum(s.red_cards for s in match_stats_list)
    
    return {
        "player_id": player_id,
        "total_goals": total_goals,
        "total_assists": total_assists,
        "average_goal": average_goal,
        "average_assist": average_assist,
        "total_yellow_cards": total_yellow_cards,
        "total_red_cards": total_red_cards,
        "details": match_stats_list
    }