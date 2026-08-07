from app import crud
from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from app.models import User
from app.core.constants import ADMIN, MANAGER, ALGORITHM
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from jose import JWTError, jwt

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(db=Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": True, "require_exp": True},
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    token_in_db = crud.auth_token_crud.get_token_by_value(db, token_value=token)
    if token_in_db is None:
        raise credentials_exception

    token_expiration = token_in_db.expires_at
    if token_expiration is None:
        raise credentials_exception

    if token_expiration.tzinfo is None:
        token_expiration = token_expiration.replace(tzinfo=timezone.utc)

    if token_expiration <= datetime.now(timezone.utc):
        crud.auth_token_crud.delete_token(db, token_id=token_in_db.id)
        raise credentials_exception

    user = crud.user_crud.get_user_by_username(db, username=username)

    if user is None:
        raise credentials_exception

    return user


async def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé : Droits administrateur requis.",
        )
    return current_user


async def get_current_manager(current_user: User = Depends(get_current_user)):
    if current_user.role not in [ADMIN, MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé : Droits de manager requis.",
        )
    return current_user


async def get_owner_or_admin(
    user_id: int, current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id and current_user.role != ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tu ne peux pas modifier/supprimer les données d'un autre utilisateur.",
        )
    return current_user
