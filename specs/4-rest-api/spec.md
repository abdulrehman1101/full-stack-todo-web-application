# Specification: RESTful API Development (CRUD Logic)

## Overview

A secure, authenticated RESTful API for task management that provides full CRUD operations while ensuring complete data isolation between users. The API leverages JWT-based authentication to maintain user sessions and restricts data access based on user identity.

**Target Audience**: Backend developers and API consumers

**Feature Number**: 4
**Status**: Draft
**Created**: 2026-01-14
**Last Updated**: 2026-01-14

## User Scenarios & Testing

### Primary User Flows

**Scenario 1: Task Management Workflow**
- As an authenticated user, I want to manage my personal tasks through API calls
- Given I am logged in with a valid JWT token
- When I make API requests to create, read, update, or delete tasks
- Then I should only see and modify my own tasks
- And I should receive appropriate HTTP status codes for each operation

**Scenario 2: Secure Data Access**
- As a security-conscious user, I want to ensure my tasks are protected from other users
- Given the API is properly authenticated
- When another user attempts to access my tasks using their token
- Then they should receive a 404 Not Found response
- And my data should remain completely isolated

### Edge Cases
- Invalid JWT tokens should return 401 Unauthorized
- Malformed request bodies should return 422 Unprocessable Entity
- Requests for non-existent tasks should return 404 Not Found
- Requests for tasks owned by other users should return 404 Not Found (not 403 Forbidden to prevent data enumeration)

## Functional Requirements

### FR-001: Task Creation
- **Requirement**: The system must allow authenticated users to create new tasks
- **Acceptance Criteria**:
  - When a POST request is made to `/api/tasks` with a valid JWT token and task data, a new task must be created for the authenticated user
  - The task must be associated with the user ID extracted from the JWT token
  - The API must return a 201 Created status with the created task data
  - Request validation must ensure required fields are present

### FR-002: Task Retrieval (List)
- **Requirement**: The system must allow authenticated users to retrieve all their tasks
- **Acceptance Criteria**:
  - When a GET request is made to `/api/tasks` with a valid JWT token, only tasks belonging to the authenticated user must be returned
  - The API must return a 200 OK status with an array of the user's tasks
  - No tasks from other users should be included in the response

### FR-003: Task Detail Retrieval
- **Requirement**: The system must allow authenticated users to retrieve a specific task
- **Acceptance Criteria**:
  - When a GET request is made to `/api/tasks/{id}` with a valid JWT token, only return the task if it belongs to the authenticated user
  - The API must return 200 OK with the task data if the task exists and belongs to the user
  - The API must return 404 Not Found if the task doesn't exist OR doesn't belong to the user
  - The API must return 401 Unauthorized if the JWT token is invalid

### FR-004: Task Update
- **Requirement**: The system must allow authenticated users to update their tasks
- **Acceptance Criteria**:
  - When a PUT request is made to `/api/tasks/{id}` with a valid JWT token and updated task data, only update the task if it belongs to the authenticated user
  - The API must return 200 OK with the updated task data if successful
  - The API must return 404 Not Found if the task doesn't exist OR doesn't belong to the user
  - Request validation must ensure data integrity during updates

### FR-005: Task Deletion
- **Requirement**: The system must allow authenticated users to delete their tasks
- **Acceptance Criteria**:
  - When a DELETE request is made to `/api/tasks/{id}` with a valid JWT token, only delete the task if it belongs to the authenticated user
  - The API must return 200 OK with a success message if deletion is successful
  - The API must return 404 Not Found if the task doesn't exist OR doesn't belong to the user
  - The deleted task must no longer be accessible via any API endpoint

### FR-006: Task Completion Toggle
- **Requirement**: The system must allow authenticated users to toggle the completion status of their tasks
- **Acceptance Criteria**:
  - When a PATCH request is made to `/api/tasks/{id}/complete` with a valid JWT token, only toggle the completion status if the task belongs to the authenticated user
  - The API must return 200 OK with the updated task data reflecting the new completion status
  - The API must return 404 Not Found if the task doesn't exist OR doesn't belong to the user

### FR-007: Data Isolation
- **Requirement**: The system must ensure complete data isolation between users
- **Acceptance Criteria**:
  - Under no circumstances should a user be able to access, modify, or delete another user's tasks
  - All database queries must be filtered by the user ID extracted from the JWT token
  - When a user attempts to access a task that doesn't belong to them, the system must return 404 Not Found (not 403 Forbidden) to prevent data enumeration

