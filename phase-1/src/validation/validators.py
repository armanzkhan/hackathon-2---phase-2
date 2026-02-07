"""
Input validation module.

This module provides centralized validation functions for user input.
All validators return tuples with consistent format instead of raising exceptions,
allowing callers to handle validation failures explicitly.
"""

from typing import Tuple


def validate_title(title: str) -> Tuple[bool, str]:
    """
    Validate todo title.

    Rules:
        - Title must not be empty string
        - Title must not be whitespace-only
        - Leading/trailing whitespace ignored (stripped before check)

    Args:
        title: User-provided title string

    Returns:
        Tuple of (is_valid, error_message):
        - (True, "") if valid
        - (False, error_message) if invalid

    Raises:
        None (errors returned in tuple)

    Examples:
        >>> validate_title("Buy groceries")
        (True, '')

        >>> validate_title("")
        (False, 'Title cannot be empty')

        >>> validate_title("   ")
        (False, 'Title cannot be empty')

        >>> validate_title("  Valid Title  ")
        (True, '')
    """
    stripped = title.strip()
    if not stripped:
        return (False, "Title cannot be empty")
    return (True, "")


def validate_id(id_str: str) -> Tuple[bool, int, str]:
    """
    Validate and parse todo ID.

    Rules:
        - Must be parseable as integer
        - Must be positive (> 0)
        - Leading/trailing whitespace allowed (stripped)

    Args:
        id_str: User-provided ID string

    Returns:
        Tuple of (is_valid, parsed_id, error_message):
        - (True, id, "") if valid
        - (False, 0, error_message) if invalid

    Raises:
        None (errors returned in tuple)

    Examples:
        >>> validate_id("1")
        (True, 1, '')

        >>> validate_id("42")
        (True, 42, '')

        >>> validate_id("abc")
        (False, 0, 'Invalid ID format. Please enter a number.')

        >>> validate_id("-5")
        (False, 0, 'ID must be positive')

        >>> validate_id("0")
        (False, 0, 'ID must be positive')

        >>> validate_id("  123  ")
        (True, 123, '')
    """
    try:
        todo_id = int(id_str.strip())
        if todo_id <= 0:
            return (False, 0, "ID must be positive")
        return (True, todo_id, "")
    except ValueError:
        return (False, 0, "Invalid ID format. Please enter a number.")


def validate_description(description: str) -> Tuple[bool, str]:
    """
    Validate todo description.

    Rules:
        - Any string accepted (including empty)
        - No length restrictions

    Args:
        description: User-provided description string

    Returns:
        Tuple of (is_valid, error_message):
        - Always (True, "") (no validation)

    Raises:
        None

    Examples:
        >>> validate_description("")
        (True, '')

        >>> validate_description("Any text")
        (True, '')

        >>> validate_description("Very long text" * 1000)
        (True, '')
    """
    # Descriptions have no validation rules
    return (True, "")
