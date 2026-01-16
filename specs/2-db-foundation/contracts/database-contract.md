# API Contract: Database Foundation & Schema

## Database Connection Endpoint
```
GET /health/database
```
**Purpose**: Verify database connectivity and health status
**Response**: 200 OK with database status information
**Authentication**: None required

## User Model Operations
```
POST /users
```
**Purpose**: Create a new user in the database
**Request Body**:
```json
{
  "email": "string (required, valid email format)"
}
```
**Response**: 201 Created with user object containing id, email, and created_at

## Task Model Operations
```
POST /tasks
```
**Purpose**: Create a new task associated with a user
**Request Body**:
```json
{
  "user_id": "UUID (required, must reference existing user)",
  "description": "string (required, non-empty)",
  "is_completed": "boolean (optional, defaults to false)"
}
```
**Response**: 201 Created with task object containing all fields

```
GET /users/{user_id}/tasks
```
**Purpose**: Retrieve all tasks for a specific user
**Response**: 200 OK with array of task objects

## Validation Requirements
- All UUID fields must be valid UUID format
- Email fields must pass email validation
- Foreign key constraints must be validated
- Required fields must be present in requests