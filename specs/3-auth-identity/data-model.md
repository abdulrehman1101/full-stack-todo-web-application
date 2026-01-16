# Data Model: Authentication & Identity (Better Auth + JWT)

## Overview
This document describes the data structures and relationships for the authentication system, focusing on how authenticated users map to existing database models and how JWT tokens carry user identity information.

## Core Entities

### User
**Source**: Extends existing User model from Spec 1 (Neon DB)

**Attributes**:
- `id`: UUID (Primary Key) - Uniquely identifies the user across the system
- `email`: String - Primary authentication identifier (unique, validated)
- `created_at`: DateTime - Timestamp of account creation
- `updated_at`: DateTime - Timestamp of last account update (optional addition)

**Relationships**:
- Related to Task entities via `user_id` foreign key (established in Spec 1)
- May relate to future entities in subsequent specs

**Validation Rules**:
- Email must follow RFC 5322 standard format
- Email must be unique across all users
- Email length must be between 5 and 255 characters
- Account must be registered before authentication

### JWT Token
**Type**: Serialized authentication token (JSON Web Token)

**Payload Claims**:
- `sub`: Subject (user ID) - Maps to User.id in database
- `email`: User email - Verification information from User.email
- `iat`: Issued At - Unix timestamp when token was generated
- `exp`: Expiration Time - Unix timestamp when token expires
- `jti`: JWT ID - Unique identifier for token revocation (optional)

**Structure**:
- Header: Algorithm and token type (typically HS256)
- Payload: Claims containing user identity information
- Signature: HMAC-SHA256 using BETTER_AUTH_SECRET

**Validation Requirements**:
- Token signature must match BETTER_AUTH_SECRET
- Current time must be before expiration (exp claim)
- Subject (sub) must correspond to valid User record
- Audience claim (aud) should match application identifier

### Authentication Session
**Conceptual**: Runtime state representing an active user session

**Attributes**:
- `user_id`: UUID - Reference to authenticated User entity
- `token_expires_at`: DateTime - Expiration time for current session
- `authenticated_at`: DateTime - Timestamp when session began
- `permissions`: Array<String> - List of user permissions/scopes

**Lifecycle**:
- Created during successful authentication
- Validated on each protected request
- Expires according to JWT expiration claims
- Invalidated on logout or token expiration

## Relationships and Constraints

### User ↔ JWT Token
- One-to-many relationship: One user can have multiple simultaneous JWT tokens
- Foreign Key Constraint: JWT `sub` claim must match existing User `id`
- Validation: User must exist and be active at time of token verification

### JWT Token ↔ Protected Resources
- Access Control: Token grants access to user-specific resources only
- Isolation: Users can only access resources linked to their user_id
- Validation: Backend verifies token authenticity before processing requests

### User ↔ Application Data
- Ownership: All user-specific data is linked via user_id foreign key
- Enforcement: Backend applies user_id filter on all database queries
- Security: Users cannot access other users' data regardless of direct API calls

## API Data Transitions

### Registration → User Creation
```
Input: { email: "user@example.com", password: "securePassword123" }
Processing: Validate email format, hash password, create User record
Output: { id: "uuid-123", email: "user@example.com", created_at: "timestamp" }
```

### Login → JWT Generation
```
Input: { email: "user@example.com", password: "securePassword123" }
Processing: Authenticate credentials, validate User exists, generate JWT
Output: { accessToken: "eyJhb...token...", refreshToken: "refreshToken..." }
```

### API Request → JWT Verification
```
Input: Authorization: "Bearer eyJhb...token..."
Processing: Decode JWT, verify signature, validate expiration, extract user_id
Output: authenticated_user_id (for use in database queries)
```

## State Transitions

### Authentication Flow
1. **Unauthenticated** → User visits login page
2. **Credentials Submitted** → User enters email/password
3. **Validated** → Credentials verified against User table
4. **Authenticated** → JWT token generated and returned
5. **Active Session** → Token used for API requests with user context
6. **Expired/Logged Out** → Session invalidated, back to unauthenticated

### Token Lifecycle
- **Generated**: During successful login with Better Auth
- **Transmitted**: Sent from frontend to backend in Authorization header
- **Verified**: Signature and claims validated by FastAPI middleware
- **Applied**: User context extracted and used for data access
- **Expired**: Token becomes invalid after expiration time
- **Refreshed**: New token issued when refresh mechanism is triggered

## Validation Rules

### At Registration
- Email uniqueness enforced at database level
- Email format validated using standard regex patterns
- Password strength validated (minimum requirements)
- Duplicate registration attempts rejected gracefully

### At Authentication
- JWT signature verified using BETTER_AUTH_SECRET
- Token expiration checked against current time
- User existence verified in database
- User account status validated (active/inactive/banned)

### At API Access
- Valid JWT required for all protected endpoints
- User ID from token must match data access restrictions
- Token validity confirmed before database operations
- 401 Unauthorized returned for invalid/missing tokens