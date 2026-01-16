# Research: Authentication & Identity (Better Auth + JWT)

## Overview
This research document addresses the technical decisions and best practices needed for implementing the authentication system using Better Auth on the frontend and JWT verification on the FastAPI backend.

## Decision 1: JWT vs. Session-based Authentication

### Rationale
JWT was chosen for this implementation because:
- Stateless architecture supports horizontal scaling of backend services
- Eliminates need for shared session storage across multiple backend instances
- Enables cross-domain authentication between frontend and backend
- Aligns with the project's scalability-driven architecture principle

### Alternatives Considered
- **Traditional Sessions**: Would require shared session storage (Redis/database), creating additional infrastructure complexity
- **OAuth 2.0 Tokens**: More complex for basic email/password authentication, not needed for MVP
- **Cookie-based Auth**: Limited cross-domain capabilities and security considerations

## Decision 2: Better Auth JWT Plugin Configuration

### Rationale
Better Auth's JWT plugin provides:
- Seamless integration with existing Next.js authentication flows
- Built-in security best practices for token generation and validation
- Easy configuration for custom claims and expiration times
- Compatibility with the existing Neon DB User table from Spec 1

### Best Practices Applied
- Use strong secret keys (>32 characters) for token signing
- Set appropriate expiration times (15-30 minutes for access tokens)
- Implement refresh token mechanism for extended sessions
- Secure token transmission via HTTPS only

## Decision 3: Shared Secret Strategy

### Rationale
Using a shared secret (BETTER_AUTH_SECRET) ensures:
- Consistent token signing and verification between frontend and backend
- Secure communication channel between services
- Compliance with security best practices
- Prevention of token forgery attacks

### Security Considerations
- Store secret in environment variables, never in code
- Use different secrets for development and production
- Rotate secrets periodically for enhanced security
- Ensure secret has sufficient entropy (recommended 256-bit minimum)

## Decision 4: FastAPI JWT Verification Approach

### Rationale
FastAPI's dependency injection system combined with HTTPBearer security provides:
- Clean integration with existing FastAPI route handlers
- Automatic 401 response for invalid/missing tokens
- Easy extraction of user identity from JWT claims
- Proper separation of authentication logic from business logic

### Implementation Pattern
- Create custom dependency function that extracts and verifies JWT
- Return authenticated user ID for use in route handlers
- Raise HTTPException(401) for invalid tokens
- Cache decoded token information to avoid repeated verification

## Decision 5: Error Handling Strategy

### Rationale
Proper error handling ensures:
- Clear user feedback for authentication failures
- Security by not revealing specific reasons for failures
- Consistent behavior across all authentication endpoints
- Protection against timing attacks

### Error Types Handled
- Invalid JWT tokens (malformed, expired, incorrect signature)
- Missing Authorization header
- User not found in database after JWT verification
- Expired sessions requiring re-authentication

## Data Flow Architecture

### User Login Flow
1. User submits email/password to Better Auth
2. Better Auth validates credentials against database
3. Better Auth generates signed JWT with user ID claim
4. JWT returned to frontend for storage and use in API requests

### API Request Flow
1. Frontend includes JWT in Authorization header as "Bearer <token>"
2. FastAPI dependency intercepts request and extracts token
3. JWT signature verified using shared secret
4. User ID extracted from token claims
5. User validated against database record
6. Request processed with authenticated user context

## Technology Stack Integration

### Frontend Components
- Better Auth with JWT plugin for user registration/login
- Next.js API routes for authentication endpoints
- Client-side storage of JWT (localStorage/secure cookies)
- API client with automatic token inclusion in requests

### Backend Components
- FastAPI HTTPBearer security dependency
- PyJWT/Jose for token decoding and validation
- Shared secret verification against BETTER_AUTH_SECRET
- SQLModel integration for user lookup from Neon DB

## Security Best Practices Applied

### Token Security
- Use HTTPS for all authentication requests
- Set secure, httpOnly cookies if storing tokens client-side
- Implement token expiration and refresh mechanisms
- Validate token audience and issuer claims

### Implementation Security
- Never log JWT tokens in application logs
- Validate token structure before attempting verification
- Use constant-time comparison for token validation
- Implement rate limiting for authentication endpoints