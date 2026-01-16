---
id: 2
title: "Protected Route Navigation Fix"
stage: "implementation"
date_iso: "2026-01-15"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "4-frontend-ui-dev"
branch: "3-auth-identity"
user: "claude"
command: "/sp.implement The mobile UI is already fixed and working great. Now, I only need to fix the logout error: Cannot update a component (Router) while rendering a different component (ProtectedRoute). Task: In src/components/auth/ProtectedRoute.tsx, find the logic that redirects the user to /login. Move the router.push('/login') or router.replace('/login') call inside a useEffect hook. Why: Navigation shouldn't happen during the render phase. Moving it to useEffect ensures the component finishes rendering before the router changes the page. Please apply this fix so the console is clean during logout."
labels: ["auth", "routing", "navigation", "error-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - E:\gemini cli\hackathon-todo-app\frontend\src\components\auth\ProtectedRoute.tsx
tests_yaml: []
---

# Protected Route Navigation Fix

## User Input
```
The mobile UI is already fixed and working great. Now, I only need to fix the logout error: Cannot update a component (Router) while rendering a different component (ProtectedRoute).

Task:

In src/components/auth/ProtectedRoute.tsx, find the logic that redirects the user to /login.

Move the router.push('/login') or router.replace('/login') call inside a useEffect hook.

Why: Navigation shouldn't happen during the render phase. Moving it to useEffect ensures the component finishes rendering before the router changes the page.

Please apply this fix so the console is clean during logout.
```

## Response Summary
Successfully fixed the logout error in ProtectedRoute.tsx by moving the navigation logic from the render phase to a useEffect hook. The original issue occurred because `router.replace('/login')` was being called directly during rendering, which caused React to throw an error about updating a component while rendering a different component.

The fix involved:
1. Importing `useEffect` hook
2. Moving the redirect logic inside a `useEffect` hook that runs when authentication state changes
3. Keeping appropriate loading states to maintain UX during navigation

## Outcome
The ProtectedRoute component now properly handles authentication checks and redirects without triggering the "Cannot update a component (Router) while rendering a different component (ProtectedRoute)" error. The navigation occurs after the component has finished rendering, preventing the console error during logout.