# Repository Contract: TodoRepository

**Feature**: 001-todo-crud | **Date**: 2026-02-07

## Purpose

This contract defines the interface and behavioral guarantees for the TodoRepository class, which manages in-memory CRUD operations for Todo entities.

## Interface Definition

```python
class TodoRepository:
    """
    In-memory repository for Todo entities.

    Responsibilities:
    - Generate unique IDs for todos
    - Store and retrieve todos in memory
    - Ensure data integrity (unique IDs, validation)
    - Provide CRUD operations
    """

    def __init__(self) -> None:
        """
        Initialize empty repository.

        Post-conditions:
        - Storage is empty (no todos)
        - Next ID is set to 1
        """

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

        Guarantees:
            - Operation is atomic (no partial state)
            - ID uniqueness across all creates
            - Title validation performed
        """

    def get_by_id(self, todo_id: int) -> Todo | None:
        """
        Retrieve todo by unique ID.

        Args:
            todo_id: Unique identifier

        Returns:
            Todo instance if found, None if not found

        Raises:
            None (returns None instead of raising exceptions)

        Post-conditions:
            - Repository state unchanged (read-only)

        Guarantees:
            - Returns None for invalid/non-existent IDs
            - Returns immutable Todo (caller cannot modify storage)
        """

    def get_all(self) -> list[Todo]:
        """
        Retrieve all todos sorted by ID (ascending).

        Args:
            None

        Returns:
            List of Todo instances sorted by ID
            Empty list if no todos exist

        Raises:
            None

        Post-conditions:
            - Repository state unchanged (read-only)
            - Returned list sorted by ID (1, 2, 3, ...)

        Guarantees:
            - Always returns list (never None)
            - List is copy (caller cannot modify storage)
            - Sorting is consistent (same order every call)
        """

    def update(self, todo_id: int, title: str | None = None,
               description: str | None = None) -> Todo:
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

        Guarantees:
            - Operation is atomic (no partial updates)
            - Title validation performed if title provided
            - Completion status never changed
            - Returns new immutable instance
        """

    def delete(self, todo_id: int) -> bool:
        """
        Delete todo by ID.

        Args:
            todo_id: Unique identifier

        Returns:
            True if deleted, False if not found

        Raises:
            None (returns False instead of raising)

        Post-conditions:
            - Todo removed from storage if found
            - Storage unchanged if not found

        Guarantees:
            - ID never reused after deletion
            - Operation is atomic
            - Idempotent (multiple deletes safe)
        """

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

        Guarantees:
            - Operation is atomic
            - Idempotent (marking complete multiple times safe)
            - Returns new immutable instance
        """

    def exists(self, todo_id: int) -> bool:
        """
        Check if todo exists by ID.

        Args:
            todo_id: Unique identifier

        Returns:
            True if todo exists, False otherwise

        Raises:
            None

        Post-conditions:
            - Repository state unchanged (read-only)

        Guarantees:
            - Fast O(1) check
            - No side effects
        """
```

## Contract Guarantees

### Atomicity
- All write operations (create, update, delete, mark_complete) are atomic
- No partial state changes (either fully succeeds or fully fails)
- No race conditions (single-threaded application)

### ID Uniqueness
- Every created todo gets a unique ID
- IDs are sequential integers starting at 1
- IDs never reused, even after deletion
- No ID collisions even with 1000+ creates

### Immutability
- Returned Todo instances are immutable (frozen dataclass)
- Caller cannot modify repository state through returned objects
- Update/mark_complete return NEW instances (replace pattern)

### Validation
- Title validation performed in create() and update()
- Empty or whitespace-only titles rejected with ValueError
- Description has no validation (any string accepted)

### Error Handling
- Read operations (get_by_id, get_all, exists) never raise exceptions
- Write operations raise exceptions only for validation failures or not-found
- Consistent error types:
  - ValueError: Validation failures (empty title)
  - KeyError: Todo not found (update, mark_complete)

### Idempotency
- delete(): Deleting non-existent ID returns False (safe)
- mark_complete(): Marking complete multiple times is safe
- get operations: Always safe to call multiple times

### Performance
- All operations are O(1) except get_all() which is O(n log n)
- No I/O overhead (all operations in-memory)
- Fast enough for 500+ todos (per constitution)

## Invariants

**Maintained Throughout Repository Lifetime**:

1. **ID Uniqueness**: No two todos ever have the same ID
2. **ID Sequential**: IDs are assigned 1, 2, 3, ... in order
3. **No Gaps on Create**: Next ID is always (max ID + 1)
4. **Gaps on Delete**: Deleting ID 5 doesn't affect next ID (still 6, 7, ...)
5. **Storage Consistency**: _storage keys match todo.id values
6. **Counter Consistency**: _next_id equals (max ID + 1)

