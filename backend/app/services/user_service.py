from sqlalchemy.orm import Session
from app import schemas, crud
from app.core.security import get_password_hash


def create_new_user(db: Session, user_in: schemas.UserCreate):

    user_data = user_in.model_dump()

    password = user_data.pop("password")
    user_data["hashed_password"] = get_password_hash(password)

    return crud.user.create_user(db, user_data)
