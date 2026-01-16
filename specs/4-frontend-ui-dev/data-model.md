# Frontend Data Models: Todo Application

**Feature**: Frontend UI Development
**Created**: 2026-01-14

## Entity Definitions

### User
**Description**: Represents the authenticated user in the frontend application

**Fields**:
- `id` (string | UUID): Unique identifier for the user
- `email` (string): User's email address
- `name` (string | null): User's display name (optional)
- `createdAt` (Date): Account creation timestamp
- `updatedAt` (Date): Last update timestamp

**Validation**:
- `email` must be a valid email format
- `name` must be between 1-100 characters if provided

**State Transitions**:
- Unauthenticated → Authenticated (login/register)
- Authenticated → Unauthenticated (logout)

### Task
**Description**: Represents a todo item in the frontend application

**Fields**:
- `id` (string | UUID): Unique identifier for the task
- `title` (string): Task title (1-200 characters)
- `description` (string): Task description (optional)
- `isCompleted` (boolean): Completion status
- `userId` (string | UUID): Owner of the task
- `createdAt` (Date): Creation timestamp
- `updatedAt` (Date): Last update timestamp

**Validation**:
- `title` must be between 1-200 characters
- `description` must be between 0-500 characters if provided
- `userId` must match the authenticated user's ID

**State Transitions**:
- Created → In Progress → Completed
- Completed → In Progress (toggle)

### AuthenticationState
**Description**: Represents the authentication state in the frontend application

**Fields**:
- `user` (User | null): Currently authenticated user
- `isLoading` (boolean): Whether authentication state is being resolved
- `isLoggedIn` (boolean): Whether a user is currently logged in
- `token` (string | null): JWT token for API authentication

**State Transitions**:
- {user: null, isLoading: true, isLoggedIn: false} → Login attempt
- {user: User, isLoading: false, isLoggedIn: true} → Successful login
- {user: null, isLoading: false, isLoggedIn: false} → Logout

### ThemeState
**Description**: Represents the current theme configuration

**Fields**:
- `mode` ('midnight' | 'deep-dark'): Current theme mode
- `isDark` (boolean): Whether dark mode is active
- `colors` (object): Current color palette configuration

**State Transitions**:
- 'midnight' → 'deep-dark' (theme toggle)
- 'deep-dark' → 'midnight' (theme toggle)

### TaskFilter
**Description**: Represents filters applied to the task list

**Fields**:
- `status` ('all' | 'active' | 'completed'): Task completion status filter
- `searchQuery` (string): Text search filter
- `sortBy` ('createdAt' | 'updatedAt' | 'title'): Sort criteria
- `sortOrder` ('asc' | 'desc'): Sort order

## Relationships

### User → Task
- **Relationship**: One-to-Many (one user can have many tasks)
- **Cardinality**: 1:N
- **Constraint**: A task must belong to exactly one user
- **Implementation**: Task entity contains `userId` field that references User's `id`

## State Management Models

### AppState
**Description**: Top-level application state structure

**Fields**:
- `auth` (AuthenticationState): Authentication state
- `tasks` (Task[]): List of tasks for the current user
- `ui` (object): UI-specific state (loading indicators, modals, etc.)
- `theme` (ThemeState): Current theme configuration

### FormState
**Description**: State structure for form components

**Fields** (for LoginForm):
- `email` (string): Email input value
- `password` (string): Password input value
- `errors` (object): Validation errors
- `isLoading` (boolean): Submission state

**Fields** (for TaskForm):
- `title` (string): Task title input
- `description` (string): Task description input
- `errors` (object): Validation errors
- `isLoading` (boolean): Submission state

## API Response Models

### AuthResponse
**Description**: Expected structure of authentication API responses

**Fields**:
- `accessToken` (string): JWT access token
- `tokenType` (string): Token type (usually "bearer")
- `user` (User): User object

### TaskResponse
**Description**: Expected structure of task API responses

**Fields** (for single task):
- `id` (string): Task ID
- `title` (string): Task title
- `description` (string): Task description
- `isCompleted` (boolean): Completion status
- `userId` (string): User ID
- `createdAt` (string): Creation timestamp (ISO format)
- `updatedAt` (string): Update timestamp (ISO format)

**Fields** (for task list):
- `data` (TaskResponse[]): Array of task objects
- `total` (number): Total number of tasks
- `page` (number): Current page
- `limit` (number): Items per page

## Validation Rules

### User Validation
- Email format: Must match RFC 5322 standard
- Name: Alphanumeric characters, spaces, hyphens, and apostrophes only
- Length limits as specified above

### Task Validation
- Title: Required, 1-200 characters
- Description: Optional, 0-500 characters
- isCompleted: Boolean value only
- userId: Must match authenticated user ID

### Authentication Validation
- Email: Required, valid format
- Password: At least 8 characters with complexity requirements (handled by backend)

## Frontend-Specific Types

### ComponentProps
**Description**: Type definitions for component properties

**TaskCardProps**:
- `task` (Task): Task object to display
- `onToggleComplete` (function): Callback for completion toggle
- `onEdit` (function): Callback for edit action
- `onDelete` (function): Callback for delete action

**LoginFormProps**:
- `onLogin` (function): Callback for successful login
- `onNavigateToRegister` (function): Callback to switch to registration

**TaskFormProps**:
- `onSubmit` (function): Callback for form submission
- `initialValues` (Task | null): Initial form values for editing

## State Transition Diagrams

### Authentication Flow
```
Unauthenticated State
        ↓ (login attempt)
Loading State
        ↓ (success)
Authenticated State
        ↓ (logout)
Unauthenticated State
```

### Task Lifecycle
```
Initial State (empty)
        ↓ (create)
Task Created State
        ↓ (toggle complete)
Task Completed State
        ↓ (toggle incomplete)
Task Active State
        ↓ (delete)
Back to Initial State
```

## Error Models

### APIError
**Description**: Structure for API error responses

**Fields**:
- `message` (string): Error message
- `code` (string): Error code
- `details` (any): Additional error details

### ValidationError
**Description**: Structure for validation errors

**Fields**:
- `field` (string): Field name with error
- `message` (string): Validation error message
- `code` (string): Validation error code