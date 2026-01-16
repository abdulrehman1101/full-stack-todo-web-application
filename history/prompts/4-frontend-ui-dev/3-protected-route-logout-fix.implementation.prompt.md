---
id: 3
title: "Protected Route Logout Error Fix"
stage: "implementation"
date_iso: "2026-01-15"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "4-frontend-ui-dev"
branch: "3-auth-identity"
user: "claude"
command: "/sp.implement I am still seeing a React error in the console during logout (see 179.PNG): Cannot update a component ('Router') while rendering a different component ('ProtectedRoute'). Task: Refactor ProtectedRoute Navigation File: frontend/src/components/auth/ProtectedRoute.tsx. The Fix: Ensure that the redirect to /login happens inside a useEffect hook, not directly in the component's body. Logic: > - Keep the loading spinner visible if loading is true. If !isAuthenticated and !loading, use useEffect to trigger router.replace('/login'). Why: This ensures the component finishes its render cycle before the Router tries to change the page, which is the correct React pattern. Please apply this fix so the console stays clean and the app remains stable during logout."
labels: ["auth", "routing", "navigation", "error-fix", "logout"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - E:\gemini cli\hackathon-todo-app\frontend\src\components\auth\ProtectedRoute.tsx
tests_yaml: []
---

# Protected Route Logout Error Fix

## User Input
```
I am still seeing a React error in the console during logout (see 179.PNG): Cannot update a component ('Router') while rendering a different component ('ProtectedRoute').

Task: Refactor ProtectedRoute Navigation

File: frontend/src/components/auth/ProtectedRoute.tsx.

The Fix: Ensure that the redirect to /login happens inside a useEffect hook, not directly in the component's body.

Logic: > - Keep the loading spinner visible if loading is true.

If !isAuthenticated and !loading, use useEffect to trigger router.replace('/login').

Why: This ensures the component finishes its render cycle before the Router tries to change the page, which is the correct React pattern.

Please apply this fix so the console stays clean and the app remains stable during logout.
```

## Response Summary
Successfully fixed the logout error in ProtectedRoute.tsx by ensuring that navigation happens asynchronously after the render cycle. The key changes were:

1. Maintained the useEffect hook for navigation logic to ensure it runs after rendering
2. Changed the component to return null instead of a loading spinner when user is not authenticated and loading is complete
3. This prevents the conflict between rendering content and performing navigation simultaneously

The implementation now properly follows React's lifecycle by separating rendering logic from side effects (navigation).

## Outcome
The "Cannot update a component ('Router') while rendering a different component ('ProtectedRoute')" error is now resolved. The ProtectedRoute component properly handles logout scenarios by allowing the render cycle to complete before triggering navigation, resulting in a clean console and stable application behavior during logout.