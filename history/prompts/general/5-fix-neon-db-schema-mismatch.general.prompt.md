---
id: 5
title: Fix Neon DB Schema Mismatch
stage: green
date_iso: 2026-01-14
surface: agent
model: sonnet-4-5-20250929
feature: none
branch: 3-auth-identity
user: claude
command: "I switched back to Neon DB, but registration is failing with a 500 Internal Server Error (as seen in 152.PNG). The logs show: column 'hashed_password' of relation 'user' does not exist."
labels: ["database", "schema", "migration", "neon", "postgres"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/drop_and_recreate_tables.py (temporary script)
tests_yaml: |
  - Tables dropped and recreated successfully
  - User table now includes hashed_password column
  - Task table includes proper foreign key relationships
prompt_text: |
  "I switched back to Neon DB, but registration is failing with a 500 Internal Server Error (as seen in 152.PNG). The logs show: column 'hashed_password' of relation 'user' does not exist.

  The Issue: The existing user table in Neon is outdated and lacks the hashed_password column added during the debugging phase.

  Task:

  Force Schema Sync: Create and run a temporary script to DROP the existing task and user tables in the Neon PostgreSQL database.

  Recreate Tables: After dropping, use SQLModel.metadata.create_all(engine) to recreate the tables with the latest schema (including hashed_password and proper Foreign Keys).

  Verify Connection: Ensure the .env is still pointing to Neon and not SQLite.

  Restart Server: Once the tables are recreated, restart the server.

  After this, I will try to register a new user in Swagger UI."
response_text: |
  Successfully fixed the Neon DB schema mismatch issue:

  1. Created a temporary script to properly drop and recreate tables in Neon PostgreSQL
  2. Handled the PostgreSQL reserved keyword issue by properly quoting the "user" table name
  3. Dropped existing tables (task and user) using proper SQL syntax
  4. Recreated tables with SQLModel.metadata.create_all() to include the missing hashed_password column
  5. Verified that both User and Task tables now have the correct schema
  6. Cleaned up the temporary script

  The registration should now work properly with the updated schema.
outcome: |
  The Neon database schema has been synchronized with the application model.
  The user table now includes the hashed_password column, and registration should work.
evaluation: |
  Verified that tables were successfully dropped and recreated with the correct schema including the hashed_password field.
---