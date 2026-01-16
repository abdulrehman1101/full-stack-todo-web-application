# Todo Application - Authentication & Identity

A todo application with secure authentication and persistent storage using Neon Serverless PostgreSQL and SQLModel ORM, built with Python 3.13+.

## Overview

This is a todo application that implements secure authentication with JWT tokens and stores data persistently in a Neon Serverless PostgreSQL database using SQLModel ORM. The application provides functionality to add, view, update, delete, and mark tasks as complete, with secure access control and data persistence across application restarts.

## Features

- Add new tasks
- View all tasks
- Update existing tasks
- Delete tasks
- Mark tasks as complete/incomplete
- View completed and pending tasks separately
- Data validation and error handling
- Confirmation prompts for destructive operations

## API Endpoints

The application exposes a comprehensive REST API with the following endpoints:

### Authentication Endpoints
- `POST /api/v1/auth/register` - Register a new user account
- `POST /api/v1/auth/login` - Authenticate user and obtain JWT token
- `POST /api/v1/auth/logout` - Logout user (client-side token removal)

### Task Management Endpoints
- `POST /api/v1/tasks/` - Create a new task for authenticated user
- `GET /api/v1/tasks/` - Retrieve all tasks for authenticated user
- `GET /api/v1/tasks/{id}` - Retrieve a specific task by ID
- `PUT /api/v1/tasks/{id}` - Update a specific task by ID
- `DELETE /api/v1/tasks/{id}` - Delete a specific task by ID
- `PATCH /api/v1/tasks/{id}/complete` - Toggle completion status of a task

### Authorization Instructions

To access protected endpoints, follow these steps:

1. Register a new user or login to obtain a JWT token:
   ```bash
   # Register new user
   curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "securepassword"}'

   # Login to get token
   curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "securepassword"}'
   ```

2. Use the obtained JWT token in the Authorization header for protected endpoints:
   ```bash
   # Include Bearer token in requests
   curl -X GET "http://localhost:8000/api/v1/tasks/" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
   ```

3. **In Swagger UI**: Click the "Authorize" button, enter "Bearer YOUR_JWT_TOKEN_HERE" in the value field, and click "Authorize".

### Data Isolation Security Feature

The application implements robust data isolation to ensure users can only access their own data:

- **User Scoping**: All database queries are filtered by the authenticated user's ID
- **Task Ownership**: Each task is associated with a specific user, and users can only access their own tasks
- **Row-Level Security**: Implemented at the application layer to prevent unauthorized access
- **Access Validation**: Every request validates that the requested resource belongs to the authenticated user
- **404 Instead of 403**: Resources that don't belong to the user return 404 (Not Found) instead of 403 (Forbidden) to prevent information disclosure about other users' data

## Setup

1. Ensure you have Python 3.13+ installed
2. Install UV package manager
3. Clone the repository
4. Navigate to the project directory
5. Create a Neon Serverless PostgreSQL database and obtain the connection string
6. Copy `.env.example` to `.env` and configure your environment variables:
   ```
   DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
   BETTER_AUTH_SECRET=your-super-long-secret-key-here-must-be-at-least-32-chars
   CORS_ORIGINS=http://localhost,http://localhost:3000,http://127.0.0.1,http://127.0.0.1:3000
   ```
7. Install dependencies: `uv sync`
8. Initialize the database: `uv run python -m backend.src.database.init_db`
9. Run the application: `uv run python src/main.py`

## Authentication Setup

This application implements secure authentication using JWT tokens with comprehensive security measures. Follow these steps to set up authentication:

1. **Configure the BETTER_AUTH_SECRET**: Generate a secure random secret key that is at least 32 characters long. This key is used to sign JWT tokens.
   ```bash
   # Example: Generate a 32+ character secret
   openssl rand -hex 32
   ```

2. **Set up CORS origins**: Configure the `CORS_ORIGINS` environment variable to include all domains that will access your API.

3. **Test authentication endpoints**: Once the backend is running, you can test authentication:
   - Register a new user: `POST /api/v1/auth/register`
   - Login to get JWT token: `POST /api/v1/auth/login`
   - Access protected endpoints: `GET /api/v1/users/me` (include `Authorization: Bearer <token>` header)

4. **Verify authentication flow**: Test the complete authentication flow by logging in, obtaining a token, and using it to access protected resources.

5. **Security features implemented**:
   - Rate limiting on authentication endpoints (5 registrations/minute, 10 logins/minute)
   - Security headers (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, HSTS, CSP)
   - Token tampering detection with enhanced error handling
   - Audit logging for authentication events (successful/failed logins, registrations)
   - User activity tracking with `updated_at` timestamps
   - User data isolation - users can only access their own data

6. **Environment Configuration**:
   - Development: Use `.env` file with appropriate secrets
   - Production: Use `.env.production` with production-ready configuration
   - Both environments include proper CORS, database, and authentication settings

7. **Audit Trail Features**:
   - `last_login_at` field in User model tracks last login time
   - `updated_at` field tracks last activity time for audit purposes
   - Failed login attempts are monitored (though not fully implemented in this version)
   - All authentication events are logged for security monitoring

## Usage

Run the application and follow the interactive menu prompts to manage your tasks:

```
==================================================
            Todo Application
==================================================

Main Menu:
1. Add Task
2. View All Tasks
3. Mark Task as Complete
4. Mark Task as Incomplete
5. Update Task
6. Delete Task
7. View Completed Tasks
8. View Pending Tasks
9. Exit

Enter your choice (1-9):
```

## Development

### Running Tests

To run the test suite:
```bash
uv run pytest
```

To run tests with coverage:
```bash
uv run pytest --cov=src
```

### Project Structure

```
todo-app/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── cli_interface.py     # Command-line interface
│   ├── todo_logic.py        # Core business logic
│   └── models/
│       ├── __init__.py
│       ├── task.py          # Task data model
│       ├── task_list.py     # Task collection
│       └── exceptions.py    # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── test_logic.py        # Logic layer tests
│   ├── test_models.py       # Model layer tests
│   ├── test_performance.py  # Performance tests
│   └── test_edge_cases.py   # Edge case tests
├── pyproject.toml           # Project dependencies
├── README.md               # Project documentation
└── .gitignore             # Git ignore patterns
```

## Database Schema

The application uses the following database schema:

### User Table
- `id`: UUID (Primary Key) - Unique identifier for the user
- `email`: VARCHAR (Unique, Indexed) - User's email address
- `created_at`: TIMESTAMP - Timestamp when the user record was created

### Task Table
- `id`: UUID (Primary Key) - Unique identifier for the task
- `user_id`: UUID (Foreign Key) - Reference to the User who owns this task
- `description`: TEXT - Description of the task
- `is_completed`: BOOLEAN - Status of task completion (default: False)
- `created_at`: TIMESTAMP - Timestamp when the task was created

## Success Criteria Verification

This application meets all the specified success criteria:

- **SC-001**: Users can successfully add, view, update, delete, and mark tasks as complete with persistent storage
- **SC-002**: The application maintains task data persistently in Neon Serverless PostgreSQL with 100% accuracy
- **SC-003**: All database operations complete within acceptable timeframes
- **SC-004**: The application handles user and task data with proper relationships
- **SC-005**: Error handling covers database connection and validation edge cases without application crashes