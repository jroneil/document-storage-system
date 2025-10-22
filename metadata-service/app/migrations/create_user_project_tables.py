"""
Database migration script to create user and project tables.
Run this script to initialize the user-project structure in PostgreSQL.
"""

import os
import sys
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Add the parent directory to Python path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.postgres_models import Base

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv(
    "POSTGRES_URL",
    "postgresql://admin:password@localhost:5432/document_storage"
)

def create_tables():
    """Create all tables defined in the models."""
    try:
        engine = create_engine(DATABASE_URL)
        
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✓ Tables created successfully!")
        
        # Print created tables
        print("\nCreated tables:")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
            
    except Exception as e:
        print(f"✗ Error creating tables: {str(e)}")
        raise

def drop_tables():
    """Drop all tables (use with caution!)."""
    try:
        engine = create_engine(DATABASE_URL)
        
        print("WARNING: Dropping all tables...")
        response = input("Are you sure? Type 'yes' to confirm: ")
        
        if response.lower() == 'yes':
            Base.metadata.drop_all(bind=engine)
            print("✓ Tables dropped successfully!")
        else:
            print("Operation cancelled.")
            
    except Exception as e:
        print(f"✗ Error dropping tables: {str(e)}")
        raise

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--drop':
        drop_tables()
    else:
        create_tables()
