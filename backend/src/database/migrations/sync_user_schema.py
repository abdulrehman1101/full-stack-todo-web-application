"""
Database migration script to sync the user table schema with the User model.
This script ensures the database table has the same columns as the User model.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy import create_engine, text, inspect
from ..config.settings import settings
from ..models.user import User
from sqlmodel import SQLModel
from ..engine import create_db_engine

def sync_user_table_schema():
    """
    Synchronizes the user table schema with the User model.
    """
    print("Starting database schema synchronization...")

    # Create database engine
    engine = create_db_engine(settings.database_url)

    try:
        # Use SQLModel metadata to create/update tables
        # This will create missing tables and columns
        print("Creating all tables based on SQLModel metadata...")
        SQLModel.metadata.create_all(engine)

        print("Database schema synchronized successfully!")

        # Verify the columns exist
        inspector = inspect(engine)
        columns = inspector.get_columns('user')
        column_names = [col['name'] for col in columns]

        print(f"Columns in 'user' table: {column_names}")

        # Check if required columns exist
        required_columns = ['name', 'username']
        missing_columns = [col for col in required_columns if col not in column_names]

        if missing_columns:
            print(f"ERROR: Missing columns: {missing_columns}")
            return False
        else:
            print("All required columns exist in the user table.")
            return True

    except Exception as e:
        print(f"Error during schema synchronization: {str(e)}")
        raise

if __name__ == "__main__":
    sync_user_table_schema()