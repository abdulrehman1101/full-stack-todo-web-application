# Quickstart Guide: In-Memory Python Console Todo App

**Feature**: 1-todo-app
**Created**: 2026-01-12

## Getting Started

### Prerequisites
- Python 3.13 or higher
- UV package manager

### Installation
1. Clone the repository
2. Navigate to the project directory
3. Install dependencies: `uv sync`
4. Activate virtual environment: `uv run python backend/src/main.py`

### Running the Application
```bash
# Activate the environment and run
uv run python backend/src/main.py
```

### Project Structure
```
todo-app/
├── backend/
│   ├── src/
│   │   ├── main.py              # Application entry point
│   │   ├── todo_logic.py        # Core business logic
│   │   ├── cli_interface.py     # Command-line interface
│   │   └── models/
│   │       └── task.py          # Task data model
│   ├── tests/
│   │   ├── test_todo_logic.py   # Logic unit tests
│   │   ├── test_cli_interface.py # CLI integration tests
│   │   └── test_models.py       # Model unit tests
│   └── pyproject.toml           # Project dependencies
├── .specify/                  # Specification files
├── specs/                     # Feature specifications
├── history/                   # Prompt history records
└── README.md                  # Project documentation
```

## Development Commands

### Setting up the environment
```bash
# Install dependencies
uv sync

# Run the application
uv run python backend/src/main.py

# Run tests
uv run pytest backend/tests

# Check test coverage
uv run pytest --cov=backend/src
```

## Core Components

### Task Model (`backend/src/models/task.py`)
- Defines the Task entity with id, description, and completion status
- Implements validation rules for task properties

### Todo Logic (`backend/src/todo_logic.py`)
- Contains all business logic for task management
- Implements CRUD operations for tasks
- Manages in-memory storage

### CLI Interface (`backend/src/cli_interface.py`)
- Handles user input and menu navigation
- Formats task display for console output
- Provides user feedback and error messages

### Main Application (`backend/src/main.py`)
- Entry point for the application
- Orchestrates interaction between components
- Runs the main application loop