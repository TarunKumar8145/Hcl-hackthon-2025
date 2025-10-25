# SmartBank - Modular Banking Backend System

## 🎯 Project Overview

SmartBank is a secure, scalable backend system that supports core banking operations including user registration, KYC verification, account management, transactions, and fraud detection. This implementation focuses on **Phase 1: User Registration & KYC** with a complete web interface.

## ✅ Implemented Features

### Phase 1: User Registration & KYC ✅
- **User Registration**: Complete registration form with validation
- **JWT Authentication**: Secure login/logout system
- **KYC Document Upload**: Multi-document upload with status tracking
- **Document Verification**: Admin workflow for document approval
- **Responsive Web UI**: Bootstrap-based modern interface
- **MySQL Integration**: Full database persistence

### Security Features ✅
- Password hashing with bcrypt
- JWT token authentication
- File upload validation (JPG, PNG, PDF only)
- SQL injection prevention
- Input sanitization and validation

## 🏗️ Architecture

### Backend Stack
- **Framework**: FastAPI (Python)
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **File Handling**: FastAPI multipart

### Frontend Stack
- **UI Framework**: Bootstrap 5
- **JavaScript**: Vanilla JS with Fetch API
- **Templates**: Jinja2
- **Icons**: Font Awesome

## 📊 Database Schema

### Core Tables Implemented:
1. **users** - User profiles and authentication
2. **kyc_documents** - Document storage and verification status
3. **accounts** - Ready for Phase 2 (account management)
4. **transactions** - Ready for Phase 2 (money transfers)
5. **audit_logs** - Ready for Phase 2 (system monitoring)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL Server
- Linux/WSL environment

### Installation & Setup

1. **Navigate to project directory:**
   ```bash
   cd /mnt/c/Users/User/OneDrive/Desktop/HCL-HACKTHON1/smartbank
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Start the application:**
   ```bash
   ./start_app.sh
   ```
   
   Or manually:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Access the application:**
   - Open browser: http://localhost:8000
   - Home page with navigation
   - Registration: http://localhost:8000/register
   - Login: http://localhost:8000/login
   - Dashboard: http://localhost:8000/dashboard
   - KYC: http://localhost:8000/kyc

## 🌐 API Endpoints

### Authentication APIs
- `POST /api/register` - User registration
- `POST /api/login` - User login (returns JWT token)

### KYC Management APIs
- `POST /api/kyc/upload` - Upload KYC document (requires auth)
- `GET /api/kyc/status` - Get document verification status (requires auth)

### Web Pages
- `/` - Home page
- `/register` - Registration form
- `/login` - Login form
- `/dashboard` - User dashboard
- `/kyc` - KYC verification page

## 📱 User Journey

### 1. Registration Flow
1. User visits `/register`
2. Fills registration form with:
   - Personal details (name, email, phone)
   - Date of birth and address
   - Secure password (8+ characters)
3. System validates and creates account
4. Success modal redirects to login

### 2. Login & Dashboard
1. User logs in at `/login`
2. Receives JWT token (stored in localStorage)
3. Redirected to `/dashboard`
4. Dashboard shows:
   - KYC status
   - Account summary (placeholder for Phase 2)
   - Quick actions menu

### 3. KYC Verification
1. User clicks "Complete KYC" from dashboard
2. Navigates to `/kyc` page
3. Uploads documents:
   - Document type (Aadhar, PAN, Passport, DL)
   - Document number
   - File upload (JPG/PNG/PDF)
4. Real-time status tracking
5. Document status updates (Pending → Under Review → Approved/Rejected)

## 🔒 Security Implementation

### Authentication
- JWT tokens with 30-minute expiration
- Secure password hashing (bcrypt)
- Protected routes requiring valid tokens

### File Security
- File type validation (images and PDFs only)
- Secure file storage in `/uploads` directory
- File size limits and naming conventions

### Data Validation
- Pydantic models for request validation
- SQL injection prevention via ORM
- Input sanitization for all user data

## 📁 Project Structure

```
smartbank/
├── main.py              # FastAPI application
├── models.py            # Database models
├── schemas.py           # Pydantic schemas
├── auth.py              # Authentication utilities
├── database.py          # Database configuration
├── setup_db.py          # Database setup script
├── requirements.txt     # Python dependencies
├── start_app.sh         # Startup script
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   └── kyc.html
├── uploads/             # KYC document storage
├── venv/                # Virtual environment
└── static/              # Static files (CSS, JS, images)
```

## 🔄 Next Phase Implementation

The system is architected for easy extension:

### Phase 2: Account Management
- Account creation (Savings, Current, FD)
- Balance management
- Account number generation
- Account status tracking

### Phase 3: Money Transfer
- Internal transfers between accounts
- External bank transfers
- Daily limit enforcement
- Transaction history

### Phase 4: Loan Processing
- Loan application workflow
- Credit scoring integration
- Approval process
- EMI calculations

### Phase 5: Fraud Detection
- Transaction pattern analysis
- Risk scoring algorithms
- Real-time fraud alerts
- Machine learning integration

## 🛠️ Development Notes

### Database Configuration
- MySQL connection: `mysql+pymysql://root:root@localhost/smartbank`
- Auto-generated tables via SQLAlchemy
- Enum support for status fields

### File Upload Handling
- Secure multipart form handling
- File validation and storage
- Path sanitization

### Frontend Integration
- RESTful API design
- JSON request/response format
- Error handling with user-friendly messages

## 🎯 Success Metrics

### Phase 1 Achievements:
✅ Complete user registration system
✅ Secure authentication with JWT
✅ KYC document upload and tracking
✅ Responsive web interface
✅ MySQL database integration
✅ Security best practices implemented
✅ Modular architecture for future expansion

## 🚀 Demo Instructions

1. **Start the application** using the startup script
2. **Register a new user** with valid details
3. **Login** with the created credentials
4. **Complete KYC** by uploading documents
5. **View dashboard** to see system status
6. **Test API endpoints** using the web interface

The system is now ready for Phase 2 implementation (Account Management) and can be easily extended with additional banking features.

---

**Built with ❤️ for HCL Hackathon**
**Tech Stack**: FastAPI + MySQL + Bootstrap + JWT
