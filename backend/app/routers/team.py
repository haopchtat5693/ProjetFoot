from app.services.team_sync_service import sync_and_save_team
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    return crud.team.createTeam(db, team)


@router.get("/{team_id}", response_model=schemas.Team)
async def get_team(team_id: int, db: Session = Depends(get_db)):
    try:
        team = await sync_and_save_team(db, team_id=team_id)
    except Exception as e:
        team = crud.team.getTeam(db, team_id)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Team non trouvée en base et échec de synchronisation API : {str(e)}",
            )

    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team introuvable")

    return team



@router.get("/", response_model=list[schemas.Team])
def get_teams(db: Session = Depends(get_db)):
    return crud.team.getTeams(db)


@router.put("/{team_id}", response_model=schemas.Team)
def update_team(team_id: int, team_in: schemas.TeamUpdate, db: Session = Depends(get_db)):
    team = crud.team.getTeam(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return crud.team.updateTeam(db, team_id, team_in)


@router.delete("/{team_id}", response_model=schemas.Team)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    team = crud.team.getTeam(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return crud.team.deleteTeam(db, team_id)