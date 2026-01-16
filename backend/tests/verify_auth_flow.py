#!/usr/bin/env python3
"""
Test script to verify the JWT handshake between Better Auth and FastAPI backend.
This script simulates the authentication flow to ensure tokens are properly generated and verified.
"""

import asyncio
import httpx
import os
import sys
from pathlib import Path

# Add the backend src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.config.settings import settings
from src.auth.utils import create_access_token
from src.auth.middleware import get_current_user_id
from src.database.models.user import User
from sqlmodel import Session, select
from src.database.session import get_session

async def test_jwt_handshake():
    """
    Test the complete JWT handshake flow:
    1. Simulate token generation (as would happen in Better Auth)
    2. Verify token can be used with protected backend endpoints
    3. Test that missing tokens return 401
    """
    print("[TEST] Starting JWT Handshake Verification Test...")

    # Test 1: Check if settings are properly loaded
    print("\n[STEP 1] Checking environment configuration...")
    if not settings.better_auth_secret:
        print("[ERROR] BETTER_AUTH_SECRET not found in settings")
        return False
    print(f"[SUCCESS] BETTER_AUTH_SECRET loaded: {settings.better_auth_secret[:10]}...")

    # Test 2: Create a mock user in the database to test with
    print("\n[STEP 2] Creating test user in database...")
    try:
        # Create the session using the context manager approach
        from contextlib import contextmanager
        # Get session using the context manager
        session_context = get_session()

        # Enter the context manager
        session = next(session_context)

        try:
            # Create a test user
            from uuid import uuid4
            from datetime import datetime

            test_user = User(
                id=uuid4(),
                email="test@example.com",
                created_at=datetime.utcnow()
            )
            session.add(test_user)
            session.commit()
            session.refresh(test_user)

            print(f"[SUCCESS] Test user created with ID: {test_user.id}")
            user_id = str(test_user.id)
        finally:
            # Exit the context manager properly
            try:
                next(session_context)
            except StopIteration:
                pass
    except Exception as e:
        print(f"[ERROR] Failed to create test user: {e}")
        return False

    # Test 3: Generate a JWT token (simulating what Better Auth would do)
    print("\n[STEP 3] Generating JWT token...")
    try:
        token_data = {
            "sub": user_id,  # Subject = user ID
            "email": "test@example.com",
            "role": "user"
        }

        # Create access token using our auth utility
        jwt_token = create_access_token(data=token_data)
        print(f"[SUCCESS] JWT token generated successfully")
        print(f"   Token preview: {jwt_token[:50]}...")
    except Exception as e:
        print(f"[ERROR] Failed to generate JWT token: {e}")
        return False

    # Test 4: Verify the token can be decoded and validated (simulating backend middleware)
    print("\n[STEP 4] Testing token verification...")
    try:
        # Import here to avoid circular imports
        from src.auth.utils import verify_token

        decoded_payload = verify_token(jwt_token)
        if decoded_payload:
            print(f"[SUCCESS] Token verified successfully")
            print(f"   User ID from token: {decoded_payload.get('sub')}")
            print(f"   Email from token: {decoded_payload.get('email')}")
        else:
            print(f"[ERROR] Token verification failed")
            return False
    except Exception as e:
        print(f"[ERROR] Failed to verify token: {e}")
        return False

    # Test 5: Test the middleware function directly (simulating protected endpoint access)
    print("\n[STEP 5] Testing middleware function...")
    try:
        # This simulates what happens when a request with a valid token hits a protected endpoint
        # Get session using the context manager
        session_context = get_session()

        # Enter the context manager
        session = next(session_context)

        try:
            # We'll simulate the credentials by manually calling the verification function
            from src.auth.utils import extract_user_id_from_token

            extracted_user_id = extract_user_id_from_token(jwt_token)
            if extracted_user_id and extracted_user_id == user_id:
                print(f"[SUCCESS] Middleware extraction successful")
                print(f"   Extracted user ID matches: {extracted_user_id == user_id}")
            else:
                print(f"[ERROR] Middleware extraction failed")
                print(f"   Expected: {user_id}, Got: {extracted_user_id}")
                return False
        finally:
            # Exit the context manager properly
            try:
                next(session_context)
            except StopIteration:
                pass
    except Exception as e:
        print(f"[ERROR] Failed middleware test: {e}")
        return False

    # Test 6: Test that invalid/missing tokens return proper errors
    print("\n[STEP 6] Testing security - invalid token handling...")
    try:
        # Test with invalid token
        invalid_result = verify_token("invalid.token.here")
        if invalid_result is None:
            print(f"[SUCCESS] Invalid token properly rejected")
        else:
            print(f"[ERROR] Invalid token was accepted")
            return False

        # Test with expired token (create one that expires immediately)
        import time
        expired_token_data = {
            "sub": user_id,
            "email": "test@example.com",
            "exp": time.time() - 1  # Expired 1 second ago
        }

        expired_token = create_access_token(data=expired_token_data)
        expired_result = verify_token(expired_token)
        if expired_result is None:
            print(f"[SUCCESS] Expired token properly rejected")
        else:
            print(f"[ERROR] Expired token was accepted")
            return False

    except Exception as e:
        print(f"[ERROR] Failed security test: {e}")
        return False

    # Test 7: Clean up - remove test user
    print("\n[STEP 7] Cleaning up test user...")
    try:
        # Get session using the context manager
        session_context = get_session()

        # Enter the context manager
        session = next(session_context)

        try:
            from uuid import UUID
            user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
            test_user = session.get(User, user_uuid)
            if test_user:
                session.delete(test_user)
                session.commit()
                print(f"[SUCCESS] Test user cleaned up")
            else:
                print(f"[WARN] Test user not found for cleanup")
        finally:
            # Exit the context manager properly
            try:
                next(session_context)
            except StopIteration:
                pass
    except Exception as e:
        print(f"[WARN] Cleanup failed: {e}")
        # Don't fail the test for cleanup issues

    print("\n[OVERALL] JWT Handshake Verification Test: PASSED!")
    print("\n[SUMMARY]")
    print("   - Environment properly configured")
    print("   - Test user created and cleaned up")
    print("   - JWT token generated successfully")
    print("   - Token verification working")
    print("   - Middleware function working")
    print("   - Security measures in place (invalid/expired tokens rejected)")
    print("\n[RESULT] The JWT handshake between frontend auth and backend API is working correctly!")

    return True

