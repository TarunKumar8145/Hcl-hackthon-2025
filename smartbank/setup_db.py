import pymysql
from sqlalchemy import create_engine
from models import Base

def create_database():
    """Create the smartbank database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root'
        )
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS smartbank")
            print("Database 'smartbank' created successfully!")
        
        connection.close()
        
        # Now create tables using SQLAlchemy
        engine = create_engine("mysql+pymysql://root:root@localhost/smartbank")
        Base.metadata.create_all(bind=engine)
        print("All tables created successfully!")
        
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    create_database()
