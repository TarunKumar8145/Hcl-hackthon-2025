import pytest
from models import User

class TestUserRegistration:
    def test_successful_registration(self, client):
        user_data = {
            "email": "newuser@example.com",
            "phone": "9876543210",
            "password": "password123",
            "first_name": "New",
            "last_name": "User",
            "date_of_birth": "1995-05-15",
            "address": "New Address"
        }
        
        response = client.post("/api/register", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["first_name"] == user_data["first_name"]
        assert "password" not in data

    def test_duplicate_email_registration(self, client, test_user):
        user_data = {
            "email": test_user.email,  # Duplicate email
            "phone": "9999999999",
            "password": "password123",
            "first_name": "Duplicate",
            "last_name": "User",
            "date_of_birth": "1995-05-15",
            "address": "Duplicate Address"
        }
        
        response = client.post("/api/register", json=user_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_duplicate_phone_registration(self, client, test_user):
        user_data = {
            "email": "different@example.com",
            "phone": test_user.phone,  # Duplicate phone
            "password": "password123",
            "first_name": "Duplicate",
            "last_name": "User",
            "date_of_birth": "1995-05-15",
            "address": "Duplicate Address"
        }
        
        response = client.post("/api/register", json=user_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_invalid_email_format(self, client):
        user_data = {
            "email": "invalid-email",  # Invalid format
            "phone": "9876543210",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
            "date_of_birth": "1995-05-15",
            "address": "Test Address"
        }
        
        response = client.post("/api/register", json=user_data)
        assert response.status_code == 422  # Validation error

    def test_missing_required_fields(self, client):
        user_data = {
            "email": "test@example.com",
            # Missing required fields
        }
        
        response = client.post("/api/register", json=user_data)
        assert response.status_code == 422
