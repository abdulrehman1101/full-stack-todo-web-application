"""
Script to manually add missing columns to the user table in PostgreSQL.
This addresses the issue where the User model was updated but the database wasn't.
"""

import subprocess
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from src.config.settings import settings

def run_manual_migration():
    """
    Manually add missing columns to the user table.
    """
    print("Starting manual database migration...")

    # Connect to the database
    engine = create_engine(settings.database_url)

    try:
        with engine.connect() as conn:
            # Add name column if it doesn't exist
            print("Adding name column (if not exists)...")
            add_name_sql = """
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                               WHERE table_name = 'user' AND column_name = 'name') THEN
                    ALTER TABLE "user" ADD COLUMN name VARCHAR(255);
                END IF;
            END $$;
            """
            conn.execute(text(add_name_sql))

            # Add username column if it doesn't exist
            print("Adding username column (if not exists)...")
            add_username_sql = """
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                               WHERE table_name = 'user' AND column_name = 'username') THEN
                    ALTER TABLE "user" ADD COLUMN username VARCHAR(255);
                END IF;
            END $$;
            """
            conn.execute(text(add_username_sql))

            # Commit the transaction
            conn.commit()

            print("Database migration completed successfully!")
            print("Added 'name' and 'username' columns to the 'user' table.")

    except Exception as e:
        print(f"Error during migration: {str(e)}")
        raise

if __name__ == "__main__":
    run_manual_migration()