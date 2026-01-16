# Tasks: Authentication & Identity (Better Auth + JWT)

**Feature**: Authentication & Identity Implementation
**Branch**: `3-auth-identity`
**Created**: 2026-01-13
**Source Plan**: [specs/3-auth-identity/plan.md](specs/3-auth-identity/plan.md)
**Dependencies**: [specs/3-auth-identity/spec.md](specs/3-auth-identity/spec.md), [specs/2-db-foundation/spec.md](specs/2-db-foundation/spec.md)

## Phase 1: Environment & Setup

**Goal**: Establish development environment and install required dependencies for both frontend and backend services.

- [X] T001 Install PyJWT in backend via uv (backend/requirements.txt)
- [X] T002 [P] Install python-jose in backend via uv (backend/requirements.txt)
- [X] T003 Initialize frontend directory structure if not already present (frontend/package.json)
- [X] T004 [P] Install better-auth in frontend (frontend/package.json)
- [X] T005 [P] Install @better-auth/node in frontend (frontend/package.json)
- [X] T006 Add BETTER_AUTH_SECRET to backend .env file (backend/.env)
- [X] T007 [P] Add BETTER_AUTH_SECRET to frontend .env.local file (frontend/.env.local)
- [X] T008 [P] Create .env.example with sample secrets (backend/.env.example, frontend/.env.example)

## Phase 2: Foundational Components

**Goal**: Create foundational authentication components that will be used by all user stories.

- [X] T009 Create backend auth utils module for JWT operations (backend/src/auth/utils.py)
- [X] T010 [P] Create backend auth middleware module (backend/src/auth/middleware.py)
- [X] T011 [P] Create backend auth schemas module (backend/src/auth/schemas.py)
- [X] T012 [P] Create frontend auth configuration (frontend/src/lib/auth.ts)
- [X] T013 [P] Create frontend API client module (frontend/src/services/api-client.ts)
- [X] T014 [P] Create frontend auth hook (frontend/src/hooks/useAuth.ts)
- [X] T015 Update backend deps module to include auth dependency (backend/src/api/deps.py)

## Phase 3: User Story 1 - User Registration and Login (P1)

**Goal**: Implement user registration and login functionality with JWT token generation.

**Independent Test**: Can be fully tested by registering a new user, logging in, and accessing a protected resource to verify the authentication flow works end-to-end.

- [X] T016 [US1] Create Better Auth API routes in Next.js (frontend/src/app/api/auth/[[...auth]]/route.ts)
- [X] T017 [P] [US1] Create Login component (frontend/src/components/auth/Login.tsx)
- [X] T018 [P] [US1] Create Register component (frontend/src/components/auth/Register.tsx)
- [X] T019 [P] [US1] Configure Better Auth with JWT plugin (frontend/src/lib/auth.ts)
- [X] T020 [US1] Implement JWT token generation in Better Auth (frontend/src/lib/auth.ts)
- [ ] T021 [US1] Test user registration flow with email/password (frontend/src/components/auth/Register.test.tsx)
- [ ] T022 [P] [US1] Test user login flow with JWT token retrieval (frontend/src/components/auth/Login.test.tsx)

## Phase 4: User Story 2 - Secure API Access (P1)

**Goal**: Implement JWT token verification middleware on backend to protect API endpoints.

**Independent Test**: Can be fully tested by making API requests with valid/invalid tokens and verifying appropriate access control.

- [X] T023 [US2] Implement JWT decoding and verification logic (backend/src/auth/utils.py)
- [X] T024 [US2] Create FastAPI dependency for JWT verification (backend/src/auth/middleware.py)
- [X] T025 [US2] Update existing API endpoints to require authentication (backend/src/api/deps.py)
- [X] T026 [P] [US2] Create protected API endpoint example (backend/src/api/v1/endpoints/users.py)
- [X] T027 [US2] Implement 401 Unauthorized response for invalid tokens (backend/src/auth/middleware.py)
- [ ] T028 [P] [US2] Test valid JWT access to protected endpoints (backend/tests/integration/test_auth_valid.py)
- [ ] T029 [P] [US2] Test invalid JWT returns 401 Unauthorized (backend/tests/integration/test_auth_invalid.py)
- [ ] T030 [P] [US2] Test missing JWT returns 401 Unauthorized (backend/tests/integration/test_auth_missing.py)

## Phase 5: User Story 3 - Session Management (P2)

**Goal**: Implement session persistence and management across browser sessions.

**Independent Test**: Can be tested by logging in, refreshing the browser, navigating to different pages, and verifying the session remains active.

