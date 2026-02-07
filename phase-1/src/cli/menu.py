"""
Main menu system for Todo CLI application.

This module provides the TodoMenu class which manages the main menu loop
and command dispatch for user interaction.
"""

from src.repository.todo_repository import TodoRepository
from src.cli.commands import (
    handle_create,
    handle_list,
    handle_update,
    handle_delete,
    handle_complete
)


class TodoMenu:
    """
    Main menu interface for Todo application.

    Manages the command loop, displays menu options, validates user input,
    and dispatches commands to appropriate handlers.

    Attributes:
        repository: TodoRepository instance for data management

    Examples:
        >>> repo = TodoRepository()
        >>> menu = TodoMenu(repo)
        >>> menu.run()  # Starts interactive menu loop
    """

    def __init__(self, repository: TodoRepository):
        """
        Initialize menu with repository.

        Args:
            repository: TodoRepository instance
        """
        self.repository = repository
        self.running = True

    def display_menu(self) -> None:
        """
        Display the main menu options.

        Shows numbered menu with all available commands.
        """
        print("\n=== Todo Manager ===")
        print("1. Create a new todo")
        print("2. View all todos")
        print("3. Update a todo")
        print("4. Delete a todo")
        print("5. Mark todo as complete")
        print("6. Exit")
        print()

    def get_choice(self) -> str:
        """
        Prompt user for menu choice.

        Returns:
            User's menu choice as string
        """
        return input("Enter your choice (1-6): ").strip()

    def dispatch_command(self, choice: str) -> None:
        """
        Dispatch user choice to appropriate command handler.

        Args:
            choice: User's menu choice (1-6)
        """
        if choice == '1':
            handle_create(self.repository)
        elif choice == '2':
            handle_list(self.repository)
        elif choice == '3':
            handle_update(self.repository)
        elif choice == '4':
            handle_delete(self.repository)
        elif choice == '5':
            handle_complete(self.repository)
        elif choice == '6':
            self.running = False
        else:
            print("[X] Invalid choice. Please enter a number between 1 and 6.")

    def run(self) -> None:
        """
        Run the main menu loop.

        Displays menu, gets user input, and dispatches commands until exit.
        Handles unexpected errors gracefully.
        """
        while self.running:
            try:
                self.display_menu()
                choice = self.get_choice()
                self.dispatch_command(choice)
            except Exception as e:
                print(f"\n[X] Unexpected error: {e}")
                print("Please try again.\n")
