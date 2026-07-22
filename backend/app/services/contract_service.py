from sqlalchemy.orm import Session

from app import crud, models, schemas


def ensure_contract_exists(db: Session, player_id: int, team_id: int, season_id: int):
    contract = (
        db.query(models.Contract)
        .filter(
            models.Contract.player_id == player_id,
            models.Contract.team_id == team_id,
            models.Contract.season_id == season_id,
        )
        .first()
    )

    if contract:
        return contract

    return crud.contract.createContract(
        db,
        schemas.ContractCreate(
            player_id=player_id,
            team_id=team_id,
            season_id=season_id,
        ),
    )
