---
id: 002
title: "Fix Better Auth Export Error"
stage: "refactor"
date_iso: "2026-01-17"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "claude"
command: "/sp.implement"
labels: ["auth", "nextjs", "route-handler", "dependency-update"]
spec: null
ticket: null
adr: null
pr: null
files_yaml:
  - "frontend/app/api/auth/[[...auth]]/route.ts"
tests_yaml: []
links: []
prompt_text: |
  Fix Better-Auth Export Error in Next.js Route Handler

  Error Found: > Export handleAuth doesn't exist in target module "better-auth/next-js". This is because handleAuth has been renamed to toNextJsHandler in the latest version of Better Auth.

  Instructions:

  Open the file: frontend/app/api/auth/[[...auth]]/route.ts.

  Change the import statement from: import { handleAuth } from "better-auth/next-js"; to: import { toNextJsHandler } from "better-auth/next-js";

  Update the export line from: export const { GET, POST } = handleAuth(auth); to: export const { GET, POST } = toNextJsHandler(auth);

  Double-check that auth is correctly imported as a named import from @/src/lib/auth.

  Verification: Ensure that the auth object is exported as a named constant (export const auth = ...) in frontend/src/lib/auth.ts to match this import.
response_text: |
  Successfully fixed the Better-Auth export error in the Next.js route handler:

  1. Updated import statement in frontend/app/api/auth/[[...auth]]/route.ts:
     - Changed from: import { handleAuth } from "better-auth/next-js"
     - Changed to: import { toNextJsHandler } from "better-auth/next-js"

  2. Updated export line in the same file:
     - Changed from: export const { GET, POST } = handleAuth(auth)
     - Changed to: export const { GET, POST } = toNextJsHandler(auth)

  3. Verified that auth is correctly imported as a named import from @/src/lib/auth
  4. Confirmed that auth object is exported as a named constant (export const auth = ...) in frontend/src/lib/auth.ts

  The changes address the API change in Better Auth where handleAuth was renamed to toNextJsHandler in the latest version.
outcome: "Successfully resolved the Better Auth export error by updating the import and usage to the new API (toNextJsHandler) while maintaining the same functionality."
evaluation: "All tasks completed successfully. The route handler should now work correctly with the updated Better Auth API."
---

# Fix Better-Auth Export Error in Next.js Route Handler

## Summary of Changes

Successfully fixed the Better-Auth export error by updating the Next.js route handler to use the new API name:

### Issue
The error occurred because `handleAuth` has been renamed to `toNextJsHandler` in the latest version of Better Auth.

### Solution
Updated `frontend/app/api/auth/[[...auth]]/route.ts`:

1. **Import Statement**:
   - Changed from: `import { handleAuth } from "better-auth/next-js"`
   - Changed to: `import { toNextJsHandler } from "better-auth/next-js"`

2. **Export Line**:
   - Changed from: `export const { GET, POST } = handleAuth(auth)`
   - Changed to: `export const { GET, POST } = toNextJsHandler(auth)`

3. **Verification**:
   - Confirmed that `auth` is correctly imported as a named import from `@/src/lib/auth`
   - Verified that the `auth` object is exported as a named constant (`export const auth = ...`) in `frontend/src/lib/auth.ts`

## Result
The route handler now uses the correct API name and should resolve the build error while maintaining the same authentication functionality.