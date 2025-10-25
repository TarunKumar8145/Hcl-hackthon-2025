import pytest
from models import Account

class TestAccountCreation:
    def test_create_savings_account(self, client, auth_headers):
        account_data = {
            "account_type": "SAVINGS",
            "initial_deposit": 5000.0
        }
        
        response = client.post("/api/accounts/create", data=account_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["account_type"] == "SAVINGS"
        assert data["balance"] == 5000.0
        assert data["account_number"].startswith("SB")
        assert len(data["account_number"]) == 14  # SB + 12 digits

    def test_create_current_account(self, client, auth_headers):
        account_data = {
            "account_type": "CURRENT",
            "initial_deposit": 10000.0
        }
        
        response = client.post("/api/accounts/create", data=account_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["account_type"] == "CURRENT"
        assert data["balance"] == 10000.0

    def test_create_fd_account(self, client, auth_headers):
        account_data = {
            "account_type": "FD",
            "initial_deposit": 50000.0
        }
        
        response = client.post("/api/accounts/create", data=account_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["account_type"] == "FD"
        assert data["balance"] == 50000.0

    def test_create_account_without_auth(self, client):
        account_data = {
            "account_type": "SAVINGS",
            "initial_deposit": 5000.0
        }
        
        response = client.post("/api/accounts/create", data=account_data)
        assert response.status_code == 401

    def test_create_account_invalid_type(self, client, auth_headers):
        account_data = {
            "account_type": "INVALID",
            "initial_deposit": 5000.0
        }
        
        response = client.post("/api/accounts/create", data=account_data, headers=auth_headers)
        assert response.status_code == 422

    def test_create_account_negative_deposit(self, client, auth_headers):
        account_data = {
            "account_type": "SAVINGS",
            "initial_deposit": -1000.0
        }
        
        response = client.post("/api/accounts/create", data=account_data, headers=auth_headers)
        assert response.status_code == 400

    def test_account_number_uniqueness(self, client, auth_headers, db_session):
        # Create multiple accounts and verify unique account numbers
        account_numbers = set()
        
        for i in range(5):
            account_data = {
                "account_type": "SAVINGS",
                "initial_deposit": 1000.0
            }
            response = client.post("/api/accounts/create", data=account_data, headers=auth_headers)
            assert response.status_code == 200
            account_number = response.json()["account_number"]
            assert account_number not in account_numbers
            account_numbers.add(account_number)
