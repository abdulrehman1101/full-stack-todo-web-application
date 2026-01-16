"""
Database migration script to add missing columns to the user table.
This script adds the name and username columns that were added to the User model
but not to the database schema.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy import create_engine, text
from ..config.settings import settings

def add_missing_user_columns():
    """
    Adds missing name and username columns to the user table.
    """
    print("Starting database migration to add missing user columns...")

    # Create database engine
    engine = create_engine(settings.database_url)

    try:
        with engine.connect() as conn:
            # Check if 'name' column exists
            print("Checking if 'name' column exists...")
            name_col_query = text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'user' AND column_name = 'name'
            """)

            result = conn.execute(name_col_query)
            name_exists = result.fetchone() is not None

            if not name_exists:
                print("Adding 'name' column to user table...")
                add_name_query = text("ALTER TABLE \"user\" ADD COLUMN name VARCHAR(255)")
                conn.execute(add_name_query)
                conn.commit()
                print("'name' column added successfully!")
            else:
                print("'name' column already exists.")

            # Check if 'username' column exists
            print("Checking if 'username' column exists...")
            username_col_query = text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'user' AND column_name = 'username'
            """)

            result = conn.execute(username_col_query)
            username_exists = result.fetchone() is not None

            if not username_exists:
                print("Adding 'username' column to user table...")
                add_username_query = text("ALTER TABLE \"user\" ADD COLUMN username VARCHAR(255)")
                conn.execute(add_username_query)
                conn.commit()
                print("'username' column added successfully!")
            else:
                print("'username' column already exists.")

        print("Database migration completed successfully!")

    except Exception as e:
        print(f"Error during migration: {str(e)}")
        raise

if __name__ == "__main__":
    add_missing_user_columns()