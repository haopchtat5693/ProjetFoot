from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


contract_crud = CRUDBase(models.Contract)


def get_contract(db: Session, contract_id: int):
    return contract_crud.get(db, contract_id)


def get_contracts(db: Session, skip: int = 0, limit: int = 100):
    return contract_crud.get_multi(db, skip=skip, limit=limit)


def create_contract(db: Session, contract: schemas.ContractCreate):
    return contract_crud.create(db, contract)


def update_contract(
    db: Session, contract_id: int, contract_update: schemas.ContractUpdate
):
    return contract_crud.update(db, contract_id, contract_update)


def delete_contract(db: Session, contract_id: int):
    return contract_crud.delete(db, contract_id)
