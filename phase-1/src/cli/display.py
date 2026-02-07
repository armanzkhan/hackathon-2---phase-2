"""
Display formatting module for CLI output.

This module provides functions to format todos and messages for display
in the command-line interface. All formatting is consistent and human-readable.
"""

from typing import List
from src.models.todo import Todo


def format_todo_list(todos: List[Todo]) -> str:
    """
    Format a list of todos as a readable table.

    Creates a formatted table with ID, status icon, and title columns.
    If the list is empty, returns a friendly message instead.

    Args:
        todos: List of Todo instances (can be empty)

    Returns:
        Formatted string ready for display

    Status Indicators:
        - [X] for completed todos
        - [ ] for incomplete todos

    Examples:
        >>> todos = [
        ...     Todo(id=1, title="Buy groceries", completed=False),
        ...     Todo(id=2, title="Call dentist", completed=True)
        ... ]
        >>> print(format_todo_list(todos))
        === Your Todos ===
        ID | Status | Title
        ----|--------|-------------------
        1   | [ ]    | Buy groceries
        2   | [X]    | Call dentist

        >>> print(format_todo_list([]))
        No todos found. Create one to get started!
    """
    if not todos:
        return "No todos found. Create one to get started!"

    # Header
    lines = [
        "=== Your Todos ===",
        "ID | Status | Title",
        "----|--------|-------------------"
    ]

    # Format each todo
    for todo in todos:
        status_icon = "[X]" if todo.completed else "[ ]"
        # Pad ID to 3 characters for alignment
        id_str = str(todo.id).ljust(3)
        lines.append(f"{id_str} | {status_icon}    | {todo.title}")

    return "\n".join(lines)


def format_single_todo(todo: Todo) -> str:
    """
    Format a single todo with all details.

    Shows ID, title, description, and completion status.

    Args:
        todo: Todo instance to format

    Returns:
        Formatted string with todo details

    Examples:
        >>> todo = Todo(id=1, title="Buy groceries", description="Milk, eggs", completed=False)
        >>> print(format_single_todo(todo))
        Todo #1
        Title: Buy groceries
        Description: Milk, eggs
        Status: [ ] Incomplete
    """
    status_text = "[X] Complete" if todo.completed else "[ ] Incomplete"

    lines = [
        f"Todo #{todo.id}",
        f"Title: {todo.title}",
        f"Description: {todo.description or '(no description)'}",
        f"Status: {status_text}"
    ]

    return "\n".join(lines)


def format_error(message: str) -> str:
    """
    Format an error message consistently.

    Prefixes the message with an error indicator [X] for visual consistency.

    Args:
        message: Error message text

    Returns:
        Formatted error message

    Examples:
        >>> format_error("Title cannot be empty")
        '[X] Error: Title cannot be empty'

        >>> format_error("Todo with ID 999 not found")
        '[X] Error: Todo with ID 999 not found'
    """
    return f"[X] Error: {message}"


def format_success(message: str) -> str:
    """
    Format a success message consistently.

    Prefixes the message with a success indicator [OK] for visual consistency.

    Args:
        message: Success message text

    Returns:
        Formatted success message

    Examples:
        >>> format_success("Todo created with ID 1")
        '[OK] Todo created with ID 1'

        >>> format_success("Todo 2 deleted successfully")
        '[OK] Todo 2 deleted successfully'
    """
    return f"[OK] {message}"
