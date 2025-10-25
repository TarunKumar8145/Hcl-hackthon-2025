# SmartBank - Modular Banking Backend System

A secure, scalable backend system that supports core banking operations including user registration, KYC verification, account management, transactions, and fraud detection.

## Features Implemented

### Phase 1: User Registration & KYC
- ✅ User Registration with validation
- ✅ JWT Authentication
- ✅ KYC Document Upload
- ✅ Document Status Tracking
- ✅ Responsive Web UI
- ✅ MySQL Database Integration

## Tech Stack

- **Backend**: FastAPI
- **Database**: MySQL
- **Authentication**: JWT (JSON Web Tokens)
- **Frontend**: HTML, Bootstrap, JavaScript
- **ORM**: SQLAlchemy
- **File Upload**: FastAPI File handling

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server (running on localhost)
- MySQL credentials: username=root, password=root

### 1. Install Dependencies
```bash
cd smartbank
pip install -r requirements.txt
```

### 2. Setup Database
```bash
python setup_db.py
```

### 3. Run the Application
```bash
python main.py
```

The application will be available at: http://localhost:8000

## API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login

### KYC Management
- `POST /api/kyc/upload` - Upload KYC document
- `GET /api/kyc/status` - Get KYC document status

### Web Pages
- `/` - Home page
- `/register` - User registration form
- `/login` - Login form
- `/dashboard` - User dashboard
- `/kyc` - KYC verification page

## Database Models

### Users Table
- User profile information
- Authentication credentials
- Role-based access control

### KYC Documents Table
- Document type and number
- File path storage
- Verification status
- Approval workflow

### Accounts Table (Ready for Phase 2)
- Account management
- Balance tracking
- Account types (Savings, Current, FD)

### Transactions Table (Ready for Phase 2)
- Transaction history
- Transfer operations
- Audit trail

### Audit Logs Table (Ready for Phase 2)
- System activity logging
- Security monitoring
- Compliance tracking

## Usage

1. **Register**: Create a new user account at `/register`
2. **Login**: Access your account at `/login`
3. **Dashboard**: View account overview at `/dashboard`
4. **KYC**: Complete document verification at `/kyc`

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- File upload validation
- SQL injection prevention
- Input sanitization

## Next Phase Implementation

The system is designed to easily extend with:
- Account creation and management
- Money transfer operations
- Loan processing
- Fraud detection
- Admin dashboard
- Audit reporting

## File Structure
```
smartbank/
├── main.py              # FastAPI application
├── models.py            # Database models
├── schemas.py           # Pydantic schemas
├── auth.py              # Authentication utilities
├── database.py          # Database configuration
├── setup_db.py          # Database setup script
├── requirements.txt     # Python dependencies
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   └── kyc.html
├── uploads/             # KYC document storage
└── static/              # Static files
```
