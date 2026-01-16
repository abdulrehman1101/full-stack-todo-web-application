#!/usr/bin/env python3
"""
Final validation script for the todo application database foundation.
This script validates that all components of the database foundation are working properly.
"""
import subprocess
import sys
import os
from pathlib import Path

# Add the backend/src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from .health_check import check_database_connection, check_database_session
from .schema_verification import run_schema_verification


def run_final_validation():
    """
    Runs the complete final validation for the database foundation.
    """
    print("=" * 60)
    print("FINAL VALIDATION: Database Foundation & Schema (Spec 1)")
    print("=" * 60)

    # Change to the backend directory to run tests
    original_dir = os.getcwd()
    backend_dir = Path(__file__).parent.parent.parent
    os.chdir(backend_dir)

    try:
        # 1. Check database connectivity
        print("\n1. Testing database connectivity...")
        connection_ok = check_database_connection()
        print(f"   Database connection: {'✓ PASS' if connection_ok else '✗ FAIL'}")

        # 2. Check database session
        print("\n2. Testing database session management...")
        session_ok = check_database_session()
        print(f"   Database session: {'✓ PASS' if session_ok else '✗ FAIL'}")

        # 3. Run schema verification
        print("\n3. Verifying database schema...")
        schema_ok = run_schema_verification()
        print(f"   Schema verification: {'✓ PASS' if schema_ok else '✗ FAIL'}")

        # 4. Run integration tests
        print("\n4. Running integration tests...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest",
                "backend/tests/integration/test_db_connectivity.py",
                "-v"
            ], capture_output=True, text=True, timeout=60)

            integration_tests_ok = result.returncode == 0
            print(f"   Integration tests: {'✓ PASS' if integration_tests_ok else '✗ FAIL'}")

            if not integration_tests_ok:
                print(f"   Details: {result.stderr}")

        except subprocess.TimeoutExpired:
            print("   Integration tests: ✗ TIMEOUT")
            integration_tests_ok = False
        except Exception as e:
            print(f"   Integration tests: ✗ ERROR - {str(e)}")
            integration_tests_ok = False

        # 5. Check that all required files exist
        print("\n5. Checking required files...")
        required_files = [
            "backend/src/database/models/user.py",
            "backend/src/database/models/task.py",
            "backend/src/database/engine.py",
            "backend/src/database/session.py",
            "backend/src/database/init_db.py",
            "backend/src/config/settings.py",
            "backend/requirements.txt",
            ".env.example"
        ]

        files_ok = True
        for file_path in required_files:
            if os.path.exists(file_path):
                print(f"   ✓ {file_path}")
            else:
                print(f"   ✗ Missing: {file_path}")
                files_ok = False

        # 6. Overall status
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY:")
        print("=" * 60)

        all_checks = [
            ("Database Connection", connection_ok),
            ("Database Session", session_ok),
            ("Schema Verification", schema_ok),
            ("Integration Tests", integration_tests_ok),
            ("Required Files", files_ok)
        ]

        total_passed = sum(1 for _, passed in all_checks if passed)
        total_tests = len(all_checks)

        for name, passed in all_checks:
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{name:<20}: {status}")

        print("-" * 60)
        print(f"PASSED: {total_passed}/{total_tests}")

        overall_success = all(check[1] for check in all_checks)

        if overall_success:
            print("\n🎉 SPEC 1: DATABASE FOUNDATION & SCHEMA - COMPLETE ✓")
            print("   All components successfully validated!")
            print("   Ready for Spec 2: API Implementation")
        else:
            print("\n❌ SPEC 1: DATABASE FOUNDATION & SCHEMA - INCOMPLETE ✗")
            print("   Some components failed validation.")

        print("=" * 60)

        return overall_success

    finally:
        # Restore original directory
        os.chdir(original_dir)


if __name__ == "__main__":
    success = run_final_validation()
    sys.exit(0 if success else 1)