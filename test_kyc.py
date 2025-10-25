import pytest
import io
from models import KYCDocument, User
from auth import get_password_hash, create_access_token

class TestKYCUpload:
    def test_successful_document_upload(self, client, auth_headers):
        # Create a fake PDF file
        file_content = b"fake pdf content"
        file_data = {
            "document_file": ("test_document.pdf", io.BytesIO(file_content), "application/pdf")
        }
        form_data = {
            "document_type": "aadhaar",
            "document_number": "123456789012"
        }
        
        response = client.post("/api/kyc/upload", data=form_data, files=file_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "uploaded successfully" in data["message"]
        assert "document_id" in data

    def test_upload_invalid_file_type(self, client, auth_headers):
        file_content = b"fake text content"
        file_data = {
            "document_file": ("test_document.txt", io.BytesIO(file_content), "text/plain")
        }
        form_data = {
            "document_type": "aadhaar",
            "document_number": "123456789012"
        }
        
        response = client.post("/api/kyc/upload", data=form_data, files=file_data, headers=auth_headers)
        assert response.status_code == 400
        assert "Only JPG, PNG, and PDF files are allowed" in response.json()["detail"]

    def test_upload_without_auth(self, client):
        file_content = b"fake pdf content"
        file_data = {
            "document_file": ("test_document.pdf", io.BytesIO(file_content), "application/pdf")
        }
        form_data = {
            "document_type": "aadhaar",
            "document_number": "123456789012"
        }
        
        response = client.post("/api/kyc/upload", data=form_data, files=file_data)
        assert response.status_code == 401

    def test_upload_missing_document_type(self, client, auth_headers):
        file_content = b"fake pdf content"
        file_data = {
            "document_file": ("test_document.pdf", io.BytesIO(file_content), "application/pdf")
        }
        form_data = {
            "document_number": "123456789012"
            # Missing document_type
        }
        
        response = client.post("/api/kyc/upload", data=form_data, files=file_data, headers=auth_headers)
        assert response.status_code == 422

    def test_upload_missing_document_number(self, client, auth_headers):
        file_content = b"fake pdf content"
        file_data = {
            "document_file": ("test_document.pdf", io.BytesIO(file_content), "application/pdf")
        }
        form_data = {
            "document_type": "aadhaar"
            # Missing document_number
        }
        
        response = client.post("/api/kyc/upload", data=form_data, files=file_data, headers=auth_headers)
        assert response.status_code == 422

class TestKYCStatus:
    @pytest.fixture
    def kyc_document(self, db_session, test_user):
        kyc_doc = KYCDocument(
            user_id=test_user.id,
            document_type="aadhaar",
            document_number="123456789012",
            document_path="uploads/test_doc.pdf",
            status="PENDING"
        )
        db_session.add(kyc_doc)
        db_session.commit()
        db_session.refresh(kyc_doc)
        return kyc_doc

    def test_get_kyc_status(self, client, auth_headers, kyc_document):
        response = client.get("/api/kyc/status", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["document_type"] == "aadhaar"
        assert data[0]["status"] == "PENDING"

    def test_get_kyc_status_without_auth(self, client):
        response = client.get("/api/kyc/status")
        assert response.status_code == 401

class TestKYCAdmin:
    @pytest.fixture
    def admin_user(self, db_session):
        admin = User(
            email="admin@example.com",
            phone="1111111111",
            password_hash=get_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            date_of_birth="1980-01-01",
            address="Admin Address",
            role="ADMIN"
        )
        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)
        return admin

    @pytest.fixture
    def admin_headers(self, admin_user):
        token = create_access_token(data={"sub": admin_user.email})
        return {"Authorization": f"Bearer {token}"}

    def test_admin_approve_kyc(self, client, admin_headers, kyc_document):
        response = client.put(f"/api/admin/kyc/{kyc_document.id}/approve", headers=admin_headers)
        assert response.status_code == 200
        assert "approved" in response.json()["message"]

    def test_admin_reject_kyc(self, client, admin_headers, kyc_document):
        response = client.put(f"/api/admin/kyc/{kyc_document.id}/reject", headers=admin_headers)
        assert response.status_code == 200
        assert "rejected" in response.json()["message"]

    def test_non_admin_approve_kyc(self, client, auth_headers, kyc_document):
        response = client.put(f"/api/admin/kyc/{kyc_document.id}/approve", headers=auth_headers)
        assert response.status_code == 403

    def test_approve_nonexistent_kyc(self, client, admin_headers):
        response = client.put("/api/admin/kyc/99999/approve", headers=admin_headers)
        assert response.status_code == 404
