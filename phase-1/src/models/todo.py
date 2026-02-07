"""
Todo domain entity module.

This module defines the Todo entity as an immutable dataclass with built-in
validation. All todos are frozen (immutable) after creation to prevent
accidental state mutation.
"""

from dataclasses import dataclass, replace
from typing import Optional


@dataclass(frozen=True)
class Todo:
    """
    Immutable Todo entity representing a task or item to be completed.

    Attributes:
        id: Unique integer identifier (auto-assigned by repository)
        title: Task description (required, non-empty after strip)
        description: Optional detailed information (default: empty string)
        completed: Boolean flag indicating completion status (default: False)

    Validation:
        - Title must not be empty or whitespace-only
        - Validation occurs in __post_init__, raises ValueError if invalid

    Immutability:
        - All fields are frozen after creation
        - Use update() or mark_complete() methods to create modified copies

    Examples:
        >>> todo = Todo(id=1, title="Buy groceries")
        >>> todo.title
        'Buy groceries'
        >>> todo.completed
        False

        >>> completed_todo = todo.mark_complete()
        >>> completed_todo.completed
        True
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False

    def __post_init__(self) -> None:
        """
        Validate todo after initialization.

        Validates that the title is non-empty after stripping whitespace.
        This ensures invalid todos can never exist in the system.

        Raises:
            ValueError: If title is empty or whitespace-only
        """
        # Validate title is non-empty after stripping whitespace
        if not self.title.strip():
            raise ValueError("Title cannot be empty")

    def update(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> 'Todo':
        """
        Create a new Todo instance with updated fields.

        Returns a new Todo with the specified fields updated while preserving
        all other fields including completion status. This maintains immutability.

        Args:
            title: New title (None = no change)
            description: New description (None = no change)

        Returns:
            New Todo instance with updated fields

        Raises:
            ValueError: If new title is empty or whitespace-only

        Examples:
            >>> todo = Todo(id=1, title="Old Title", description="Old desc")
            >>> updated = todo.update(title="New Title")
            >>> updated.title
            'New Title'
            >>> updated.description
            'Old desc'
        """
        updates = {}
        if title is not None:
            updates['title'] = title
        if description is not None:
            updates['description'] = description

        # Create new instance with updates
        new_todo = replace(self, **updates)

        # Trigger validation by accessing __post_init__ logic
        # The dataclass replace creates a new instance which triggers __post_init__
        return new_todo

    def mark_complete(self) -> 'Todo':
        """
        Create a new Todo instance marked as complete.

        Returns a new Todo with completed=True while preserving all other fields.
        This operation is idempotent (marking complete multiple times is safe).

        Returns:
            New Todo instance with completed=True

        Examples:
            >>> todo = Todo(id=1, title="Task", completed=False)
            >>> completed = todo.mark_complete()
            >>> completed.completed
            True
            >>> completed.title
            'Task'
        """
        return replace(self, completed=True)
