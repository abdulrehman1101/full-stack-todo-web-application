# Quickstart Guide: Authentication & Identity (Better Auth + JWT)

## Overview
This guide provides the essential steps to implement and test the authentication system with Better Auth and JWT verification between Next.js frontend and FastAPI backend.

## Prerequisites
- Node.js 18+ and npm/yarn for frontend development
- Python 3.13+ and pip/uv for backend development
- Access to Neon Serverless PostgreSQL database
- Basic understanding of JWT concepts and OAuth flows

## Environment Setup

### 1. Configure Secrets
Create or update environment files with shared secret:

**Backend (.env)**:
```bash
DATABASE_URL=postgresql://username:password@host:port/dbname
BETTER_AUTH_SECRET=your-32-character-secret-key-here-32chars
```

**Frontend (.env.local)**:
```bash
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_SECRET=your-32-character-secret-key-here-32chars
```

### 2. Install Dependencies
```bash
# Backend
cd backend
pip install better-auth pyjwt python-jose

# Frontend
cd frontend
npm install better-auth @better-auth/node
```

## Implementation Steps

### Step 1: Configure Better Auth (Frontend)
1. Create `src/lib/auth.js` with Better Auth configuration
2. Enable JWT plugin with shared secret
3. Configure email/password authentication provider
4. Set appropriate token expiration times

### Step 2: Create JWT Verification Middleware (Backend)
1. Create `backend/src/auth/middleware.py` with JWT verification logic
2. Implement HTTPBearer security dependency
3. Add user ID extraction from token claims
4. Connect to Neon DB to verify user exists

### Step 3: Update API Dependencies
1. Create authentication dependency in `backend/src/api/deps.py`
2. Inject authenticated user ID into route handlers
3. Apply dependency to all protected endpoints
4. Ensure 401 responses for invalid tokens

### Step 4: Integrate with Existing Models
1. Verify JWT user ID matches existing User records in Neon DB
2. Apply user_id filter to all database queries for data isolation
3. Test that users can only access their own data
4. Validate error handling for invalid tokens

## Testing the Implementation

### 1. Unit Tests
```bash
# Backend JWT verification tests
pytest tests/unit/test_jwt_verification.py

# Frontend authentication flow tests
npm run test src/__tests__/auth-flow.test.js
```

### 2. Integration Tests
```bash
# End-to-end authentication flow
pytest tests/integration/test_auth_flow.py

# Cross-service authentication tests
npm run test src/__tests__/cross-service.test.js
```

### 3. Manual Testing
1. Register a new user via frontend registration form
2. Verify user account is created in Neon DB User table
3. Log in and obtain JWT token from Better Auth
4. Make API request with JWT token to protected endpoint
5. Verify backend accepts token and returns user-specific data
6. Try API request without token - should return 401 Unauthorized
7. Try API request with invalid token - should return 401 Unauthorized

## Key Endpoints

### Frontend Authentication Routes
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User authentication
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - End current session

### Backend Protected Routes
- `GET /api/users/me` - Get authenticated user details
- `GET /api/tasks` - Get user's tasks (requires authentication)
- `POST /api/tasks` - Create new task (requires authentication)
- `PUT /api/tasks/{id}` - Update task (requires authentication)

## Troubleshooting

### Common Issues

**JWT Verification Fails**
- Verify BETTER_AUTH_SECRET matches between frontend and backend
- Check token format: "Bearer <token>" in Authorization header
- Ensure token hasn't expired (check iat and exp claims)

**401 Unauthorized Errors**
- Confirm Authorization header is included in requests
- Validate JWT token is properly formatted
- Check that token was issued by Better Auth

**Cross-Service Communication Problems**
- Verify network connectivity between services
- Check that environment variables are properly loaded
- Confirm shared secret is identical on both services

### Debugging Steps
1. Enable detailed logging in both frontend and backend
2. Verify JWT token structure using jwt.io debugger
3. Check database connectivity and User table contents
4. Validate environment variable configuration
5. Test authentication flow step-by-step

## Security Considerations
- Never log JWT tokens in application logs
- Use HTTPS for all authentication requests
- Implement rate limiting on authentication endpoints
- Regularly rotate BETTER_AUTH_SECRET in production
- Validate token audience and issuer claims