# Quickstart Guide: RESTful API Development (CRUD Logic)

## Overview
This guide provides a rapid introduction to the task management API implementation, including setup instructions and basic usage patterns for developers.

## Prerequisites
- Python 3.13+ installed
- UV package manager
- Access to Neon Serverless PostgreSQL database
- Completed authentication system from Spec 3 (JWT-based)

## Setup Instructions

### 1. Environment Configuration
```bash
# Copy environment template
cp backend/.env.example backend/.env

# Configure your environment variables
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
BETTER_AUTH_SECRET=your-super-long-secret-key-here-must-be-at-least-32-chars
CORS_ORIGINS=http://localhost,http://localhost:3000,http://127.0.0.1,http://127.0.0.1:3000
```

### 2. Install Dependencies
```bash
cd backend
uv sync
```

### 3. Initialize Database
```bash
uv run python -m backend.src.database.init_db
```

## API Endpoint Structure

The task management API follows RESTful conventions with the following endpoints:

### Base URL: `/api/v1`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | List all tasks for authenticated user |
| POST | `/tasks` | Create a new task for authenticated user |
| GET | `/tasks/{id}` | Get specific task details |
| PUT | `/tasks/{id}` | Update task details |
| DELETE | `/tasks/{id}` | Delete a task |
| PATCH | `/tasks/{id}/complete` | Toggle task completion status |

## Authentication Requirements

All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

## Quick API Usage Examples

### 1. List All Tasks
```bash
curl -X GET \
  http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer your-jwt-token-here"
```

### 2. Create a New Task
```bash
curl -X POST \
  http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer your-jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{"description": "Complete the API implementation"}'
```

### 3. Get Specific Task
```bash
curl -X GET \
  http://localhost:8000/api/v1/tasks/task-id-here \
  -H "Authorization: Bearer your-jwt-token-here"
```

### 4. Update a Task
```bash
curl -X PUT \
  http://localhost:8000/api/v1/tasks/task-id-here \
  -H "Authorization: Bearer your-jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated task description", "is_completed": true}'
```

### 5. Toggle Task Completion
```bash
curl -X PATCH \
  http://localhost:8000/api/v1/tasks/task-id-here/complete \
  -H "Authorization: Bearer your-jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 6. Delete a Task
```bash
curl -X DELETE \
  http://localhost:8000/api/v1/tasks/task-id-here \
  -H "Authorization: Bearer your-jwt-token-here"
```

## Key Implementation Concepts

### 1. Data Isolation
Each database query filters by the authenticated user's ID to ensure complete data isolation:
```python
# Example implementation pattern
tasks = session.exec(
    select(Task).where(Task.user_id == current_user_id)
).all()
```

### 2. Error Handling
The API follows security best practices by returning 404 for unauthorized access:
- Return 404 Not Found for tasks that don't exist OR don't belong to the user
- Never reveal whether resources exist to unauthorized users

### 3. Response Validation
All responses use Pydantic models for automatic serialization and validation:
```python
# Example response model
class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    description: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime
```

## Testing the API

### Run Unit Tests
```bash
uv run pytest backend/tests/unit/
```

### Run Integration Tests
```bash
uv run pytest backend/tests/integration/
```

### Test Data Isolation
Verify that users cannot access each other's data:
```bash
# This should return 404, not 403
curl -X GET http://localhost:8000/api/v1/tasks/other-users-task-id \
  -H "Authorization: Bearer different-users-jwt-token"
```

## Performance Considerations

- API responses should return within 500ms for 95% of requests
- Database queries should use indexes on user_id for efficient filtering
- Connection pooling should be configured appropriately for expected load

## Troubleshooting

### Common Issues
1. **401 Unauthorized**: Verify JWT token is valid and properly formatted
2. **404 Not Found**: Check that task exists and belongs to authenticated user
3. **422 Validation Error**: Verify request body matches expected schema
4. **Database Connection**: Ensure DATABASE_URL is properly configured

### Debugging Tips
- Enable logging to trace request flow
- Verify JWT token contents using a JWT decoder
- Check database connectivity with a simple health check endpoint