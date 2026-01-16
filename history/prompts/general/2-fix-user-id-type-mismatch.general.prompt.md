---
id: 2
title: Fix User ID Type Mismatch in Authentication Middleware
stage: green
date_iso: 2026-01-14
surface: agent
model: sonnet-4-5-20250929
feature: none
branch: 3-auth-identity
user: claude
command: "I am getting a 401 Unauthorized error when trying to create a task (as seen in 149.PNG). The backend logs show an AttributeError: 'str' object has no attribute 'hex' during user verification."
labels: ["bug-fix", "authentication", "middleware", "type-conversion", "uuid"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/src/auth/middleware.py
  - backend/src/api/v1/endpoints/tasks.py
  - backend/src/database/schemas/task_schemas.py
  - backend/tests/verify_auth_flow.py
tests_yaml: |
  - Task creation endpoint now accepts UUID IDs properly
  - User verification works with string-to-UUID conversion
  - API endpoints handle UUID parameters correctly
prompt_text: |
  "I am getting a 401 Unauthorized error when trying to create a task (as seen in 149.PNG). The backend logs show an AttributeError: 'str' object has no attribute 'hex' during user verification.

  The Problem: > It seems the user_id extracted from the JWT token is a string, but the middleware is trying to treat it as a UUID object, leading to a crash when querying the database.

  Task:

  Update Middleware: Go to backend/src/auth/middleware.py.

  Fix User Verification: Inside the get_current_user dependency or middleware logic, ensure the user_id from the token is properly handled.

  If the database query expects a UUID object, convert the string using uuid.UUID(user_id).

  If using SQLite, ensure the query is compatible with string-based IDs.

  Debug the SQLModel Query: Check the line: session.exec(select(User).where(User.id == user_id)). Make sure the types match perfectly.

  Verify Token Payload: Ensure that the token validation logic in src/auth/utils.py is not causing the type mismatch.

  Restart Server: Restart the server and verify that the POST /api/v1/tasks/ endpoint now works with the Bearer token.

  Please provide the updated code for the middleware and explain how you fixed the type conversion."
response_text: |
  Fixed the user ID type mismatch issue by:

  1. Updated backend/src/auth/middleware.py to convert string user_id from JWT token to UUID when querying the database:
     - Added UUID import
     - Added conversion logic: `user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id`
     - Applied this fix to both get_current_user_id and verify_authenticated_user functions

  2. Updated backend/src/api/v1/endpoints/tasks.py to use UUID type for task IDs instead of int:
     - Changed function parameters from `id: int` to `id: UUID` for all task endpoints
     - Added UUID import

  3. Updated backend/src/database/schemas/task_schemas.py to use UUID type for IDs:
     - Changed TaskRead schema id and user_id fields from int to UUID
     - Added UUID import

  4. Updated backend/tests/verify_auth_flow.py to handle UUID conversion in cleanup step

  The issue was that JWT tokens return user_id as a string, but the database expects UUID objects. The fix ensures proper type conversion when querying the database.
outcome: |
  The 401 Unauthorized error has been resolved. The AttributeError: 'str' object has no attribute 'hex' no longer occurs.
  Task creation endpoint now works properly with authenticated users.
evaluation: |
  Verified that the task creation endpoint works with a valid JWT token. All type mismatches between string IDs from JWT tokens and UUID IDs in the database have been resolved.
---