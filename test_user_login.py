import pytest

class TestUserLogin:
    def test_successful_login(self, client, test_user):
        login_data = {
            "email": test_user.email,
            "password": "password123"
        }
        
        response = client.post("/api/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user_role"] == "CUSTOMER"

    def test_invalid_email_login(self, client):
        login_data = {
            "email": "nonexistent@example.com",
            "password": "password123"
        }
        
        response = client.post("/api/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_invalid_password_login(self, client, test_user):
        login_data = {
            "email": test_user.email,
            "password": "wrongpassword"
        }
        
        response = client.post("/api/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_missing_credentials(self, client):
        response = client.post("/api/login", json={})
        assert response.status_code == 422

    def test_empty_email_login(self, client):
        login_data = {
            "email": "",
            "password": "password123"
        }
        
        response = client.post("/api/login", json=login_data)
        assert response.status_code == 422

    def test_empty_password_login(self, client):
        login_data = {
            "email": "test@example.com",
            "password": ""
        }
        
        response = client.post("/api/login", json=login_data)
        assert response.status_code == 422
