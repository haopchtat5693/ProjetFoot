from sqlalchemy.orm import Session

import models, schemas

from .base import CRUDBase


auth_token_crud = CRUDBase(models.Token)


def getToken(db: Session, token_id: int):
    return auth_token_crud.get(db, token_id)


def getTokens(db: Session, skip: int = 0, limit: int = 100):
    return auth_token_crud.get_multi(db, skip=skip, limit=limit)


def createToken(db: Session, token: schemas.TokenCreate):
    return auth_token_crud.create(db, token)


def updateToken(db: Session, token_id: int, token_update: schemas.TokenUpdate):
    return auth_token_crud.update(db, token_id, token_update)


def deleteToken(db: Session, token_id: int):
    return auth_token_crud.delete(db, token_id)