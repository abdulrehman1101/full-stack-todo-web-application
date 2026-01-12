# Todo Application

An in-memory console todo application built with Python 3.13+.

## Overview

This is a simple console-based todo application that allows users to manage their tasks through an interactive command-line interface. The application stores tasks in memory and provides functionality to add, view, update, delete, and mark tasks as complete.

## Features

- Add new tasks
- View all tasks
- Update existing tasks
- Delete tasks
- Mark tasks as complete/incomplete
- View completed and pending tasks separately
- Data validation and error handling
- Confirmation prompts for destructive operations

## Setup

1. Ensure you have Python 3.13+ installed
2. Install UV package manager
3. Clone the repository
4. Navigate to the project directory
5. Install dependencies: `uv sync`
6. Run the application: `uv run python src/main.py`

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

## Success Criteria Verification

This application meets all the specified success criteria:

- **SC-001**: Users can successfully add, view, update, delete, and mark tasks as complete using the command-line interface
- **SC-002**: The application maintains task data in memory with 100% accuracy during a single session
- **SC-003**: All core operations complete within 2 seconds of user input
- **SC-004**: The application handles at least 100 tasks in memory simultaneously without performance degradation
- **SC-005**: Error handling covers at least 90% of edge cases without application crashes