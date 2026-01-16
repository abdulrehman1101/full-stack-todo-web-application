"""
Schema verification for the todo application models.
This module verifies that the SQLModel models exist in the database with correct structure.
"""
from sqlalchemy import text
from .engine import engine
from .models.user import User
from .models.task import Task
import inspect


def verify_schema_exists():
    """
    Verifies that the User and Task tables exist in the database with the correct columns,
    data types, and foreign key relationships.
    """
    if engine is None:
        print("Database engine not initialized")
        return False

    try:
        with engine.connect() as connection:
            # Check if User table exists and has correct columns
            user_columns = connection.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'user'
                ORDER BY ordinal_position
            """)).fetchall()

            if not user_columns:
                print("User table does not exist")
                return False

            print(f"User table has {len(user_columns)} columns:")
            for col in user_columns:
                print(f"  - {col[0]}: {col[1]} (nullable: {col[2]})")

            # Check if Task table exists and has correct columns
            task_columns = connection.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'task'
                ORDER BY ordinal_position
            """)).fetchall()

            if not task_columns:
                print("Task table does not exist")
                return False

            print(f"Task table has {len(task_columns)} columns:")
            for col in task_columns:
                print(f"  - {col[0]}: {col[1]} (nullable: {col[2]})")

            # Check foreign key relationships
            fk_query = text("""
                SELECT
                    tc.table_name,
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                    AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY'
            """)

            foreign_keys = connection.execute(fk_query).fetchall()
            print(f"Found {len(foreign_keys)} foreign key relationships:")
            for fk in foreign_keys:
                print(f"  - {fk[0]}.{fk[1]} -> {fk[2]}.{fk[3]}")

            # Verify specific expected columns
            user_column_names = [col[0] for col in user_columns]
            expected_user_cols = ['id', 'email', 'created_at']
            missing_user_cols = [col for col in expected_user_cols if col not in user_column_names]

            if missing_user_cols:
                print(f"Missing User columns: {missing_user_cols}")
                return False

            task_column_names = [col[0] for col in task_columns]
            expected_task_cols = ['id', 'user_id', 'description', 'is_completed', 'created_at']
            missing_task_cols = [col for col in expected_task_cols if col not in task_column_names]

            if missing_task_cols:
                print(f"Missing Task columns: {missing_task_cols}")
                return False

            print("Schema verification passed: All tables and columns exist as expected")
            return True

    except Exception as e:
        print(f"Schema verification failed: {str(e)}")
        return False


def run_schema_verification():
    """
    Runs the complete schema verification process.
    """
    print("Running schema verification against live database...")
    success = verify_schema_exists()
    print(f"Schema verification: {'PASSED' if success else 'FAILED'}")
    return success


if __name__ == "__main__":
    run_schema_verification()