### FR-008: Authentication & Authorization
- **Requirement**: The system must authenticate all requests except health checks
- **Acceptance Criteria**:
  - All task-related endpoints must require a valid JWT token
  - Invalid or missing tokens must result in 401 Unauthorized responses
  - Tokens must be validated against the established JWT authentication system from Spec 2
  - Health check endpoints (if any) should remain accessible without authentication

### FR-009: Validation & Error Handling
- **Requirement**: The system must provide appropriate validation and error handling
- **Acceptance Criteria**:
  - Proper HTTP status codes must be returned (200 OK, 201 Created, 401 Unauthorized, 404 Not Found, 422 Unprocessable Entity)
  - Request bodies must be validated using appropriate schema validation
  - Error responses must include meaningful error messages without exposing system internals
  - Validation failures must return appropriate error codes and messages

### FR-010: Persistence
- **Requirement**: The system must persist all task data to the Neon PostgreSQL database
- **Acceptance Criteria**:
  - All task operations must be backed by the Neon Serverless PostgreSQL database
  - Data must survive application restarts
  - Database transactions must be used appropriately to ensure data consistency
  - SQLModel must be used for all database interactions

## Non-Functional Requirements

### Security
- All endpoints (except health checks) must require valid JWT authentication
- Data isolation must be maintained at the application layer
- No sensitive information should be exposed in error messages
- Rate limiting should be applied to prevent abuse (inherit from authentication system)

### Performance
- API responses should be delivered within 500ms under normal load
- The system should handle at least 100 concurrent authenticated users
- Database queries should be optimized to prevent N+1 problems

### Scalability
- The API should be stateless and horizontally scalable
- JWT-based authentication should not require server-side session storage
- Database connections should be managed efficiently

## Success Criteria

### Quantitative Metrics
- **SC-001**: 100% of authenticated API requests successfully return user-specific data with proper data isolation
- **SC-002**: All 6 required endpoints (GET, POST, GET by ID, PUT, DELETE, PATCH) must be fully functional with appropriate HTTP status codes
- **SC-003**: Response times for all endpoints must be under 500ms for 95% of requests under normal load
- **SC-004**: Data isolation must be 100% effective - no user should ever access another user's data

### Qualitative Measures
- **SC-005**: API consumers should find the endpoints intuitive and well-documented
- **SC-006**: Error handling should provide clear, actionable feedback to API consumers
- **SC-007**: Authentication integration should be seamless with existing JWT infrastructure
- **SC-008**: System should handle edge cases gracefully without exposing sensitive information

## Key Entities

### Task Entity
- **Description**: Represents a user's individual task with description, completion status, and metadata
- **Attributes**:
  - ID (UUID): Unique identifier for the task
  - User ID (UUID): Reference to the owner user
  - Description (Text): The task content/description
  - Is Completed (Boolean): Status indicating completion
  - Created At (DateTime): Timestamp of creation
  - Updated At (DateTime): Timestamp of last modification

### User Entity
- **Description**: Represents an authenticated user in the system
- **Attributes**:
  - ID (UUID): Unique identifier for the user
  - Email (String): User's email address
  - Created At (DateTime): Timestamp of account creation
  - Last Login At (DateTime): Timestamp of last login
  - Updated At (DateTime): Timestamp of last activity

## Constraints & Limitations

### Technical Constraints
- Backend must use FastAPI with Python 3.13+
- Database interactions must use SQLModel ORM
- All endpoints must require JWT token authentication (except health checks)
- Must integrate with existing authentication system from Spec 2
- Data isolation must be implemented at the application layer

### Scope Limitations
- No advanced filtering (search by keyword, date ranges, etc.) in this MVP
- No task sharing between users
- No bulk operations (bulk create, update, delete)
- No task categorization or tagging
- No task assignment or collaboration features

### Not Building
- Frontend UI or CSS (reserved for Spec 4)
- Advanced reporting or analytics
- Email notifications or reminders
- File attachments or rich media
- Third-party integrations

## Assumptions

- The authentication system from Spec 2 is fully functional and available
- The Neon PostgreSQL database is properly configured and accessible
- SQLModel models for User and Task entities are already defined and working
- JWT token extraction and validation utilities are available from previous specs
- The API will follow RESTful conventions and best practices
- Basic health check endpoints exist or will be implemented separately

## Dependencies

- **Spec 1**: Todo Application foundation and CLI interface
- **Spec 2**: Database Foundation with User and Task models
- **Spec 3**: Authentication & Identity with JWT token system
- **Neon PostgreSQL**: Cloud database service for data persistence
- **SQLModel**: ORM for database interactions
- **FastAPI**: Web framework for API development
- **Better Auth**: Authentication provider for JWT generation