---
id: 4
title: "Fix Auth Provider Context Error"
stage: "general"
date_iso: "2026-01-15"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "3-auth-identity"
user: "rehman"
command: "sp.implement"
labels: ["frontend", "authentication", "context", "layout"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "frontend/app/layout.tsx"
tests_yaml:
  - "Context error resolved"
  - "Auth provider accessible throughout app"
---

# Prompt History Record

## Original Prompt
```
I am getting a runtime error: useAuth must be used within an AuthProvider when navigating to /login or /register.

The Problem: > The AuthProvider was created in Phase 3 but it hasn't been wrapped around the application in the root layout.

Task:

Update Root Layout: Go to frontend/src/app/layout.tsx.

Import AuthProvider: Import { AuthProvider } from @/contexts/AuthContext.

Wrap Children: Wrap the {children} and other components (like Navbar) inside the <AuthProvider> tag.

The structure should look like: <AuthProvider> <ParticlesBackground /> <GlassyNavbar /> {children} <Footer /> </AuthProvider>

Verify: Ensure there are no more context errors when visiting /login or /register.

Please provide the updated layout.tsx code.
```

## Response Summary
Successfully fixed the runtime error by updating the root layout to wrap the application with the AuthProvider:

1. Updated `frontend/app/layout.tsx` to:
   - Import AuthProvider from "@/src/contexts/AuthContext"
   - Import GlassyNavbar from "@/src/components/nav/GlassyNavbar"
   - Import Footer from "@/src/components/footer/Footer"
   - Wrap all application components inside the <AuthProvider> tag
   - Structure now follows: <AuthProvider> <ParticlesBackground /> <GlassyNavbar /> {children} <Footer /> </AuthProvider>

The AuthContext is now available throughout the entire application, resolving the "useAuth must be used within an AuthProvider" error when visiting /login or /register pages.