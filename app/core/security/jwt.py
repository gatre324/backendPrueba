from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.config.settings import settings
from app.core.exceptions import InvalidTokenError


def create_access_token(*, subject: str, user_type: str) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=settings.access_token_expire_minutes)
    payload: dict[str, Any] = {
        "sub": subject,
        "user_type": user_type,
        "type": "access",
        "iat": now,
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as exc:
        raise InvalidTokenError() from exc
    if payload.get("type") != "access" or not payload.get("sub"):
        raise InvalidTokenError()
    return payload
