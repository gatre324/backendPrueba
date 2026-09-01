from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.core.exceptions import InvalidTokenError
from app.core.security.jwt import decode_access_token
from app.modules.users.infrastructure.repositories import SqlAlchemyUserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        payload = decode_access_token(token)
        user_id = UUID(payload["sub"])
    except (InvalidTokenError, ValueError, KeyError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_TOKEN", "message": "El token no es válido o ha expirado"},
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    user = SqlAlchemyUserRepository(db).get_by_id(user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "UNAUTHORIZED", "message": "No se pudo autenticar al usuario"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


CurrentUser = Annotated[object, Depends(get_current_user)]
