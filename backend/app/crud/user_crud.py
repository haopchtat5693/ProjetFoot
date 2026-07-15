from sqlalchemy.orm import Session

import models, schemas

from .base import CRUDBase

user_crud = CRUDBase(models.User)


def get_user(db: Session, user_id: int):
    return user_crud.get(db, user_id)


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return user_crud.get_multi(db, skip=skip, limit=limit)


def create_user(db: Session, user: schemas.UserCreate):
    return user_crud.create(db, user)


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    return user_crud.update(db, user_id, user_update)


def delete_user(db: Session, user_id: int):
    return user_crud.delete(db, user_id)