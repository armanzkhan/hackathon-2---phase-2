"""
CLI command handlers for todo operations.

This module provides command handler functions that connect user input
to repository operations. Each handler includes input validation,
error handling, and success confirmations.
"""

from src.repository.todo_repository import TodoRepository
from src.validation.validators import validate_title, validate_id
from src.cli.display import (
    format_todo_list,
    format_error,
    format_success
)


def handle_create(repository: TodoRepository) -> None:
    """
    Handle the create todo command.

    Prompts user for title and description, validates input, creates the todo,
    and displays confirmation or error message.

    Args:
        repository: TodoRepository instance

    Examples:
        >>> repo = TodoRepository()
        >>> # User enters: "Buy groceries" and "Milk, eggs"
        >>> handle_create(repo)
        ✔ Todo created with ID 1
    """
    # Prompt for title
    title = input("Enter title: ")

    # Validate title
    is_valid, error = validate_title(title)
    if not is_valid:
        print(format_error(error))
        return

    # Prompt for description (optional)
    description = input("Enter description (optional): ")

    # Create todo
    try:
        todo = repository.create(title, description)
        print(format_success(f"Todo created with ID {todo.id}"))
    except ValueError as e:
        print(format_error(str(e)))


def handle_list(repository: TodoRepository) -> None:
    """
    Handle the list todos command.

    Retrieves all todos and displays them in a formatted table.

    Args:
        repository: TodoRepository instance

    Examples:
        >>> repo = TodoRepository()
        >>> repo.create("Task 1")
        >>> repo.create("Task 2")
        >>> handle_list(repo)
        === Your Todos ===
        ID | Status | Title
        ----|--------|-------------------
        1   | ✘      | Task 1
        2   | ✘      | Task 2
    """
    todos = repository.get_all()
    print(format_todo_list(todos))


def handle_update(repository: TodoRepository) -> None:
    """
    Handle the update todo command.

    Prompts user for todo ID and new values, validates input, updates the todo,
    and displays confirmation or error message.

    Args:
        repository: TodoRepository instance

    Examples:
        >>> repo = TodoRepository()
        >>> todo = repo.create("Old Title")
        >>> # User enters: "1", "New Title", "New Description"
        >>> handle_update(repo)
        ✔ Todo 1 updated successfully
    """
    # Prompt for ID
    id_str = input("Enter todo ID: ")

    # Validate ID
    is_valid, todo_id, error = validate_id(id_str)
    if not is_valid:
        print(format_error(error))
        return

    # Check if todo exists
    if not repository.exists(todo_id):
        print(format_error(f"Todo with ID {todo_id} not found"))
        return

    # Prompt for new values
    new_title = input("Enter new title (or press Enter to skip): ")
    new_description = input("Enter new description (or press Enter to skip): ")

    # Process inputs (None = no change)
    title_to_update = new_title if new_title else None
    description_to_update = new_description if new_description else None

    # Validate new title if provided
    if title_to_update:
        is_valid, error = validate_title(title_to_update)
        if not is_valid:
            print(format_error(error))
            return

    # Update todo
    try:
        repository.update(todo_id, title=title_to_update, description=description_to_update)
        print(format_success(f"Todo {todo_id} updated successfully"))
    except (KeyError, ValueError) as e:
        print(format_error(str(e)))


def handle_delete(repository: TodoRepository) -> None:
    """
    Handle the delete todo command.

    Prompts user for todo ID, validates input, deletes the todo,
    and displays confirmation or error message.

    Args:
        repository: TodoRepository instance

    Examples:
        >>> repo = TodoRepository()
        >>> todo = repo.create("Task to delete")
        >>> # User enters: "1"
        >>> handle_delete(repo)
        ✔ Todo 1 deleted successfully
    """
    # Prompt for ID
    id_str = input("Enter todo ID: ")

    # Validate ID
    is_valid, todo_id, error = validate_id(id_str)
    if not is_valid:
        print(format_error(error))
        return

    # Check if todo exists
    if not repository.exists(todo_id):
        print(format_error(f"Todo with ID {todo_id} not found"))
        return

    # Delete todo
    repository.delete(todo_id)
    print(format_success(f"Todo {todo_id} deleted successfully"))


def handle_complete(repository: TodoRepository) -> None:
    """
    Handle the mark complete command.

    Prompts user for todo ID, validates input, marks the todo as complete,
    and displays confirmation or error message.

    Args:
        repository: TodoRepository instance

    Examples:
        >>> repo = TodoRepository()
        >>> todo = repo.create("Task to complete")
        >>> # User enters: "1"
        >>> handle_complete(repo)
        ✔ Todo 1 marked as complete
    """
    # Prompt for ID
    id_str = input("Enter todo ID: ")

    # Validate ID
    is_valid, todo_id, error = validate_id(id_str)
    if not is_valid:
        print(format_error(error))
        return

    # Check if todo exists
    if not repository.exists(todo_id):
        print(format_error(f"Todo with ID {todo_id} not found"))
        return

    # Mark complete
    try:
        repository.mark_complete(todo_id)
        print(format_success(f"Todo {todo_id} marked as complete"))
    except KeyError as e:
        print(format_error(str(e)))
