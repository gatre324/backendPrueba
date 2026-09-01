def register_payload(email: str = "ana@example.com") -> dict[str, str]:
    return {
        "email": email,
        "password": "secure-password-123",
        "first_name": "Ana",
        "last_name": "Pérez",
    }


def test_register_login_me_and_logout(client):
    registered = client.post("/api/v1/auth/register", json=register_payload())
    assert registered.status_code == 201
    body = registered.json()
    assert body["user"]["user_type"] == "patient"
    assert "password_hash" not in body["user"]

    logged_in = client.post(
        "/api/v1/auth/login",
        json={"email": "ANA@example.com", "password": "secure-password-123"},
    )
    assert logged_in.status_code == 200
    token = logged_in.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    me = client.get("/api/v1/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["email"] == "ana@example.com"

    logout = client.post("/api/v1/auth/logout", headers=headers)
    assert logout.status_code == 204


def test_duplicate_email_is_rejected(client):
    assert client.post("/api/v1/auth/register", json=register_payload()).status_code == 201
    duplicate = client.post("/api/v1/auth/register", json=register_payload("ANA@example.com"))

    assert duplicate.status_code == 409
    assert duplicate.json()["code"] == "EMAIL_ALREADY_REGISTERED"


def test_invalid_payload_is_rejected(client):
    response = client.post("/api/v1/auth/register", json={"email": "bad", "password": "short"})

    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"


def test_wrong_credentials_and_missing_token_are_rejected(client):
    client.post("/api/v1/auth/register", json=register_payload())
    wrong_password = client.post(
        "/api/v1/auth/login",
        json={"email": "ana@example.com", "password": "wrong-password"},
    )

    assert wrong_password.status_code == 401
    assert client.get("/api/v1/auth/me").status_code == 401


def test_inactive_user_cannot_login(client):
    client.post("/api/v1/auth/register", json=register_payload())
    from sqlalchemy.orm import Session

    from app.modules.users.infrastructure.models import UserModel

    # The database fixture is injected by the test client override.
    with Session(client.db_engine) as db:
        user = db.query(UserModel).filter_by(email="ana@example.com").one()
        user.is_active = False
        db.commit()

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "ana@example.com", "password": "secure-password-123"},
    )
    assert response.status_code == 401