## Usage Examples

### Example 1: Create and Retrieve

```python
repo = TodoRepository()

# Create first todo
todo1 = repo.create("Buy groceries", "Milk, eggs, bread")
assert todo1.id == 1
assert todo1.title == "Buy groceries"
assert todo1.completed == False

# Create second todo
todo2 = repo.create("Call dentist")
assert todo2.id == 2

# Retrieve by ID
retrieved = repo.get_by_id(1)
assert retrieved == todo1

# Retrieve all
all_todos = repo.get_all()
assert len(all_todos) == 2
assert all_todos[0].id == 1
assert all_todos[1].id == 2
```

### Example 2: Update Preserves Completion Status

```python
repo = TodoRepository()

# Create and mark complete
todo = repo.create("Task 1")
completed_todo = repo.mark_complete(todo.id)
assert completed_todo.completed == True

# Update title/description
updated = repo.update(todo.id, title="Updated Task 1", description="New details")
assert updated.completed == True  # ← Completion preserved
assert updated.title == "Updated Task 1"
```

### Example 3: Delete and ID Reuse

```python
repo = TodoRepository()

# Create 3 todos
todo1 = repo.create("Task 1")  # ID: 1
todo2 = repo.create("Task 2")  # ID: 2
todo3 = repo.create("Task 3")  # ID: 3

# Delete middle todo
success = repo.delete(2)
assert success == True

# Next create gets ID 4 (not 2)
todo4 = repo.create("Task 4")  # ID: 4 (not reused)
assert todo4.id == 4

# Get all returns sorted list without deleted todo
all_todos = repo.get_all()
assert len(all_todos) == 3
assert [t.id for t in all_todos] == [1, 3, 4]
```

### Example 4: Error Handling

```python
repo = TodoRepository()

# Empty title validation
try:
    repo.create("")  # Should raise ValueError
    assert False, "Should have raised ValueError"
except ValueError as e:
    assert "empty" in str(e).lower()

# Not found handling
result = repo.get_by_id(999)
assert result is None  # Returns None, not exception

exists = repo.exists(999)
assert exists == False

# Delete non-existent
deleted = repo.delete(999)
assert deleted == False  # Returns False, not exception

# Update non-existent (raises exception)
try:
    repo.update(999, title="New")
    assert False, "Should have raised KeyError"
except KeyError:
    pass  # Expected
```

## Testing Requirements

### Unit Tests Required

1. **Create Operation**:
   - ✅ Create with valid title
   - ✅ Create with title and description
   - ✅ Create with title only (description defaults to "")
   - ❌ Create with empty title (should raise ValueError)
   - ❌ Create with whitespace-only title (should raise ValueError)
   - ✅ IDs are sequential (1, 2, 3, ...)
   - ✅ IDs are unique across 1000+ creates

2. **Read Operations**:
   - ✅ Get by ID when exists
   - ✅ Get by ID when not exists (returns None)
   - ✅ Get all when empty (returns [])
   - ✅ Get all when multiple todos exist (sorted by ID)
   - ✅ Exists returns True/False correctly

3. **Update Operation**:
   - ✅ Update title only
   - ✅ Update description only
   - ✅ Update both title and description
   - ✅ Update preserves completion status
   - ❌ Update non-existent ID (raises KeyError)
   - ❌ Update with empty title (raises ValueError)

4. **Delete Operation**:
   - ✅ Delete existing todo
   - ✅ Delete non-existent todo (returns False)
   - ✅ ID not reused after deletion
   - ✅ Multiple deletes of same ID (idempotent)

5. **Mark Complete Operation**:
   - ✅ Mark complete sets completed=True
   - ✅ Mark complete preserves other fields
   - ❌ Mark complete non-existent ID (raises KeyError)
   - ✅ Mark complete multiple times (idempotent)

6. **Invariants**:
   - ✅ IDs always unique
   - ✅ IDs always sequential
   - ✅ Storage consistent with counter
   - ✅ No ID collisions with 1000+ operations

## Contract Versioning

**Version**: 1.0.0
**Date**: 2026-02-07
**Status**: Draft

**Breaking Changes**:
- None (initial version)

**Non-Breaking Changes**:
- None (initial version)

## Related Contracts

- [Validation Contract](./validation-contract.md) - Input validation rules
- [Data Model](../data-model.md) - Todo entity specification

## Compliance

This contract must be satisfied by the TodoRepository implementation in `src/repository/todo_repository.py`. All unit tests in `tests/unit/test_repository.py` must verify contract compliance.
