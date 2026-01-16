# Data Model: Database Foundation & Schema

## Entity: User

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the user
- `email`: String (Unique, Required) - User's email address for identification
- `created_at`: DateTime - Timestamp when the user record was created

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- ID must be a valid UUID format
- Created_at defaults to current timestamp on creation

**Relationships**:
- One-to-Many: User has many Tasks (via user_id foreign key)

## Entity: Task

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the task
- `user_id`: UUID (Foreign Key) - Reference to the User who owns this task
- `description`: String (Required) - Description of the task
- `is_completed`: Boolean - Status of task completion (default: False)
- `created_at`: DateTime - Timestamp when the task was created

**Validation Rules**:
- User_id must reference an existing User
- Description must not be empty
- ID must be a valid UUID format
- Created_at defaults to current timestamp on creation
- is_completed defaults to False

**State Transitions**:
- Task starts with `is_completed = False`
- Task can transition to `is_completed = True` when marked as done
- Task can transition back to `is_completed = False` if unmarked

**Relationships**:
- Many-to-One: Task belongs to one User (via user_id foreign key)

## Database Schema Constraints

**Primary Keys**: Both User and Task entities use UUID primary keys for better scalability and privacy.

**Foreign Key Constraints**: Task.user_id references User.id with proper referential integrity.

**Unique Constraints**: User.email must be unique to prevent duplicate accounts.

**Indexing Strategy**:
- Primary key indexes on all id fields
- Index on user_id in Task table for efficient user-based queries
- Potential composite indexes for common query patterns