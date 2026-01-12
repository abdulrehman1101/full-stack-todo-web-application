# Data Model: In-Memory Python Console Todo App

**Feature**: 1-todo-app
**Created**: 2026-01-12
**Status**: Final

## Entity Definitions

### Task
Represents a single todo item in the application

**Attributes**:
- `id`: integer (unique identifier, auto-incremented)
- `description`: string (task description, required)
- `completed`: boolean (completion status, default: False)
- `created_at`: datetime (timestamp of creation, auto-set)

**Validation Rules**:
- Description must be non-empty (1+ characters)
- Description must be less than 500 characters
- ID must be unique within the TaskList
- ID must be positive integer

### TaskList
Collection of Task entities managed in memory during application runtime

**Attributes**:
- `tasks`: dictionary mapping task IDs to Task objects
- `next_id`: integer (next available ID for auto-generation)

**Methods**:
- `add_task(description: str) -> Task`: Creates new task and adds to collection
- `get_task(task_id: int) -> Optional[Task]`: Retrieves task by ID
- `update_task(task_id: int, description: str = None, completed: bool = None) -> Optional[Task]`: Updates task properties
- `delete_task(task_id: int) -> bool`: Removes task from collection
- `list_all_tasks() -> List[Task]`: Returns all tasks sorted by ID
- `mark_complete(task_id: int) -> Optional[Task]`: Marks task as completed
- `get_completed_tasks() -> List[Task]`: Returns only completed tasks
- `get_pending_tasks() -> List[Task]`: Returns only pending tasks

**Validation Rules**:
- Cannot add task with empty description
- Cannot update/get/delete non-existent task
- Cannot add duplicate IDs (handled by auto-generation)

## State Transitions

### Task State Transitions
- Pending (completed=False) → Completed (completed=True) when marked complete
- Completed (completed=True) → Pending (completed=False) when marked incomplete

## Relationships
- TaskList contains 0 to N Task objects
- Each Task belongs to exactly one TaskList
- Task IDs are unique within the TaskList scope

## Data Access Patterns
- Primary access by ID (O(1) lookup in dictionary)
- Secondary access by completion status (filter operations)
- Sequential access when listing all tasks