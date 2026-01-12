"""
CLI Interface for Todo Application

This module provides the command-line interface for interacting with the todo application.
"""
import os
import sys
from typing import Optional

# Handle imports for both direct execution and module execution
try:
    from .todo_logic import TodoLogic
    from .models.task import Task
except ImportError:
    # When run as a script, need to handle imports differently
    import importlib.util
    # Add the current directory to path to allow imports
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    # Import using absolute paths
    todo_logic_spec = importlib.util.spec_from_file_location("todo_logic", os.path.join(os.path.dirname(__file__), "todo_logic.py"))
    todo_logic_module = importlib.util.module_from_spec(todo_logic_spec)
    todo_logic_spec.loader.exec_module(todo_logic_module)
    TodoLogic = todo_logic_module.TodoLogic

    # Import task model
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    task_spec = importlib.util.spec_from_file_location("task", os.path.join(models_dir, "task.py"))
    task_module = importlib.util.module_from_spec(task_spec)
    task_spec.loader.exec_module(task_module)
    Task = task_module.Task


class CLIInterface:
    """
    Command-line interface for the todo application.

    Provides methods to interact with the todo logic through a console interface.
    """

    def __init__(self):
        """Initialize the CLI interface with the todo logic."""
        self.todo_logic = TodoLogic()

    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self, title: str = "Todo Application"):
        """Display a formatted header."""
        print("=" * 50)
        print(f"{title:^50}")
        print("=" * 50)
        print()

    def display_menu(self):
        """Display the main menu options."""
        print("Main Menu:")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Mark Task as Complete")
        print("4. Mark Task as Incomplete")
        print("5. Update Task")
        print("6. Delete Task")
        print("7. View Completed Tasks")
        print("8. View Pending Tasks")
        print("9. Exit")
        print()

    def get_user_choice(self) -> str:
        """Get and validate user menu choice."""
        while True:
            try:
                choice = input("Enter your choice (1-9): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 9.")
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                exit()
            except EOFError:
                print("\n\nGoodbye!")
                exit()

    def add_task(self):
        """Handle adding a new task."""
        print("\n--- Add New Task ---")
        try:
            description = input("Enter task description: ").strip()
            if not description:
                print("Task description cannot be empty.")
                return

            task = self.todo_logic.add_task(description)
            print(f"Task added successfully! ID: {task.id}, Description: {task.description}")
        except Exception as e:
            print(f"Error adding task: {e}")

    def view_all_tasks(self):
        """Handle viewing all tasks."""
        print("\n--- All Tasks ---")
        tasks = self.todo_logic.list_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            status = "✓" if task.completed else "○"
            print(f"{status} [{task.id}] {task.description} (Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')})")

    def mark_task_complete(self):
        """Handle marking a task as complete."""
        print("\n--- Mark Task as Complete ---")
        try:
            task_id = int(input("Enter task ID to mark as complete: "))
            task = self.todo_logic.mark_complete(task_id)

            if task:
                print(f"Task {task.id} marked as complete: {task.description}")
            else:
                print(f"Task with ID {task_id} not found.")
        except ValueError:
            print("Invalid task ID. Please enter a number.")
        except Exception as e:
            print(f"Error marking task as complete: {e}")

    def mark_task_incomplete(self):
        """Handle marking a task as incomplete."""
        print("\n--- Mark Task as Incomplete ---")
        try:
            task_id = int(input("Enter task ID to mark as incomplete: "))
            task = self.todo_logic.mark_incomplete(task_id)

            if task:
                print(f"Task {task.id} marked as incomplete: {task.description}")
            else:
                print(f"Task with ID {task_id} not found.")
        except ValueError:
            print("Invalid task ID. Please enter a number.")
        except Exception as e:
            print(f"Error marking task as incomplete: {e}")

    def update_task(self):
        """Handle updating a task."""
        print("\n--- Update Task ---")
        try:
            task_id = int(input("Enter task ID to update: "))

            # Check if task exists
            task = self.todo_logic.get_task(task_id)
            if not task:
                print(f"Task with ID {task_id} not found.")
                return

            print(f"Current task: {task.description}")
            new_description = input("Enter new description (or press Enter to keep current): ").strip()

            # Only update description if provided
            if new_description:
                updated_task = self.todo_logic.update_task(task_id, description=new_description)
                if updated_task:
                    print(f"Task {updated_task.id} updated successfully: {updated_task.description}")
                else:
                    print(f"Failed to update task with ID {task_id}.")
            else:
                print("No changes made to description.")

        except ValueError:
            print("Invalid task ID. Please enter a number.")
        except Exception as e:
            print(f"Error updating task: {e}")

    def delete_task(self):
        """Handle deleting a task."""
        print("\n--- Delete Task ---")
        try:
            task_id = int(input("Enter task ID to delete: "))

            # Confirm deletion
            task = self.todo_logic.get_task(task_id)
            if not task:
                print(f"Task with ID {task_id} not found.")
                return

            confirm = input(f"Are you sure you want to delete task '{task.description}'? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                success = self.todo_logic.delete_task(task_id)
                if success:
                    print(f"Task {task_id} deleted successfully.")
                else:
                    print(f"Failed to delete task with ID {task_id}.")
            else:
                print("Deletion cancelled.")
        except ValueError:
            print("Invalid task ID. Please enter a number.")
        except Exception as e:
            print(f"Error deleting task: {e}")

    def view_completed_tasks(self):
        """Handle viewing completed tasks."""
        print("\n--- Completed Tasks ---")
        tasks = self.todo_logic.get_completed_tasks()

        if not tasks:
            print("No completed tasks found.")
            return

        for task in tasks:
            print(f"✓ [{task.id}] {task.description} (Completed)")

    def view_pending_tasks(self):
        """Handle viewing pending tasks."""
        print("\n--- Pending Tasks ---")
        tasks = self.todo_logic.get_pending_tasks()

        if not tasks:
            print("No pending tasks found.")
            return

        for task in tasks:
            print(f"○ [{task.id}] {task.description} (Pending)")

    def run(self):
        """Run the main application loop."""
        self.clear_screen()
        self.display_header()

        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_all_tasks()
            elif choice == '3':
                self.mark_task_complete()
            elif choice == '4':
                self.mark_task_incomplete()
            elif choice == '5':
                self.update_task()
            elif choice == '6':
                self.delete_task()
            elif choice == '7':
                self.view_completed_tasks()
            elif choice == '8':
                self.view_pending_tasks()
            elif choice == '9':
                print("\nThank you for using the Todo Application. Goodbye!")
                break

            # Pause before showing menu again
            input("\nPress Enter to continue...")
            self.clear_screen()
            self.display_header()