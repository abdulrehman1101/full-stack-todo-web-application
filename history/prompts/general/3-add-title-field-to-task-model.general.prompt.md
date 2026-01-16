---
id: 3
title: Add Missing Title Field to Task Model
stage: green
date_iso: 2026-01-14
surface: agent
model: sonnet-4-5-20250929
feature: none
branch: 3-auth-identity
user: claude
command: "The authentication is now working, but I'm getting a 500 Internal Server Error when creating a task (as seen in 150.PNG). The logs indicate a ResponseValidationError because the title field is missing in the returned Task object."
labels: ["bug-fix", "database", "model", "validation", "schema"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/src/database/models/task.py
  - backend/src/database/schemas/task_schemas.py
  - backend/src/api/v1/endpoints/tasks.py
tests_yaml: |
  - Task model now includes title field
  - Database schema updated with title column
  - Task creation endpoint works properly
prompt_text: |
  "The authentication is now working, but I'm getting a 500 Internal Server Error when creating a task (as seen in 150.PNG). The logs indicate a ResponseValidationError because the title field is missing in the returned Task object.

  Task:

  Update Task Model: Go to backend/src/database/models/task.py. Ensure the Task model has a title field: title: str = Field(index=True)

  Update Schemas: Go to backend/src/database/schemas/task_schemas.py. Ensure that TaskCreate and TaskRead both include the title field.

  Sync Database: Since we are adding a new column (title) to the Task table, please drop the existing task table and recreate it to reflect the new schema.

  Verify Create Logic: In backend/src/api/v1/endpoints/tasks.py, ensure the create_task function is correctly mapping the title from the request to the database model.

  Restart Server: Restart the server and try creating the task again.

  Please provide the updated code for the Task model and the create_task endpoint."
response_text: |
  Fixed the missing title field issue by:

  1. Updated backend/src/database/models/task.py to add title field:
     - Added title field to TaskBase with min_length=1, max_length=200
     - Added explicit title field definition in Task model with proper constraints
     - Set nullable=False and index=True as requested

  2. Verified that the schemas in task_schemas.py already had the title field correctly defined

  3. Verified that the task endpoint in tasks.py was already correctly mapping the title field

  4. Recreated the database to apply the new schema with the title column

  The Task model now has a proper title field that matches the API schema expectations.
outcome: |
  The 500 Internal Server Error has been resolved. The ResponseValidationError no longer occurs.
  Task creation endpoint now works properly with the title field.
evaluation: |
  Verified that the task creation endpoint works correctly and returns a proper Task object with all expected fields including title.
---