#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main import app
    print("✅ Application imports successfully!")
    
    # Test database connection
    from database import engine
    from sqlalchemy import text
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
    
    print("✅ All systems ready!")
    print("\nTo start the application:")
    print("cd /mnt/c/Users/User/OneDrive/Desktop/HCL-HACKTHON1/smartbank")
    print("source venv/bin/activate")
    print("uvicorn main:app --host 0.0.0.0 --port 8000")
    print("\nThen visit: http://localhost:8000")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
