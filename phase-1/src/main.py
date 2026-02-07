"""
Todo In-Memory Console Application - Main Entry Point

A Python 3.13+ command-line todo management application with full CRUD operations
stored entirely in runtime memory. No persistence - all data is lost on exit.

Usage:
    python src/main.py

Features:
    - Create todos with title and description
    - View all todos in formatted list
    - Mark todos as complete
    - Update todo details
    - Delete todos
    - In-memory only (no persistence)

Constitution Compliance:
    ✅ Spec-Driven Development
    ✅ In-Memory Only Storage
    ✅ Python 3.13+
    ✅ CLI-First Interface
    ✅ Modular Architecture
    ✅ Clean Code Standards
"""

import sys
from src.repository.todo_repository import TodoRepository
from src.cli.menu import TodoMenu


def main() -> int:
    """
    Application entry point.

    Initializes the repository and menu system, displays welcome message,
    and starts the interactive menu loop. Handles graceful shutdown on
    keyboard interrupt and unexpected errors.

    Returns:
        Exit code (0 for success, 1 for error)

    Examples:
        >>> main()  # Starts the application
        Welcome to Todo Manager!
        All data is stored in memory and will be lost on exit.
        ...
    """
    # Display welcome message
    print("Welcome to Todo Manager!")
    print("All data is stored in memory and will be lost on exit.\n")

    try:
        # Initialize repository and menu
        repository = TodoRepository()
        menu = TodoMenu(repository)

        # Start menu loop
        menu.run()

        # Display goodbye message
        print("\nGoodbye!")
        return 0

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nGoodbye!")
        return 0

    except Exception as e:
        # Handle unexpected errors
        print(f"\n[X] Unexpected error: {e}")
        print("Application will now exit.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
