import pytest
from auth import get_password_hash, verify_password, create_access_token, verify_token
from datetime import timedelta

class TestPasswordHashing:
    def test_password_hash_generation(self):
        password = "test123"
        hashed = get_password_hash(password)
        assert hashed != password
        assert len(hashed) == 64  # SHA256 produces 64 char hex

    def test_password_verification(self):
        password = "test123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) == True
        assert verify_password("wrong", hashed) == False

class TestJWTTokens:
    def test_token_creation(self):
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_with_expiration(self):
        data = {"sub": "test@example.com"}
        expires = timedelta(minutes=30)
        token = create_access_token(data, expires)
        assert isinstance(token, str)

    def test_token_verification(self):
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        payload = verify_token(token)
        assert payload["sub"] == "test@example.com"

    def test_invalid_token_verification(self):
        with pytest.raises(Exception):
            verify_token("invalid.token.here")
