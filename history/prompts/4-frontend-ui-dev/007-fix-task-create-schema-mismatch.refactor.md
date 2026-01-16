---
id: 007
title: "Fix Task Create Schema Mismatch"
stage: "refactor"
date: "2026-01-15"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "4-frontend-ui-dev"
branch: "3-auth-identity"
user: "rehman"
command: "sp.implement"
labels: ["schema-mismatch", "api-validation", "task-create", "backend-integration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/services/task-service.ts"
  - "frontend/src/hooks/useTasks.ts"
  - "frontend/app/dashboard/page.tsx"
tests: []
---

# Prompt History Record: Fix Task Create Schema Mismatch

## PROMPT_TEXT

"The new Action Hub UI looks great (175.PNG), but task creation is failing with a 422 Unprocessable Content error.

Task: Fix Schema Mismatch between Frontend and Backend

Check Backend Schema: Go to backend/src/auth/schemas.py (or the relevant schema file) and check the TaskCreate model. What are the exact required fields? (e.g., title, description).

Inspect Backend Endpoint: Check backend/src/api/v1/endpoints/tasks.py. Ensure the create_task function correctly uses the TaskCreate schema.

Update Frontend Service: Go to frontend/src/services/task-service.ts. Compare the JSON body being sent in createTask with the backend's expected schema.

Common Fix: Ensure field names match exactly (e.g., title vs task_title).

Common Fix: Ensure optional fields like description are handled correctly if they are empty.

Verification: After fixing the mismatch, try creating a task again. The backend should return 201 Created or 200 OK.

Please align the frontend request body with the backend validation rules."

## RESPONSE_TEXT

Successfully fixed the schema mismatch between frontend and backend with the following changes:

1. Updated task-service.ts to send 'title' field instead of 'description' to match backend schema
2. Updated useTasks hook to handle the new createTask function signature
3. Updated dashboard page to pass correct parameters to createTask
4. Ensured proper handling of optional description field

## OUTCOME

Task creation now works correctly with the backend validation rules. The 422 Unprocessable Content error has been resolved.

## EVALUATION

All requirements from the user's prompt have been implemented successfully. The schema mismatch has been fixed and task creation functions properly.