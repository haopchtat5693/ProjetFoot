from sqlalchemy.orm import Session
from app import crud, schemas
from app import models


def ensure_team_exists(db: Session, team_data: schemas.TeamCreate):
    team = crud.team_crud.get_team(db, team_data.id)

    if not team:
        return crud.team_crud.create_team(
            db,
            {
                "id": team_data.id,
                "name": team_data.name,
                "city": team_data.city,
                "logo": team_data.logo,
                "coach_id": team_data.coach_id,
                "stadium_id": team_data.stadium_id,
            },
        )

    team.name = team_data.name
    team.logo = team_data.logo

    if team_data.city and team_data.city != "Unknown":
        team.city = team_data.city
    if team_data.coach_id:
        team.coach_id = team_data.coach_id
    if team_data.stadium_id:
        team.stadium_id = team_data.stadium_id

    db.commit()
    db.refresh(team)
    return team
