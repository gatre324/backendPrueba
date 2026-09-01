from app.core.security.passwords import hash_password, verify_password


def test_password_is_hashed_and_verifiable():
    plain_password = "correct-horse-battery-staple"
    stored_hash = hash_password(plain_password)

    assert stored_hash != plain_password
    assert verify_password(plain_password, stored_hash)
    assert not verify_password("wrong-password", stored_hash)
