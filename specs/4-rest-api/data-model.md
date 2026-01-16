# Data Model: RESTful API Development (CRUD Logic)

## Overview
This document describes the data structures and relationships for the task management API, focusing on how authenticated users interact with their task data through the RESTful endpoints. The model builds upon the existing User and Task entities from previous specifications with enhanced validation and API-specific schemas.

## Core Entities

### Task
**Source**: Extends existing Task model from Spec 1 (Neon DB)

**Attributes**:
- `id`: UUID (Primary Key) - Uniquely identifies the task across the system
- `user_id`: UUID (Foreign Key) - Links task to owning user (enforces data isolation)
- `description`: Text - Detailed description of the task (5-500 characters)
- `is_completed`: Boolean - Status indicating task completion (default: False)
- `created_at`: DateTime - Timestamp of task creation
- `updated_at`: DateTime - Timestamp of last task update

**Relationships**:
- Belongs to User entity via `user_id` foreign key
- One User can have many Tasks (one-to-many relationship)

**Validation Rules**:
- Description must be 5-500 characters
- Description cannot be empty or whitespace-only
- Task must be associated with a valid User ID
- User can only modify their own tasks

### TaskCreate (Request Schema)
**Type**: API Request Schema for creating new tasks

**Attributes**:
- `description`: String (Required) - Task description (5-500 characters)

**Validation Requirements**:
- Description field is required
- Description length between 5-500 characters
- Description cannot be empty or whitespace-only
- Server assigns `user_id` from authenticated user's JWT token

### TaskUpdate (Request Schema)
**Type**: API Request Schema for updating existing tasks

**Attributes**:
- `description`: String (Optional) - Updated task description (5-500 characters)
- `is_completed`: Boolean (Optional) - Updated completion status

**Validation Requirements**:
- At least one field must be provided for update
- Description length between 5-500 characters if provided
- User can only update tasks they own
- Server validates user ownership before allowing update

### TaskResponse (Response Schema)
**Type**: API Response Schema for returning task data

**Attributes**:
- `id`: UUID - Task identifier
- `user_id`: UUID - Owner's user identifier (for reference)
- `description`: String - Task description
- `is_completed`: Boolean - Completion status
- `created_at`: DateTime - Creation timestamp
- `updated_at`: DateTime - Last update timestamp

**Validation Requirements**:
- All fields are read-only from client perspective
- Data is filtered to only show user's own tasks
- Timestamps are automatically managed by the system

## API Data Transitions

### Create Task Flow
```
Input: { description: "New task description" } (via POST /api/tasks)
Processing: Validate description, assign user_id from JWT, create Task record
Output: TaskResponse { id: "uuid-123", user_id: "user-uuid", description: "New task description", is_completed: false, created_at: "timestamp", updated_at: "timestamp" }
```

### Read Task Flow
```
Input: GET /api/tasks/{task_id} (with Authorization header)
Processing: Validate JWT, verify task belongs to user, retrieve Task record
Output: TaskResponse { ...task data... } or 404 if not found/not owned by user
```

### Update Task Flow
```
Input: { description: "Updated description", is_completed: true } (via PUT /api/tasks/{task_id})
Processing: Validate JWT, verify task belongs to user, update Task record
Output: TaskResponse { ...updated task data... } or 404 if not found/not owned by user
```

### Delete Task Flow
```
Input: DELETE /api/tasks/{task_id} (with Authorization header)
Processing: Validate JWT, verify task belongs to user, delete Task record
Output: { message: "Task deleted successfully" } or 404 if not found/not owned by user
```

### Toggle Completion Flow
```
Input: PATCH /api/tasks/{task_id}/complete (with Authorization header)
Processing: Validate JWT, verify task belongs to user, toggle is_completed field
Output: TaskResponse { ...task data with toggled completion status... } or 404 if not found/not owned by user
```

## Security & Access Control

### User Data Isolation
- All database queries include `WHERE user_id = authenticated_user_id` filter
- Users cannot access, modify, or delete tasks belonging to other users
- 404 responses are returned for unauthorized access attempts (not 403) to prevent data enumeration

### Validation Layers
- **API Layer**: Pydantic schema validation for request/response formats
- **Business Logic**: User ownership verification before database operations
- **Database Layer**: SQLModel constraints and foreign key relationships