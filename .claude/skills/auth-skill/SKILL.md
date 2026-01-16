---
name: auth-skill
description: Use this Skill when building authentication systems including signup, signin, password hashing, JWT-based auth, and Better Auth integration.
---

# Auth Skill – Signup, Signin, Password Hashing, JWT & Better Auth

## Instructions

Follow these steps whenever authentication functionality is required in an application.

### 1. User Signup
- Validate user input (email, password, username, etc.)
- Ensure email uniqueness
- Hash the password before saving it to the database
- Store user data securely

### 2. Password Hashing
- Never store plain text passwords
- Use a strong hashing algorithm (bcrypt, argon2)
- Add salt automatically via the hashing library
- Compare hashed passwords during signin

### 3. User Signin
- Verify user exists
- Compare provided password with stored hash
- Reject invalid credentials
- Proceed only on successful authentication

### 4. JWT Token Generation
- Generate JWT after successful signin
- Include user ID and role in payload
- Set token expiration
- Sign token with a secure secret key

### 5. JWT Verification
- Validate token on protected routes
- Handle expired or invalid tokens
- Attach user data to request context

### 6. Better Auth Integration
- Configure Better Auth provider
- Use Better Auth for session handling
- Integrate with existing JWT or cookie-based auth
- Follow Better Auth security best practices

### 7. Security Best Practices
- Use HTTPS
- Store secrets in environment variables
- Rotate JWT secrets periodically
- Implement refresh tokens if needed

---

**Use this Skill whenever authentication, authorization, or secure user access is required in a project.**
