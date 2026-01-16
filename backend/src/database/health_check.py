"""
Database health check for the todo application.
This module provides functions to verify database connectivity.
"""
from sqlalchemy import text
from .engine import engine
from .session import get_session


def check_database_connection():
    """
    Performs a simple health check by executing a basic query against the database.

    Returns:
        bool: True if the database connection is healthy, False otherwise
    """
    if engine is None:
        print("Database engine not initialized")
        return False

    try:
        # Test the connection by executing a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            row = result.fetchone()
            if row and row[0] == 1:
                return True
            return False
    except Exception as e:
        print(f"Database connection health check failed: {str(e)}")
        return False


def check_database_session():
    """
    Performs a health check using the session management system.

    Returns:
        bool: True if the session system is working properly, False otherwise
    """
    try:
        # Test using the session context manager
        from .session import get_session
        with get_session() as session:
            result = session.exec(text("SELECT 1"))
            row = result.first()
            if row and row[0] == 1:
                return True
            return False
    except Exception as e:
        print(f"Database session health check failed: {str(e)}")
        return False


if __name__ == "__main__":
    print("Running database health checks...")

    connection_ok = check_database_connection()
    print(f"Connection health check: {'PASSED' if connection_ok else 'FAILED'}")

    session_ok = check_database_session()
    print(f"Session health check: {'PASSED' if session_ok else 'FAILED'}")

    overall_status = connection_ok and session_ok
    print(f"Overall database health: {'HEALTHY' if overall_status else 'UNHEALTHY'}")