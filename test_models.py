import pytest
from datetime import datetime, date
from models import User, Account, KYCDocument
from auth import get_password_hash

class TestUserModel:
    def test_create_user(self, db_session):
        user = User(
            email="model_test@example.com",
            phone="5555555555",
            password_hash=get_password_hash("password123"),
            first_name="Model",
            last_name="Test",
            date_of_birth=date(1990, 1, 1),
            address="Model Test Address"
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        assert user.id is not None
        assert user.email == "model_test@example.com"
        assert user.role.value == "CUSTOMER"  # Default role
        assert user.is_active == True
        assert user.created_at is not None

    def test_user_unique_email(self, db_session, test_user):
        # Try to create user with same email
        duplicate_user = User(
            email=test_user.email,  # Same email
            phone="6666666666",
            password_hash=get_password_hash("password123"),
            first_name="Duplicate",
            last_name="User",
            date_of_birth=date(1990, 1, 1),
            address="Duplicate Address"
        )
        
        db_session.add(duplicate_user)
        with pytest.raises(Exception):  # Should raise integrity error
            db_session.commit()

    def test_user_unique_phone(self, db_session, test_user):
        # Try to create user with same phone
        duplicate_user = User(
            email="different@example.com",
            phone=test_user.phone,  # Same phone
            password_hash=get_password_hash("password123"),
            first_name="Duplicate",
            last_name="User",
            date_of_birth=date(1990, 1, 1),
            address="Duplicate Address"
        )
        
        db_session.add(duplicate_user)
        with pytest.raises(Exception):  # Should raise integrity error
            db_session.commit()

class TestAccountModel:
    def test_create_account(self, db_session, test_user):
        account = Account(
            account_number="SB111111111111",
            user_id=test_user.id,
            account_type="SAVINGS",
            balance=5000.00,
            daily_limit=50000.00
        )
        
        db_session.add(account)
        db_session.commit()
        db_session.refresh(account)
        
        assert account.id is not None
        assert account.account_number == "SB111111111111"
        assert account.user_id == test_user.id
        assert float(account.balance) == 5000.00
        assert account.is_active == True

    def test_account_unique_number(self, db_session, test_user):
        # Create first account
        account1 = Account(
            account_number="SB222222222222",
            user_id=test_user.id,
            account_type="SAVINGS",
            balance=1000.00
        )
        db_session.add(account1)
        db_session.commit()
        
        # Try to create account with same number
        account2 = Account(
            account_number="SB222222222222",  # Same number
            user_id=test_user.id,
            account_type="CURRENT",
            balance=2000.00
        )
        
        db_session.add(account2)
        with pytest.raises(Exception):  # Should raise integrity error
            db_session.commit()

    def test_account_foreign_key(self, db_session):
        # Try to create account with non-existent user_id
        account = Account(
            account_number="SB333333333333",
            user_id=99999,  # Non-existent user
            account_type="SAVINGS",
            balance=1000.00
        )
        
        db_session.add(account)
        with pytest.raises(Exception):  # Should raise foreign key error
            db_session.commit()

class TestKYCDocumentModel:
    def test_create_kyc_document(self, db_session, test_user):
        kyc_doc = KYCDocument(
            user_id=test_user.id,
            document_type="aadhaar",
            document_number="123456789012",
            document_path="uploads/test_kyc.pdf"
        )
        
        db_session.add(kyc_doc)
        db_session.commit()
        db_session.refresh(kyc_doc)
        
        assert kyc_doc.id is not None
        assert kyc_doc.user_id == test_user.id
        assert kyc_doc.document_type == "aadhaar"
        assert kyc_doc.status.value == "PENDING"  # Default status
        assert kyc_doc.created_at is not None

    def test_kyc_document_foreign_key(self, db_session):
        # Try to create KYC document with non-existent user_id
        kyc_doc = KYCDocument(
            user_id=99999,  # Non-existent user
            document_type="pan",
            document_number="ABCDE1234F",
            document_path="uploads/test_pan.pdf"
        )
        
        db_session.add(kyc_doc)
        with pytest.raises(Exception):  # Should raise foreign key error
            db_session.commit()

class TestModelRelationships:
    def test_user_accounts_relationship(self, db_session, test_user):
        # Create multiple accounts for user
        account1 = Account(
            account_number="SB444444444444",
            user_id=test_user.id,
            account_type="SAVINGS",
            balance=1000.00
        )
        account2 = Account(
            account_number="SB555555555555",
            user_id=test_user.id,
            account_type="CURRENT",
            balance=2000.00
        )
        
        db_session.add_all([account1, account2])
        db_session.commit()
        
        # Test relationship
        db_session.refresh(test_user)
        assert len(test_user.accounts) == 2
        account_numbers = [acc.account_number for acc in test_user.accounts]
        assert "SB444444444444" in account_numbers
        assert "SB555555555555" in account_numbers

    def test_user_kyc_documents_relationship(self, db_session, test_user):
        # Create multiple KYC documents for user
        kyc1 = KYCDocument(
            user_id=test_user.id,
            document_type="aadhaar",
            document_number="123456789012",
            document_path="uploads/aadhaar.pdf"
        )
        kyc2 = KYCDocument(
            user_id=test_user.id,
            document_type="pan",
            document_number="ABCDE1234F",
            document_path="uploads/pan.pdf"
        )
        
        db_session.add_all([kyc1, kyc2])
        db_session.commit()
        
        # Test relationship
        db_session.refresh(test_user)
        assert len(test_user.kyc_documents) == 2
        doc_types = [doc.document_type for doc in test_user.kyc_documents]
        assert "aadhaar" in doc_types
        assert "pan" in doc_types
