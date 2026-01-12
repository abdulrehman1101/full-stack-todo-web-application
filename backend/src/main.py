"""
Main Entry Point for Todo Application

This is the main script that initializes the application and starts the CLI loop.
"""
import sys
import os

# Add the src directory to the Python path to allow imports when running from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from cli_interface import CLIInterface


def main():
    """Main function to start the todo application."""
    print("Starting Todo Application...")
    cli = CLIInterface()
    cli.run()


if __name__ == "__main__":
    main()