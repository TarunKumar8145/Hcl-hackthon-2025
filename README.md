# SmartBank - Digital Banking System

A comprehensive digital banking backend system built with FastAPI, MySQL, and modern web technologies for HCL Hackathon 2025.

## 🏦 Features

### Core Banking Features
- **User Registration & Authentication** - JWT-based secure authentication
- **KYC Verification** - Document upload and admin approval system
- **Account Management** - Multiple account types (Savings, Current, FD)
- **Money Transfer** - Secure fund transfers with balance validation
- **Role-Based Access** - Customer and Admin interfaces
- **Account Generation** - Auto-generated unique account numbers

### Security Features
- SHA256 password hashing
- JWT token authentication
- Role-based authorization
- Input validation and sanitization
- File upload security

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **MySQL** - Primary database
- **PyMySQL** - MySQL connector
- **Pydantic** - Data validation

### Frontend
- **HTML5/CSS3** - User interface
- **Bootstrap 5** - Responsive design
- **JavaScript** - Client-side interactions

### Testing
- **pytest** - Unit testing framework
- **pytest-cov** - Coverage reporting
- **httpx** - HTTP client for testing

## 📁 Project Structure

```
smartbank/
├── main.py              # FastAPI application
├── models.py            # Database models
├── schemas.py           # Pydantic schemas
├── auth.py              # Authentication logic
├── database.py          # Database connection
├── setup_db.py          # Database setup
├── templates/           # HTML templates
│   ├── base.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── kyc.html
│   ├── create_account.html
│   ├── transfer.html
│   └── admin.html
├── uploads/             # KYC document storage
├── tests/               # Unit tests
├── requirements.txt     # Dependencies
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server
- Git

### 1. Clone Repository
```bash
git clone https://github.com/TarunKumar8145/Hcl-hackthon-2025.git
cd Hcl-hackthon-2025
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Start MySQL service
sudo systemctl start mysql

# Create database
mysql -u root -p
CREATE DATABASE smartbank;
exit

# Run database setup
python setup_db.py
```

### 5. Create Uploads Directory
```bash
mkdir uploads
```

### 6. Run Application
```bash
uvicorn main:app --reload
```

Access the application at: `http://localhost:8000`

## 📊 API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login

### KYC Management
- `POST /api/kyc/upload` - Upload KYC document
- `GET /api/kyc/status` - Get KYC status
- `PUT /api/admin/kyc/{id}/approve` - Admin approve KYC
- `PUT /api/admin/kyc/{id}/reject` - Admin reject KYC

### Account Management
- `POST /api/accounts/create` - Create new account
- `GET /api/accounts` - Get user accounts

### Money Transfer
- `POST /api/transfer` - Transfer money between accounts

### Admin
- `GET /api/admin/kyc/pending` - Get pending KYC documents
- `POST /api/admin/create` - Create admin account

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest test_auth.py
```

### Test Coverage
- Authentication and authorization
- User registration and login
- Account creation and management
- Money transfer functionality
- KYC document handling
- Database model validation

## 🔐 Security Features

### Authentication
- JWT tokens with expiration
- SHA256 password hashing
- Bearer token authentication

### Authorization
- Role-based access control
- Protected admin endpoints
- User-specific data access

### Data Validation
- Pydantic schema validation
- File type restrictions
- SQL injection prevention

## 💾 Database Schema

### Tables
- **users** - User profiles and authentication
- **accounts** - Banking accounts and balances
- **kyc_documents** - KYC verification documents
- **transactions** - Transaction history (optional)
- **audit_logs** - System audit trail (optional)

## 🌐 Web Interface

### Customer Portal
- User registration and login
- Dashboard with account overview
- KYC document upload
- Account creation
- Money transfer

### Admin Portal
- KYC document approval
- User management
- System administration

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=mysql+pymysql://root:root@localhost/smartbank

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10MB
```

## 📈 Performance Features

- Database connection pooling
- Async endpoint support
- Efficient query optimization
- File upload handling

## 🚦 API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- **Developer**: Tarun Kumar
- **Project**: HCL Hackathon 2025
- **Technology**: Full Stack Banking System

## 🎯 Future Enhancements

- Real-time notifications
- Mobile app integration
- Advanced fraud detection
- Multi-factor authentication
- Account statements generation
- Transaction analytics
- Microservices architecture

## 📞 Support

For support and queries:
- GitHub Issues: [Create Issue](https://github.com/TarunKumar8145/Hcl-hackthon-2025/issues)
- Email: [Contact Developer]

---

**Built with ❤️ for HCL Hackathon 2025**
