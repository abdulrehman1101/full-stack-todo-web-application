# API Contracts: Task Management Endpoints

## Overview
This document defines the API contracts for the task management REST API, specifying the endpoints, request/response formats, and error handling patterns.

## Base URL
`/api/v1` (versioned API)

## Authentication
All endpoints (except health checks) require JWT Bearer token in Authorization header:
```
Authorization: Bearer <jwt-token>
```

## Common HTTP Status Codes
- `200 OK`: Successful request with response data
- `201 Created`: Successful resource creation
- `400 Bad Request`: Invalid request format or validation error
- `401 Unauthorized`: Invalid or missing JWT token
- `404 Not Found`: Resource not found OR user lacks permission to access resource
- `422 Unprocessable Entity`: Request validation failed

## Endpoints

### 1. List All Tasks
**Endpoint**: `GET /tasks`
**Description**: Retrieve all tasks for the authenticated user
**Authentication**: Required

#### Request
```
GET /api/v1/tasks
Headers:
  Authorization: Bearer <valid-jwt-token>
```

#### Response
**Success (200 OK)**:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "description": "Sample task description",
    "is_completed": false,
    "created_at": "2026-01-14T10:30:00Z",
    "updated_at": "2026-01-14T10:30:00Z"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "description": "Another task",
    "is_completed": true,
    "created_at": "2026-01-14T11:00:00Z",
    "updated_at": "2026-01-14T11:30:00Z"
  }
]
```

### 2. Create New Task
**Endpoint**: `POST /tasks`
**Description**: Create a new task for the authenticated user
**Authentication**: Required

#### Request
```
POST /api/v1/tasks
Headers:
  Authorization: Bearer <valid-jwt-token>
  Content-Type: application/json

Body:
{
  "description": "New task description"
}
```

#### Request Validation
- `description` is required
- `description` must be 5-500 characters
- `description` cannot be empty or whitespace-only

#### Response
**Success (201 Created)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "description": "New task description",
  "is_completed": false,
  "created_at": "2026-01-14T12:00:00Z",
  "updated_at": "2026-01-14T12:00:00Z"
}
```

### 3. Get Specific Task
**Endpoint**: `GET /tasks/{id}`
**Description**: Retrieve details of a specific task
**Authentication**: Required

#### Request
```
GET /api/v1/tasks/550e8400-e29b-41d4-a716-446655440002
Headers:
  Authorization: Bearer <valid-jwt-token>
```

#### Response
**Success (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "description": "New task description",
  "is_completed": false,
  "created_at": "2026-01-14T12:00:00Z",
  "updated_at": "2026-01-14T12:00:00Z"
}
```

**Error (404 Not Found)**:
```json
{
  "detail": "Task not found"
}
```

### 4. Update Task
**Endpoint**: `PUT /tasks/{id}`
**Description**: Update a task's details
**Authentication**: Required

#### Request
```
PUT /api/v1/tasks/550e8400-e29b-41d4-a716-446655440002
Headers:
  Authorization: Bearer <valid-jwt-token>
  Content-Type: application/json

Body:
{
  "description": "Updated task description",
  "is_completed": true
}
```

#### Request Validation
- At least one field must be provided for update
- `description` (if provided) must be 5-500 characters
- `description` (if provided) cannot be empty or whitespace-only

#### Response
**Success (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "description": "Updated task description",
  "is_completed": true,
  "created_at": "2026-01-14T12:00:00Z",
  "updated_at": "2026-01-14T13:00:00Z"
}
```

### 5. Delete Task
**Endpoint**: `DELETE /tasks/{id}`
**Description**: Delete a specific task
**Authentication**: Required

#### Request
```
DELETE /api/v1/tasks/550e8400-e29b-41d4-a716-446655440002
Headers:
  Authorization: Bearer <valid-jwt-token>
```

#### Response
**Success (200 OK)**:
```json
{
  "message": "Task deleted successfully"
}
```

### 6. Toggle Task Completion
**Endpoint**: `PATCH /tasks/{id}/complete`
**Description**: Toggle the completion status of a task
**Authentication**: Required

#### Request
```
PATCH /api/v1/tasks/550e8400-e29b-41d4-a716-446655440002/complete
Headers:
  Authorization: Bearer <valid-jwt-token>
  Content-Type: application/json

Body: {}
```

#### Response
**Success (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "description": "Updated task description",
  "is_completed": true,
  "created_at": "2026-01-14T12:00:00Z",
  "updated_at": "2026-01-14T13:30:00Z"
}
```

## Error Responses

### Common Error Format
```json
{
  "detail": "Descriptive error message"
}
```

### Authentication Errors
- **401 Unauthorized**: JWT token is missing, invalid, or expired
- **Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

### Resource Not Found
- **404 Not Found**: Task does not exist OR user lacks permission to access it
- **Response**:
```json
{
  "detail": "Task not found"
}
```

### Validation Errors
- **422 Unprocessable Entity**: Request validation failed
- **Response**:
```json
{
  "detail": [
    {
      "loc": ["body", "description"],
      "msg": "Field required",
      "type": "value_error.missing"
    }
  ]
}
```