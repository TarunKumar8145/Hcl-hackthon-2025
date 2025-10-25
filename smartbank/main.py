from fastapi import FastAPI, Depends, HTTPException, status, Form, File, UploadFile, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
import shutil
from typing import List

from database import SessionLocal, engine, get_db
from models import Base, User, KYCDocument, KYCStatus, UserRole, Account
import schemas
from auth import get_password_hash, authenticate_user, create_access_token, get_current_user

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartBank API", version="1.0.0")

# Create directories for static files and uploads
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
os.makedirs("uploads", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# API Routes
@app.post("/api/register", response_model=schemas.UserResponse)
async def register_user(user: schemas.UserRegistration, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.phone == user.phone)
    ).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email or phone number already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        phone=user.phone,
        password_hash=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
        address=user.address
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.post("/api/login", response_model=schemas.Token)
async def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_role": user.role.value
    }

@app.post("/api/kyc/upload")
async def upload_kyc_document(
    document_type: str = Form(...),
    document_number: str = Form(...),
    document_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate file type
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.pdf'}
    file_extension = os.path.splitext(document_file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG, and PDF files are allowed"
        )
    
    # Save file
    file_path = f"uploads/{current_user.id}_{document_type}_{document_file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(document_file.file, buffer)
    
    # Save KYC document record
    kyc_doc = KYCDocument(
        user_id=current_user.id,
        document_type=document_type,
        document_number=document_number,
        document_path=file_path
    )
    
    db.add(kyc_doc)
    db.commit()
    db.refresh(kyc_doc)
    
    return {"message": "KYC document uploaded successfully", "document_id": kyc_doc.id}

@app.get("/api/kyc/status", response_model=List[schemas.KYCDocumentResponse])
async def get_kyc_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    kyc_docs = db.query(KYCDocument).filter(KYCDocument.user_id == current_user.id).all()
    return kyc_docs

# Role-based access control
async def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

async def get_auditor_user(current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.AUDITOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Auditor access required"
        )
    return current_user

@app.post("/api/admin/create", response_model=schemas.UserResponse)
async def create_admin(
    email: str = Form(...),
    password: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Generate unique phone number for admin
    import random
    unique_phone = f"900000{random.randint(1000, 9999)}"
    
    # Create admin user
    hashed_password = get_password_hash(password)
    admin_user = User(
        email=email,
        phone=unique_phone,
        password_hash=hashed_password,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=datetime(1990, 1, 1),  # Default DOB
        address="Admin Address",
        role=UserRole.ADMIN
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    return admin_user

@app.get("/api/admin/users", response_model=List[schemas.UserResponse])
async def get_all_users(
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return users

@app.put("/api/admin/kyc/{document_id}/approve")
async def approve_kyc_document(
    document_id: int,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    kyc_doc = db.query(KYCDocument).filter(KYCDocument.id == document_id).first()
    if not kyc_doc:
        raise HTTPException(status_code=404, detail="KYC document not found")
    
    kyc_doc.status = KYCStatus.APPROVED
    kyc_doc.verified_by = admin_user.id
    kyc_doc.verified_at = datetime.utcnow()
    
    db.commit()
    return {"message": "KYC document approved"}

@app.put("/api/admin/kyc/{document_id}/reject")
async def reject_kyc_document(
    document_id: int,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    kyc_doc = db.query(KYCDocument).filter(KYCDocument.id == document_id).first()
    if not kyc_doc:
        raise HTTPException(status_code=404, detail="KYC document not found")
    
    kyc_doc.status = KYCStatus.REJECTED
    kyc_doc.verified_by = admin_user.id
    kyc_doc.verified_at = datetime.utcnow()
    
    db.commit()
    return {"message": "KYC document rejected"}

@app.get("/api/admin/kyc/pending")
async def get_pending_kyc_documents(
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    pending_docs = db.query(KYCDocument).filter(
        KYCDocument.status == KYCStatus.PENDING
    ).all()
    return pending_docs

@app.post("/api/accounts/create")
async def create_account(
    account_type: str = Form(...),
    initial_deposit: float = Form(0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Generate unique account number
    import random
    account_number = f"SB{random.randint(100000000000, 999999999999)}"
    
    # Ensure account number is unique
    while db.query(Account).filter(Account.account_number == account_number).first():
        account_number = f"SB{random.randint(100000000000, 999999999999)}"
    
    # Create new account
    new_account = Account(
        account_number=account_number,
        user_id=current_user.id,
        account_type=account_type.upper(),
        balance=initial_deposit
    )
    
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    
    return {
        "message": "Account created successfully",
        "account_number": account_number,
        "account_type": account_type,
        "balance": initial_deposit
    }

@app.post("/api/transfer")
async def transfer_money(
    from_account: str = Form(...),
    to_account: str = Form(...),
    amount: float = Form(...),
    description: str = Form(""),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate amount
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    
    # Get sender account
    sender_account = db.query(Account).filter(
        Account.account_number == from_account,
        Account.user_id == current_user.id
    ).first()
    
    if not sender_account:
        raise HTTPException(status_code=404, detail="Sender account not found")
    
    # Get receiver account
    receiver_account = db.query(Account).filter(Account.account_number == to_account).first()
    if not receiver_account:
        raise HTTPException(status_code=404, detail="Receiver account not found")
    
    # Validate sender balance
    if float(sender_account.balance) < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    # Simple daily limit check
    if amount > float(sender_account.daily_limit):
        raise HTTPException(status_code=400, detail="Amount exceeds daily limit")
    
    try:
        # Update balances
        sender_account.balance = float(sender_account.balance) - amount
        receiver_account.balance = float(receiver_account.balance) + amount
        
        db.commit()
        
        return {
            "message": "Transfer successful",
            "amount": amount,
            "from_account": from_account,
            "to_account": to_account,
            "new_balance": float(sender_account.balance)
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Transfer failed: {str(e)}")

@app.get("/api/transactions")
async def get_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get user's account IDs
    user_accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
    account_ids = [acc.id for acc in user_accounts]
    
    # Get transactions where user is sender or receiver
    transactions = db.query(Transaction).filter(
        (Transaction.from_account_id.in_(account_ids)) |
        (Transaction.to_account_id.in_(account_ids))
    ).order_by(Transaction.created_at.desc()).limit(10).all()
    
    return transactions
async def get_user_accounts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
    return accounts
async def get_pending_kyc_documents(
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    pending_docs = db.query(KYCDocument).filter(
        KYCDocument.status == KYCStatus.PENDING
    ).all()
    return pending_docs

@app.post("/api/accounts/create")
async def create_account(
    account_type: str = Form(...),
    initial_deposit: float = Form(1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    import random
    
    # Generate unique account number
    account_number = f"SB{random.randint(100000000000, 999999999999)}"
    
    # Ensure uniqueness
    while db.query(Account).filter(Account.account_number == account_number).first():
        account_number = f"SB{random.randint(100000000000, 999999999999)}"
    
    # Set daily limits based on account type
    daily_limits = {
        "SAVINGS": 50000.00,
        "CURRENT": 100000.00,
        "FD": 50000.00
    }
    
    # Create new account
    new_account = Account(
        account_number=account_number,
        user_id=current_user.id,
        account_type=account_type.upper(),
        balance=initial_deposit,
        daily_limit=daily_limits.get(account_type.upper(), 50000.00)
    )
    
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    
    return {
        "message": "Account created successfully",
        "account_number": account_number,
        "account_type": account_type.upper(),
        "balance": initial_deposit
    }

@app.get("/api/accounts")
async def get_user_accounts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
    return accounts

@app.post("/api/transfer")
async def transfer_money(
    from_account: str = Form(...),
    to_account: str = Form(...),
    amount: float = Form(...),
    description: str = Form(""),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate amount
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    
    # Get sender account
    sender_account = db.query(Account).filter(
        Account.account_number == from_account,
        Account.user_id == current_user.id
    ).first()
    
    if not sender_account:
        raise HTTPException(status_code=404, detail="Sender account not found")
    
    # Get receiver account
    receiver_account = db.query(Account).filter(Account.account_number == to_account).first()
    if not receiver_account:
        raise HTTPException(status_code=404, detail="Receiver account not found")
    
    # Validate sender balance
    if sender_account.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    # Check daily limit (simplified - just check current balance for now)
    if amount > float(sender_account.daily_limit):
        raise HTTPException(status_code=400, detail="Amount exceeds daily limit")
    
    try:
        # Update balances
        sender_account.balance -= amount
        receiver_account.balance += amount
        
        db.commit()
        
        return {
            "message": "Transfer successful",
            "amount": amount,
            "from_account": from_account,
            "to_account": to_account,
            "new_balance": float(sender_account.balance)
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Transfer failed: {str(e)}")

# Web Routes for UI
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/kyc", response_class=HTMLResponse)
async def kyc_page(request: Request):
    return templates.TemplateResponse("kyc.html", {"request": request})

@app.get("/accounts/create", response_class=HTMLResponse)
async def create_account_page(request: Request):
    return templates.TemplateResponse("create_account.html", {"request": request})

@app.get("/transfer", response_class=HTMLResponse)
async def transfer_page(request: Request):
    return templates.TemplateResponse("transfer.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/transfer", response_class=HTMLResponse)
async def transfer_page(request: Request):
    return templates.TemplateResponse("transfer.html", {"request": request})

@app.get("/accounts/create", response_class=HTMLResponse)
async def create_account_page(request: Request):
    return templates.TemplateResponse("create_account.html", {"request": request})

@app.get("/admin/create", response_class=HTMLResponse)
async def admin_create_page(request: Request):
    return templates.TemplateResponse("admin_create.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
