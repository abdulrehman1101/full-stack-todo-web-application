---
description: "Task list for database foundation and schema implementation"
---

# Tasks: Phase II - Spec 1: Database Foundation & Schema

**Input**: Design documents from `/specs/2-db-foundation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- **Backend**: `backend/src/database/`, `backend/src/config/`
- Paths shown below assume web app structure - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure per implementation plan
- [x] T002 [P] Initialize Python project with requirements.txt/pyproject.toml
- [x] T003 [P] Create .env.example file with DATABASE_URL placeholder
- [x] T004 [P] Add sqlmodel dependency using uv
- [x] T005 [P] Add psycopg2-binary dependency using uv
- [x] T006 [P] Add python-dotenv dependency using uv
- [x] T007 [P] Add uuid dependency using uv

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Create backend/src/config/settings.py for environment variable management
- [x] T009 Create backend/src/database/__init__.py
- [x] T010 Create backend/src/database/engine.py for database engine initialization
- [x] T011 Create backend/src/database/session.py for session management
- [x] T012 Create backend/src/database/models/__init__.py
- [x] T013 Create backend/src/database/models/user.py stub file
- [x] T014 Create backend/src/database/models/task.py stub file

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Persistent User Data Storage (Priority: P1) 🎯 MVP

**Goal**: Enable persistent storage of user data in Neon PostgreSQL database with proper model definition and database connectivity

**Independent Test**: Create User records in the database and verify they persist across application restarts, delivering the core capability of persistent user data storage.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T015 [P] [US1] Contract test for user model validation in tests/contract/test_user_model.py
- [ ] T016 [P] [US1] Integration test for database connection in tests/integration/test_database_connection.py

### Implementation for User Story 1

- [x] T017 [P] [US1] Implement User model with id, email, created_at fields in backend/src/database/models/user.py
- [x] T018 [US1] Add validation rules to User model (email format, uniqueness)
- [x] T019 [US1] Implement SQLModel compliance for User model
- [x] T020 [US1] Create database initialization script to create tables in backend/src/database/init_db.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Persistent Task Data Storage (Priority: P1)

**Goal**: Enable persistent storage of task data with proper user associations in Neon PostgreSQL database

**Independent Test**: Create Task records linked to users and verify they persist across application restarts, delivering the core capability of persistent task management.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T021 [P] [US2] Contract test for task model validation in tests/contract/test_task_model.py
- [ ] T022 [P] [US2] Integration test for user-task relationship in tests/integration/test_user_task_relationship.py

### Implementation for User Story 2

- [x] T023 [P] [US2] Implement Task model with id, user_id, description, is_completed, created_at fields in backend/src/database/models/task.py
- [x] T024 [US2] Add validation rules to Task model (required fields, foreign key constraints)
- [x] T025 [US2] Implement foreign key relationship between Task and User models
- [x] T026 [US2] Add SQLModel compliance for Task model

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Database Connection Management (Priority: P2)

**Goal**: Establish reliable database connections using Neon Serverless PostgreSQL with proper configuration management

**Independent Test**: Establish connections to the Neon database and perform basic operations, delivering the core capability of database connectivity.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [x] T027 [P] [US3] Contract test for database connection health check in tests/contract/test_db_health.py

### Implementation for User Story 3

- [x] T028 [US3] Configure database engine with Neon connection string in backend/src/database/engine.py
- [x] T029 [US3] Implement connection pooling configuration for Neon Serverless PostgreSQL
- [x] T030 [US3] Create database session context manager in backend/src/database/session.py
- [x] T031 [US3] Add environment variable validation for database credentials in backend/src/config/settings.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - ORM Model Validation (Priority: P2)

**Goal**: Ensure all database models are SQLModel-compliant to serve both database schema and API validation purposes

**Independent Test**: Validate that models properly represent required data structures and can be used for both database operations and API validation.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [x] T032 [P] [US4] Contract test for SQLModel compliance in tests/contract/test_sqlmodel_compliance.py

### Implementation for User Story 4

- [x] T033 [US4] Validate User model complies with SQLModel standards in backend/src/database/models/user.py
- [x] T034 [US4] Validate Task model complies with SQLModel standards in backend/src/database/models/task.py
- [x] T035 [US4] Test schema generation and validation for both models
- [x] T036 [US4] Verify models can be used for both database schema and API validation

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Testing & Validation Tasks

**Goal**: Implement connection health checks and verify schema in Neon console

- [x] T037 [P] Write connection health check function in backend/src/database/health_check.py
- [x] T038 Create database validation script to verify schema in Neon console
- [x] T039 [P] Add database connectivity tests to tests/integration/test_db_connectivity.py
- [x] T040 Run schema verification against live Neon instance

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T041 [P] Documentation updates in docs/
- [x] T042 Code cleanup and refactoring
- [x] T043 Performance optimization for database queries
- [x] T044 [P] Additional unit tests in tests/unit/
- [x] T045 Security validation for database access
- [x] T046 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on User model (US1) for foreign key relationship
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Depends on models from US1 and US2

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 2

```bash
# Launch all models for User Story 2 together:
Task: "Implement Task model with id, user_id, description, is_completed, created_at fields in backend/src/database/models/task.py"
Task: "Add validation rules to Task model (required fields, foreign key constraints)"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2 (after US1 foundation is complete)
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence