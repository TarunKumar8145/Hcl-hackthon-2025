import pytest
from models import Account, User
from auth import get_password_hash

class TestMoneyTransfer:
    @pytest.fixture
    def receiver_user(self, db_session):
        user = User(
            email="receiver@example.com",
            phone="9999999999",
            password_hash=get_password_hash("password123"),
            first_name="Receiver",
            last_name="User",
            date_of_birth="1990-01-01",
            address="Receiver Address"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    @pytest.fixture
    def receiver_account(self, db_session, receiver_user):
        account = Account(
            account_number="SB999999999999",
            user_id=receiver_user.id,
            account_type="SAVINGS",
            balance=5000.00
        )
        db_session.add(account)
        db_session.commit()
        db_session.refresh(account)
        return account

    def test_successful_transfer(self, client, auth_headers, test_account, receiver_account, db_session):
        transfer_data = {
            "from_account": test_account.account_number,
            "to_account": receiver_account.account_number,
            "amount": 1000.0
        }
        
        response = client.post("/api/transfer", data=transfer_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Transfer successful"
        assert data["amount"] == 1000.0
        assert data["new_balance"] == 9000.0  # 10000 - 1000

        # Verify balances in database
        db_session.refresh(test_account)
        db_session.refresh(receiver_account)
        assert float(test_account.balance) == 9000.0
        assert float(receiver_account.balance) == 6000.0

    def test_insufficient_funds_transfer(self, client, auth_headers, test_account, receiver_account):
        transfer_data = {
            "from_account": test_account.account_number,
            "to_account": receiver_account.account_number,
            "amount": 15000.0  # More than balance
        }
        
        response = client.post("/api/transfer", data=transfer_data, headers=auth_headers)
        assert response.status_code == 400
        assert "Insufficient funds" in response.json()["detail"]

    def test_exceed_daily_limit_transfer(self, client, auth_headers, test_account, receiver_account):
        transfer_data = {
            "from_account": test_account.account_number,
            "to_account": receiver_account.account_number,
            "amount": 60000.0  # Exceeds daily limit of 50000
        }
        
        response = client.post("/api/transfer", data=transfer_data, headers=auth_headers)
        assert response.status_code == 400
        assert "exceeds daily limit" in response.json()["detail"]

    def test_transfer_to_nonexistent_account(self, client, auth_headers, test_account):
        transfer_data = {
            "from_account": test_account.account_number,
            "to_account": "SB000000000000",  # Non-existent
            "amount": 1000.0
        }
        
        response = client.post("/api/transfer", data=transfer_data, headers=auth_headers)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_transfer_from_unauthorized_account(self, client, auth_headers, receiver_account):
        transfer_data = {
            "from_account": receiver_account.account_number,  # Not user's account
            "to_account": "SB123456789012",
            "amount": 1000.0
        }
        
        response = client.post("/api/transfer", data=transfer_data, headers=auth_headers)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_transfer_negative_amount(self, client, auth_headers, test_account, receiver_account):
        transfer_data = {
            "from_account": test_account.account_number,
            "to_account": receiver_account.account_number,
            "amount": -500.0
        }
        
        response = client.post("/api/transfer", data=transfer_data, headers=auth_headers)
        assert response.status_code == 400
        assert "greater than 0" in response.json()["detail"]

    def test_transfer_zero_amount(self, client, auth_headers, test_account, receiver_account):
        transfer_data = {
            "from_account": test_account.account_number,
            "to_account": receiver_account.account_number,
            "amount": 0.0
        }
        
        response = client.post("/api/transfer", data=transfer_data, headers=auth_headers)
        assert response.status_code == 400
        assert "greater than 0" in response.json()["detail"]

    def test_transfer_without_auth(self, client, test_account, receiver_account):
        transfer_data = {
            "from_account": test_account.account_number,
            "to_account": receiver_account.account_number,
            "amount": 1000.0
        }
        
        response = client.post("/api/transfer", data=transfer_data)
        assert response.status_code == 401
