from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import Optional, List
from enum import Enum

class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    AUDITOR = "auditor"

class KYCStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class UserRegistration(BaseModel):
    email: str
    phone: str
    password: str
    first_name: str
    last_name: str
    date_of_birth: date
    address: str
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('Invalid email format')
        return v
    
    @validator('phone')
    def validate_phone(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError('Phone number must be 10 digits')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class KYCDocumentCreate(BaseModel):
    document_type: str
    document_number: str
    
    @validator('document_type')
    def validate_document_type(cls, v):
        allowed_types = ['aadhar', 'pan', 'passport', 'driving_license']
        if v.lower() not in allowed_types:
            raise ValueError(f'Document type must be one of: {", ".join(allowed_types)}')
        return v.lower()

class UserResponse(BaseModel):
    id: int
    email: str
    phone: str
    first_name: str
    last_name: str
    date_of_birth: date
    address: str
    role: UserRole
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class KYCDocumentResponse(BaseModel):
    id: int
    document_type: str
    document_number: str
    status: KYCStatus
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