- [X] T031 [US3] Implement JWT token storage in frontend (frontend/src/hooks/useAuth.ts)
- [X] T032 [P] [US3] Implement token refresh mechanism (frontend/src/hooks/useAuth.ts)
- [X] T033 [P] [US3] Create ProtectedRoute component (frontend/src/components/auth/ProtectedRoute.tsx)
- [X] T034 [US3] Implement token expiration handling (frontend/src/hooks/useAuth.ts)
- [X] T035 [P] [US3] Update API client to include JWT in requests (frontend/src/services/api-client.ts)
- [ ] T036 [P] [US3] Test session persistence after browser refresh (frontend/src/components/auth/ProtectedRoute.test.tsx)
- [ ] T037 [P] [US3] Test expired token redirect to login (frontend/src/components/auth/ProtectedRoute.test.tsx)

## Phase 6: Integration & Validation

**Goal**: Complete integration between frontend and backend authentication systems and validate end-to-end flow.

- [X] T038 Configure frontend API client to automatically attach JWT Bearer token (frontend/src/services/api-client.ts)
- [X] T039 [P] Test complete end-to-end flow: Login -> Token Storage -> Authorized API Call (integration/test_e2e_auth.py)
- [X] T040 [P] Verify extracted user_id matches Neon DB record (backend/src/auth/middleware.py)
- [X] T041 Update backend database queries to filter by authenticated user_id (backend/src/database/crud.py)
- [X] T042 [P] Test user data isolation - users can't access others' data (backend/tests/integration/test_data_isolation.py)
- [X] T043 [P] Test JWT token verification performance <100ms (backend/tests/performance/test_jwt_perf.py)

## Phase 7: Testing & Validation

**Goal**: Comprehensive testing to ensure all authentication requirements are met.

- [X] T044 [P] Write backend tests for 401 Unauthorized on missing/invalid tokens (backend/tests/unit/test_auth_middleware.py)
- [X] T045 [P] Write tests for BETTER_AUTH_SECRET validation (backend/tests/unit/test_secret_validation.py)
- [X] T046 [P] Write tests for JWT token structure validation (backend/tests/unit/test_jwt_structure.py)
- [X] T047 [P] Write tests for user registration constraints (backend/tests/unit/test_user_registration.py)
- [X] T048 [P] Write tests for email format validation (frontend/src/components/auth/Register.test.tsx)
- [X] T049 [P] Write tests for password strength validation (frontend/src/components/auth/Register.test.tsx)

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Final touches, documentation, and security hardening.

- [X] T050 Update README with authentication setup instructions (backend/README.md, frontend/README.md)
- [X] T051 [P] Add security headers to authentication responses (backend/src/api/main.py)
- [X] T052 [P] Implement rate limiting for authentication endpoints (backend/src/api/v1/endpoints/auth.py)
- [X] T053 [P] Add logging for authentication events (backend/src/auth/middleware.py)
- [X] T054 [P] Add error handling for token tampering (backend/src/auth/utils.py, backend/src/auth/middleware.py)
- [X] T055 [P] Update database models to support authentication audit trail (backend/src/database/models/user.py)
- [X] T056 [P] Add environment-specific configurations (backend/.env.production, frontend/.env.production)

## Dependencies

**User Story 1 Dependencies**: Phase 1 (Environment & Setup), Phase 2 (Foundational Components)

**User Story 2 Dependencies**: Phase 1 (Environment & Setup), Phase 2 (Foundational Components), User Story 1 (Registration/Login)

**User Story 3 Dependencies**: Phase 1 (Environment & Setup), Phase 2 (Foundational Components), User Story 1 (Registration/Login)

**User Story 2 can begin after User Story 1 is partially complete**: Once JWT generation is implemented, verification can be developed in parallel.

## Parallel Execution Opportunities

- **[P] tasks**: All tasks marked with [P] can be executed in parallel with other tasks that don't modify the same files
- **Frontend vs Backend**: Frontend and backend tasks can be executed in parallel (e.g., T016-T022 with T023-T030)
- **Component Creation**: Login, Register, and ProtectedRoute components can be created in parallel (T017, T018, T033)
- **Testing**: Multiple test files can be written in parallel once implementation is complete (T021, T022, T028, T029, etc.)

## Implementation Strategy

**MVP Scope**: Complete User Story 1 (Registration/Login) and minimal User Story 2 (Basic JWT verification) to establish core authentication flow.

**Incremental Delivery**:
- MVP: Registration, login, and basic protected endpoint access
- Phase 2: Session persistence and token refresh
- Phase 3: Advanced security features and performance optimizations