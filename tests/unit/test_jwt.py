import jwt
import pytest

from app.config.settings import settings
from app.core.exceptions import InvalidTokenError
from app.core.security.jwt import create_access_token, decode_access_token


def test_access_token_contains_subject_and_type():
    token = create_access_token(subject="00000000-0000-0000-0000-000000000001", user_type="patient")

    payload = decode_access_token(token)

    assert payload["sub"] == "00000000-0000-0000-0000-000000000001"
    assert payload["type"] == "access"


def test_invalid_token_is_rejected():
    with pytest.raises(InvalidTokenError):
        decode_access_token("not-a-jwt")


def test_expired_token_is_rejected():
    token = jwt.encode({"sub": "id", "type": "access", "exp": 0}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    with pytest.raises(InvalidTokenError):
        decode_access_token(token)
