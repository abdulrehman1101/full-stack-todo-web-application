---
name: backend-skill
description: Use this Skill when building backend systems, creating API routes, handling requests and responses, and connecting applications to databases.
---

# Backend Skill – Routes, Requests, Responses & Database Connection

## Instructions

Follow these steps whenever backend logic or API development is required.

### 1. Project Setup
- Initialize backend framework (Node.js, Express, Fastify, etc.)
- Configure environment variables
- Set up project structure (routes, controllers, services)
- Enable request parsing (JSON, URL-encoded)

### 2. Route Generation
- Define RESTful routes (GET, POST, PUT, DELETE)
- Group routes by resource
- Use clear and consistent naming
- Apply versioning if needed (e.g., `/api/v1`)

### 3. Request Handling
- Validate incoming request data
- Extract params, query, and body safely
- Handle authentication and authorization
- Use middleware for common logic

### 4. Response Handling
- Return consistent response formats
- Use proper HTTP status codes
- Send meaningful error messages
- Avoid exposing sensitive information

### 5. Database Connection
- Configure database client or ORM
- Manage connection pooling
- Handle connection errors gracefully
- Close connections on shutdown

### 6. Database Operations
- Perform CRUD operations
- Use transactions for critical operations
- Prevent SQL injection
- Handle empty or failed queries safely

### 7. Error Handling
- Use centralized error handlers
- Catch async errors properly
- Log errors for debugging
- Return user-friendly error responses

### 8. Best Practices
- Keep controllers thin and logic in services
- Use async/await for readability
- Validate and sanitize input
- Secure APIs with authentication

---

**Use this Skill whenever backend routes, request handling, or database connectivity is required in an application.**