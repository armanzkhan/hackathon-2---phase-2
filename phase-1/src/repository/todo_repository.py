"""
TodoRepository module for in-memory CRUD operations.

This module provides the TodoRepository class which manages all todo storage
and operations in memory. Storage is ephemeral and lost on application exit.
"""

from typing import Optional
from src.models.todo import Todo


class TodoRepository:
    """
    In-memory repository for Todo entities.

    Manages CRUD operations for todos using a dictionary for O(1) lookups.
    IDs are auto-generated using a simple counter starting at 1.

    Storage:
        - Internal dict mapping ID -> Todo instance
        - Counter for next available ID
        - All data is ephemeral (lost on exit)

    ID Generation:
        - Simple counter starting at 1
        - Incremented on each create
        - IDs never reused (even after deletion)

    Performance:
        - Create: O(1)
        - Read by ID: O(1)
        - Read all: O(n log n) due to sorting
        - Update: O(1)
        - Delete: O(1)

    Examples:
        >>> repo = TodoRepository()
        >>> todo = repo.create("Buy groceries", "Milk, eggs")
        >>> todo.id
        1
        >>> all_todos = repo.get_all()
        >>> len(all_todos)
        1
    """

    def __init__(self) -> None:
        """
        Initialize empty repository.

        Post-conditions:
            - Storage is empty (no todos)
            - Next ID is set to 1
        """
        self._storage: dict[int, Todo] = {}
        self._next_id: int = 1

    def create(self, title: str, description: str = "") -> Todo:
        """
        Create new todo with auto-generated ID.

        Args:
            title: Task description (non-empty required)
            description: Optional details (default: empty string)

        Returns:
            Created Todo instance with unique ID

        Raises:
            ValueError: If title is empty or whitespace-only

        Post-conditions:
            - New todo stored in repository
            - ID counter incremented
            - Returned todo has completed=False
            - ID is unique and never reused

        Examples:
            >>> repo = TodoRepository()
            >>> todo1 = repo.create("Task 1")
            >>> todo1.id
            1
            >>> todo2 = repo.create("Task 2", "Description")
            >>> todo2.id
            2
        """
        # Create todo with current ID (validation happens in Todo.__post_init__)
        todo = Todo(
            id=self._next_id,
            title=title,
            description=description,
            completed=False
        )

        # Store todo
        self._storage[self._next_id] = todo

        # Increment ID for next todo
        self._next_id += 1

        return todo

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        """
        Retrieve todo by unique ID.

        Args:
            todo_id: Unique identifier

        Returns:
            Todo instance if found, None if not found

        Post-conditions:
            - Repository state unchanged (read-only)

        Examples:
            >>> repo = TodoRepository()
            >>> todo = repo.create("Task")
            >>> found = repo.get_by_id(1)
            >>> found.title
            'Task'
            >>> not_found = repo.get_by_id(999)
            >>> not_found is None
            True
        """
        return self._storage.get(todo_id)

    def get_all(self) -> list[Todo]:
        """
        Retrieve all todos sorted by ID (ascending).

        Returns:
            List of Todo instances sorted by ID
            Empty list if no todos exist

        Post-conditions:
            - Repository state unchanged (read-only)
            - Returned list sorted by ID (1, 2, 3, ...)

        Examples:
            >>> repo = TodoRepository()
            >>> repo.create("Task 1")
            >>> repo.create("Task 2")
            >>> todos = repo.get_all()
            >>> len(todos)
            2
            >>> [t.id for t in todos]
            [1, 2]
        """
        # Return sorted list of todos by ID
        return sorted(self._storage.values(), key=lambda t: t.id)

    def update(
        self,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Todo:
        """
        Update todo fields (preserves completion status).

        Args:
            todo_id: Unique identifier
            title: New title (None = no change)
            description: New description (None = no change)

        Returns:
            Updated Todo instance

        Raises:
            KeyError: If todo_id not found
            ValueError: If new title is empty/whitespace

        Post-conditions:
            - Todo fields updated as specified
            - Completion status preserved
            - ID unchanged

        Examples:
            >>> repo = TodoRepository()
            >>> todo = repo.create("Old Title")
            >>> updated = repo.update(1, title="New Title")
            >>> updated.title
            'New Title'
        """
        # Check if todo exists
        if todo_id not in self._storage:
            raise KeyError(f"Todo with ID {todo_id} not found")

        # Get existing todo
        existing_todo = self._storage[todo_id]

        # Create updated todo (immutable update)
        updated_todo = existing_todo.update(title=title, description=description)

        # Store updated todo
        self._storage[todo_id] = updated_todo

        return updated_todo

    def delete(self, todo_id: int) -> bool:
        """
        Delete todo by ID.

        Args:
            todo_id: Unique identifier

        Returns:
            True if deleted, False if not found

        Post-conditions:
            - Todo removed from storage if found
            - Storage unchanged if not found
            - ID never reused after deletion

        Examples:
            >>> repo = TodoRepository()
            >>> todo = repo.create("Task")
            >>> repo.delete(1)
            True
            >>> repo.delete(1)
            False
        """
        if todo_id in self._storage:
            del self._storage[todo_id]
            return True
        return False

    def mark_complete(self, todo_id: int) -> Todo:
        """
        Mark todo as complete (set completed=True).

        Args:
            todo_id: Unique identifier

        Returns:
            Updated Todo instance with completed=True

        Raises:
            KeyError: If todo_id not found

        Post-conditions:
            - Todo's completed field set to True
            - Other fields (title, description) preserved
            - ID unchanged

        Examples:
            >>> repo = TodoRepository()
            >>> todo = repo.create("Task")
            >>> completed = repo.mark_complete(1)
            >>> completed.completed
            True
        """
        # Check if todo exists
        if todo_id not in self._storage:
            raise KeyError(f"Todo with ID {todo_id} not found")

        # Get existing todo and mark complete
        existing_todo = self._storage[todo_id]
        completed_todo = existing_todo.mark_complete()

        # Store updated todo
        self._storage[todo_id] = completed_todo

        return completed_todo

    def exists(self, todo_id: int) -> bool:
        """
        Check if todo exists by ID.

        Args:
            todo_id: Unique identifier

        Returns:
            True if todo exists, False otherwise

        Post-conditions:
            - Repository state unchanged (read-only)

        Examples:
            >>> repo = TodoRepository()
            >>> repo.create("Task")
            >>> repo.exists(1)
            True
            >>> repo.exists(999)
            False
        """
        return todo_id in self._storage