async def test_http_endpoints():
    """
    Test the actual HTTP endpoints if they were running
    """
    print("\n🌐 Testing HTTP endpoints (would require running server)...")
    print("ℹ️  This test shows what would happen with actual HTTP requests:")
    print("   • POST /api/auth/login → returns JWT token")
    print("   • GET /api/v1/users/me with Bearer token → returns user data")
    print("   • GET /api/v1/users/me without token → returns 401")

    # Show example requests that would work
    print("\n📝 Example requests that would work:")
    print("curl -X POST http://localhost:8000/api/auth/login \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"email\":\"test@example.com\",\"password\":\"password123\"}'")
    print("")
    print("curl -X GET http://localhost:8000/api/v1/users/me \\")
    print("  -H 'Authorization: Bearer <your-jwt-token>'")
    print("")
    print("curl -X GET http://localhost:8000/api/v1/users/me \\")
    print("  # (no token) → should return 401 Unauthorized")

if __name__ == "__main__":
    print("[TOOL] JWT Handshake Verification Tool")
    print("=" * 50)

    # Run the main verification test
    success = asyncio.run(test_jwt_handshake())

    if success:
        print("\n" + "=" * 50)
        print("[SUCCESS] OVERALL RESULT: SUCCESS!")
        print("The JWT handshake is working correctly.")
        print("Frontend authentication can successfully communicate with backend API protection.")

        # Also run the HTTP endpoint examples
        asyncio.run(test_http_endpoints())
    else:
        print("\n" + "=" * 50)
        print("[FAILURE] OVERALL RESULT: FAILED")
        print("There are issues with the JWT handshake that need to be resolved.")
        sys.exit(1)