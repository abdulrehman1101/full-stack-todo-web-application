---
id: 001
title: "Fix Auth Export and Production Environment Variables"
stage: "refactor"
date_iso: "2026-01-17"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "claude"
command: "/sp.implement"
labels: ["auth", "environment", "configuration", "deployment"]
spec: null
ticket: null
adr: null
pr: null
files_yaml:
  - "frontend/src/lib/auth.ts"
  - "frontend/.env.production"
tests_yaml: []
links: []
prompt_text: |
  Task: Fix Auth Export and Production Environment Variables

  1. Fix Auth Export: In frontend/src/lib/auth.ts, change the auth initialization to a Named Export (export const auth = ...) and remove the export default auth at the bottom. This is required to fix the Vercel build error "Export auth doesn't exist".

  2. Environment Variable Logic:

  Update auth.ts to use process.env.BETTER_AUTH_SECRET for both the main secret and the JWT plugin secret.

  Set the database provider dynamically: use "postgres" if NODE_ENV is production, otherwise "sqlite".

  3. Production Env Cleanup: Update .env.production with these correct mappings:

  NEXT_PUBLIC_API_BASE_URL: https://abdulrehman2-todowebapp-backend.hf.space.

  BETTER_AUTH_URL: [Your Vercel App URL].

  BETTER_AUTH_SECRET: "ZUu822SMcByw8CNnTkOBe4NO5ElvkcCP".

  Note: Do not include localhost:3000 in the production file.
response_text: |
  Successfully implemented all required changes:

  1. Fixed auth export in frontend/src/lib/auth.ts:
     - Changed from default export to named export (export const auth)
     - Removed the export default auth statement
     - Updated to use process.env.BETTER_AUTH_SECRET for both main secret and JWT plugin secret
     - Set database provider dynamically: "postgres" in production, "sqlite" otherwise

  2. Updated .env.production file:
     - Updated NEXT_PUBLIC_API_BASE_URL to https://abdulrehman2-todowebapp-backend.hf.space
     - Set BETTER_AUTH_URL to [Your Vercel App URL] (removed localhost reference)
     - Set BETTER_AUTH_SECRET to ZUu822SMcByw8CNnTkOBe4NO5ElvkcCP
     - Removed incorrect localhost reference
outcome: "Successfully fixed the Vercel build error by changing from default export to named export in auth.ts, updated environment variables to use proper production values, and configured dynamic database provider selection."
evaluation: "All tasks completed successfully. The changes should resolve the Vercel build error and properly configure the production environment."
---

# Fix Auth Export and Production Environment Variables

## Summary of Changes

Successfully implemented all required changes to fix the Vercel build error and properly configure production environment variables:

### 1. Auth Export Fix (`frontend/src/lib/auth.ts`)
- Changed from `export default auth` to `export const auth = betterAuth({...})`
- Updated to use `process.env.BETTER_AUTH_SECRET` for both main secret and JWT plugin secret
- Implemented dynamic database provider selection: "postgres" in production, "sqlite" otherwise

### 2. Production Environment Configuration (`frontend/.env.production`)
- Updated `NEXT_PUBLIC_API_BASE_URL` to `https://abdulrehman2-todowebapp-backend.hf.space`
- Set `BETTER_AUTH_URL` to `[Your Vercel App URL]` (removed localhost reference)
- Set `BETTER_AUTH_SECRET` to `ZUu822SMcByw8CNnTkOBe4NO5ElvkcCP`
- Removed localhost reference to ensure clean production configuration

## Result
These changes should resolve the Vercel build error "Export auth doesn't exist" and properly configure the application for production deployment.