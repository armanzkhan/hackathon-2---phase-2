# Implementation Plan: Todo In-Memory Console Application

**Branch**: `001-todo-crud` | **Date**: 2026-02-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-todo-crud/spec.md`

## Summary

Implement a Python 3.13+ command-line todo management application with full CRUD operations (Create, Read, Update, Delete, Mark Complete) stored entirely in runtime memory. The application follows strict Spec-Driven Development with a three-layer architecture: CLI interface for user interaction, domain model for business logic, and in-memory repository for data management. No external dependencies or persistence mechanisms are used.

**Technical Approach**: Pure Python standard library implementation with modular separation of concerns, comprehensive input validation, and human-readable CLI output.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Standard library only (no external packages)
**Storage**: In-memory collection (dict/list) - ephemeral, no persistence
**Testing**: unittest (Python standard library)
**Target Platform**: Cross-platform (Windows, Linux, macOS) - any OS with Python 3.13+
**Project Type**: Single console application
**Performance Goals**: Operations complete in < 5 seconds, support 500+ todos without degradation
**Constraints**: No file I/O, no databases, < 1 second startup/shutdown, deterministic behavior
**Scale/Scope**: Single-user, personal task management (designed for 100-1000 todos)

## Constitution Check

*GATE: Must pass before implementation. Verifying against constitution v1.0.0*

### ✅ Spec-Driven Development (Principle I)
- [x] Specification exists and is approved (`specs/001-todo-crud/spec.md`)
- [x] All functional requirements documented (FR-001 to FR-018)
- [x] Implementation plan derived from spec only (this document)
- [x] No manual coding or logic injection planned

### ✅ In-Memory Only Storage (Principle II)
- [x] No file-based persistence (`.json`, `.txt`, `.db` files)
- [x] No database systems (SQLite, PostgreSQL, etc.)
- [x] No web frameworks (Flask, FastAPI, Django)
- [x] No background services or daemons
- [x] No AI/LLM integrations
- [x] In-memory storage only: Python dict for ID-to-Todo mapping

### ✅ Python 3.13+ Requirement (Principle III)
- [x] Target version: Python 3.13+
- [x] Type hints for all function signatures
- [x] Modern Python features (dataclasses, type annotations)

### ✅ CLI-First Interface (Principle IV)
- [x] Command-line interface using standard input/output
- [x] Human-readable output format
- [x] Clear menu-driven interaction
- [x] Deterministic behavior

### ✅ Modular Architecture (Principle V)
- [x] CLI Layer: Command parsing and user interaction (`src/cli/`)
- [x] Domain Model: Business logic and Todo entities (`src/models/`)
- [x] Data Handling: In-memory repository (`src/repository/`)
- [x] Single Responsibility Principle enforced

### ✅ Clean Code Standards (Principle VI)
- [x] Human-readable CLI output
- [x] Clear naming conventions
- [x] Type hints for all functions
- [x] Comprehensive docstrings
- [x] Deterministic and predictable behavior

**Constitution Compliance**: ✅ **PASS** - All principles satisfied, no violations

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-crud/
├── spec.md                    # Feature specification (complete)
├── plan.md                    # This implementation plan
├── data-model.md              # Domain model and data structures
├── contracts/                 # Interface contracts
│   ├── repository-contract.md # TodoRepository interface
│   └── validation-contract.md # Input validation rules
├── quickstart.md              # Development and usage guide
└── tasks.md                   # Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
src/
├── models/
│   └── todo.py               # Todo entity (dataclass with validation)
├── repository/
│   └── todo_repository.py    # In-memory CRUD operations
├── cli/
│   ├── __init__.py
│   ├── menu.py               # Main menu and command loop
│   ├── commands.py           # Command handlers (create, list, update, etc.)
│   └── display.py            # Output formatting and display logic
├── validation/
│   └── validators.py         # Input validation functions
└── main.py                   # Application entry point

tests/
├── unit/
│   ├── test_todo_model.py    # Todo entity tests
│   ├── test_repository.py    # Repository operations tests
│   ├── test_validators.py    # Validation logic tests
│   └── test_display.py       # Display formatting tests
└── integration/
    └── test_cli_integration.py # End-to-end CLI workflow tests

# Root files
README.md                      # Project overview and usage
requirements.txt               # Empty (no external dependencies)
```

**Structure Decision**: Single project structure selected. This is a standalone console application with no frontend/backend separation needed. The three-layer architecture (CLI → Domain → Repository) maps cleanly to the `src/` directory structure with clear separation of concerns.

## Complexity Tracking

> No constitution violations - this section is empty (N/A)

## Architecture Design

### Layer 1: Domain Model (`src/models/`)

**Purpose**: Define the Todo entity with built-in validation and business rules.

**Todo Entity** (`src/models/todo.py`):
- Implemented as Python dataclass for immutability and type safety
- Fields:
  - `id: int` - Unique identifier (set by repository, immutable after creation)
  - `title: str` - Task description (required, validated non-empty)
  - `description: str` - Optional details (default: empty string)
  - `completed: bool` - Completion status (default: False)
- Validation methods:
  - `validate_title()` - Ensures title is non-empty after stripping whitespace
  - `update()` - Returns new Todo instance with updated fields (immutability)
  - `mark_complete()` - Returns new Todo instance with completed=True

**Key Design Decisions**:
- **Immutability**: Todo instances are immutable after creation (use `replace()` pattern)
- **Validation at creation**: Title validation happens in `__post_init__`
- **No persistence logic**: Domain model knows nothing about storage

**Rationale**: Immutable entities prevent accidental state mutation and make testing easier. Validation at construction ensures invalid todos never exist in the system.

### Layer 2: Repository (`src/repository/`)

**Purpose**: Manage in-memory storage and provide CRUD operations.

**TodoRepository** (`src/repository/todo_repository.py`):
- Single class responsible for all data operations
- Internal storage: `dict[int, Todo]` - maps ID to Todo instance
- ID generation: Simple counter (`self._next_id`) incremented on create
- Operations:
  - `create(title: str, description: str = "") -> Todo` - Add new todo
  - `get_by_id(todo_id: int) -> Todo | None` - Retrieve single todo
  - `get_all() -> list[Todo]` - Retrieve all todos (sorted by ID)
  - `update(todo_id: int, title: str | None, description: str | None) -> Todo` - Update existing todo
  - `delete(todo_id: int) -> bool` - Remove todo, returns success status
  - `mark_complete(todo_id: int) -> Todo` - Mark todo as complete
  - `exists(todo_id: int) -> bool` - Check if ID exists

**Key Design Decisions**:
- **Single repository instance**: Passed to CLI commands (dependency injection pattern)
- **Auto-incrementing IDs**: Simple counter ensures uniqueness
- **Return immutable copies**: Repository returns Todo instances, not references
- **No exceptions for not-found**: Returns `None` for flexibility in error handling

**Rationale**: Centralized data management ensures ID uniqueness and provides single source of truth. Dictionary storage gives O(1) lookup performance.

### Layer 3: CLI Interface (`src/cli/`)

**Purpose**: Handle user interaction, command parsing, and output display.

**Menu System** (`src/cli/menu.py`):
- Main loop displaying menu options and processing user choices
- Menu options:
  1. Create a new todo
  2. View all todos
  3. Update a todo
  4. Delete a todo
  5. Mark todo as complete
  6. Exit application
- Input handling: Read choice, validate, dispatch to appropriate command handler
- Error handling: Catch exceptions and display user-friendly messages

**Command Handlers** (`src/cli/commands.py`):
- `handle_create(repository: TodoRepository)` - Prompt for title/description, create todo
- `handle_list(repository: TodoRepository)` - Display all todos with formatting
- `handle_update(repository: TodoRepository)` - Prompt for ID and new values, update todo
- `handle_delete(repository: TodoRepository)` - Prompt for ID, delete todo
- `handle_complete(repository: TodoRepository)` - Prompt for ID, mark complete
- Each handler includes:
  - Input prompting with clear instructions
  - Validation (non-empty titles, numeric IDs)
  - Error handling (invalid IDs, validation failures)
  - Success confirmation messages

**Display Formatter** (`src/cli/display.py`):
- `format_todo_list(todos: list[Todo]) -> str` - Format todos as readable table
- `format_single_todo(todo: Todo) -> str` - Format single todo details
- `format_error(message: str) -> str` - Format error messages consistently
- `format_success(message: str) -> str` - Format success messages
- Display conventions:
  - Completed: ✔ symbol
  - Incomplete: ✘ symbol
  - Empty list: "No todos found. Create one to get started!"
  - ID padding for alignment
  - Title/description truncation if needed

**Key Design Decisions**:
- **Menu-driven interface**: Simple numbered menu (more user-friendly than command parsing)
- **Separation of concerns**: Commands handle logic, display handles formatting
- **Consistent error messages**: All errors formatted uniformly
- **Validation at CLI layer**: Invalid input caught before reaching repository

**Rationale**: Menu-driven interface is simpler for users than command-line arguments. Separating display logic enables easy testing and future formatting changes.

### Validation Layer (`src/validation/`)

**Purpose**: Centralize input validation rules for reuse across CLI and tests.

**Validators** (`src/validation/validators.py`):
- `validate_title(title: str) -> tuple[bool, str]` - Check non-empty, return (valid, error_msg)
- `validate_id(id_str: str) -> tuple[bool, int, str]` - Parse and validate ID, return (valid, id, error_msg)
- `validate_description(description: str) -> tuple[bool, str]` - Validate description (currently always passes)

**Key Design Decisions**:
- **Return tuples**: Include validation result, parsed value (if applicable), and error message
- **No exceptions**: Validators return structured results for caller to handle
- **Reusable**: Used by both CLI commands and tests

**Rationale**: Centralized validation ensures consistent rules across application. Tuple returns avoid exceptions for expected validation failures.

## Data Model Design

### Todo Entity Schema

```python
@dataclass(frozen=True)
class Todo:
    id: int
    title: str
    description: str = ""
    completed: bool = False
```

**Field Specifications**:

| Field | Type | Required | Default | Constraints | Mutability |
|-------|------|----------|---------|-------------|------------|
| id | int | Yes | (assigned) | > 0, unique | Immutable |
| title | str | Yes | N/A | Non-empty after strip | Immutable |
| description | str | No | "" | No length limit | Immutable |
| completed | bool | Yes | False | True/False only | Immutable |

**Validation Rules**:
1. **Title validation** (FR-003):
   - Must not be empty string
   - Must not be whitespace-only (`title.strip() != ""`)
   - Performed in `__post_init__` method
   - Raises `ValueError` if validation fails

2. **ID validation** (FR-002, FR-015):
   - Auto-assigned by repository (not user-provided)
   - Must be unique integer > 0
   - Enforced by repository's ID counter
   - Immutable once assigned

3. **Completion status** (FR-004):
   - Defaults to `False` on creation
   - Only changed via `mark_complete()` method
   - Boolean type ensures only True/False values

**Relationships**: None - standalone entity with no foreign keys or references

### Repository Storage Schema

**Internal Structure**:
```python
class TodoRepository:
    _storage: dict[int, Todo]  # Maps ID -> Todo instance
    _next_id: int              # Counter for ID generation
```

**Operations Mapping**:

| Operation | Spec Requirement | Method | Time Complexity |
|-----------|------------------|--------|-----------------|
| Create | FR-001, FR-002 | `create(title, description)` | O(1) |
| Read (single) | FR-006 | `get_by_id(id)` | O(1) |
| Read (all) | FR-006 | `get_all()` | O(n log n)* |
| Update | FR-009, FR-010 | `update(id, title, description)` | O(1) |
| Delete | FR-012 | `delete(id)` | O(1) |
| Mark Complete | FR-011 | `mark_complete(id)` | O(1) |

*Sorted by ID for consistent display order

**ID Generation Strategy**:
- Simple counter starting at 1
- Incremented on each `create()` call
- Never reused (even after deletion)
- Thread-safe for single-threaded application

**Rationale**: Dictionary provides O(1) lookups for all operations. ID counter ensures uniqueness without complex collision checking. No need for database-style indexes since all operations are in-memory.

## Interface Contracts

### Repository Contract

**Contract**: TodoRepository must implement these operations with specified behavior.

```python
class TodoRepository:
    def create(self, title: str, description: str = "") -> Todo:
        """
        Create new todo with auto-generated ID.

        Args:
            title: Non-empty task description (validated)
            description: Optional details (default: empty string)

        Returns:
            Created Todo instance with assigned ID

        Raises:
            ValueError: If title is empty or whitespace-only
        """

    def get_by_id(self, todo_id: int) -> Todo | None:
        """
        Retrieve todo by ID.

        Args:
            todo_id: Unique identifier

        Returns:
            Todo instance if found, None otherwise
        """

    def get_all(self) -> list[Todo]:
        """
        Retrieve all todos sorted by ID.

        Returns:
            List of Todo instances (empty list if none exist)
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
        """

    def delete(self, todo_id: int) -> bool:
        """
        Delete todo by ID.

        Args:
            todo_id: Unique identifier

        Returns:
            True if deleted, False if not found
        """

    def mark_complete(self, todo_id: int) -> Todo:
        """
        Mark todo as complete.

        Args:
            todo_id: Unique identifier

        Returns:
            Updated Todo instance with completed=True

        Raises:
            KeyError: If todo_id not found
        """

    def exists(self, todo_id: int) -> bool:
        """
        Check if todo exists.

        Args:
            todo_id: Unique identifier

        Returns:
            True if exists, False otherwise
        """
```

**Contract Guarantees**:
- IDs are unique and never reused
- All operations are atomic (no partial updates)
- Todos are immutable (methods return new instances)
- No side effects on failed operations
- Empty lists/None returned instead of exceptions where appropriate

### Validation Contract

**Contract**: Input validation functions with consistent return format.

```python
def validate_title(title: str) -> tuple[bool, str]:
    """
    Validate todo title.

    Args:
        title: User-provided title string

    Returns:
        (is_valid, error_message)
        - (True, "") if valid
        - (False, "Title cannot be empty") if invalid
    """

def validate_id(id_str: str) -> tuple[bool, int, str]:
    """
    Validate and parse todo ID.

    Args:
        id_str: User-provided ID string

    Returns:
        (is_valid, parsed_id, error_message)
        - (True, id, "") if valid integer
        - (False, 0, "Invalid ID format") if not numeric
    """
```

**Contract Guarantees**:
- No exceptions raised (return error info instead)
- Consistent tuple return format
- Empty error message indicates success
- Validation matches domain model rules

## CLI User Flow

### Main Menu Loop

```
=== Todo Manager ===
1. Create a new todo
2. View all todos
3. Update a todo
4. Delete a todo
5. Mark todo as complete
6. Exit

Enter your choice (1-6): _
```

**Flow**: Display menu → Read input → Validate choice → Execute command → Display result → Return to menu

### Command Flows

**1. Create Todo** (FR-001, FR-002, FR-003, FR-004, FR-018):
```
Enter title: Buy groceries
Enter description (optional): Milk, eggs, bread
✔ Todo created with ID 1
```

**2. View All Todos** (FR-006, FR-007, FR-008):
```
=== Your Todos ===
ID | Status | Title
----|--------|-------------------
1   | ✘      | Buy groceries
2   | ✔      | Call dentist
3   | ✘      | Finish project report
```

**3. Update Todo** (FR-009, FR-010, FR-013, FR-014):
```
Enter todo ID: 1
Enter new title (or press Enter to skip): Buy groceries and snacks
Enter new description (or press Enter to skip): Milk, eggs, bread, chips
✔ Todo 1 updated successfully
```

**4. Delete Todo** (FR-012, FR-013):
```
Enter todo ID: 2
✔ Todo 2 deleted successfully
```

**5. Mark Complete** (FR-011, FR-013):
```
Enter todo ID: 1
✔ Todo 1 marked as complete
```

**Error Handling Examples** (FR-013, FR-014):
```
# Empty title
Enter title:
✘ Error: Title cannot be empty

# Invalid ID
Enter todo ID: abc
✘ Error: Invalid ID format. Please enter a number.

# Non-existent ID
Enter todo ID: 999
✘ Error: Todo with ID 999 not found
```

## Entry Point Design

**Main Entry Point** (`src/main.py`):

```python
def main():
    """Application entry point."""
    repository = TodoRepository()
    menu = TodoMenu(repository)

    print("Welcome to Todo Manager!")
    print("All data is stored in memory and will be lost on exit.\n")

    try:
        menu.run()  # Start main menu loop
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"\n✘ Unexpected error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
```

**Startup Behavior** (FR-016, SC-009):
- Initialize empty repository
- Display welcome message
- Enter menu loop
- No file I/O or database connections
- < 1 second startup time

**Shutdown Behavior** (SC-009):
- Exit menu loop
- Display goodbye message
- No cleanup needed (data is ephemeral)
- < 1 second shutdown time

**Error Handling**:
- Catch `KeyboardInterrupt` (Ctrl+C) for graceful exit
- Catch unexpected exceptions and display error
- Non-zero exit code on error

## Testing Strategy

### Unit Tests

**Test Coverage Requirements**:
- Every domain model method
- Every repository operation
- Every validation function
- Every display formatter

**Test Files**:

1. `tests/unit/test_todo_model.py`:
   - Todo creation with valid data
   - Todo creation with invalid title (empty, whitespace)
   - Todo immutability (cannot modify fields directly)
   - Todo update methods return new instances
   - Default values (description="", completed=False)

2. `tests/unit/test_repository.py`:
   - Create todo (auto-increment ID)
   - Get todo by ID (found and not found)
   - Get all todos (empty, single, multiple)
   - Update todo (title only, description only, both)
   - Update preserves completion status
   - Delete todo (success and not found)
   - Mark complete
   - ID uniqueness (1000+ creates)

3. `tests/unit/test_validators.py`:
   - Valid title validation
   - Invalid title validation (empty, whitespace)
   - Valid ID parsing
   - Invalid ID parsing (non-numeric, negative)

4. `tests/unit/test_display.py`:
   - Format empty list
   - Format single todo
   - Format multiple todos
   - Status indicators (✔ vs ✘)
   - Error message formatting
   - Success message formatting

### Integration Tests

**Test File**: `tests/integration/test_cli_integration.py`

**End-to-End Scenarios** (matching User Stories):

1. **P1: Create and View Todos**:
   - Start application
   - Create 3 todos with different titles/descriptions
   - View list and verify all 3 appear
   - Verify status indicators (all ✘)
   - Verify IDs are sequential (1, 2, 3)

2. **P2: Mark Complete**:
   - Create 2 todos
   - Mark first as complete
   - View list and verify status (✔ for first, ✘ for second)

3. **P3: Update Todo**:
   - Create todo
   - Update title and description
   - Verify changes in list view
   - Verify completion status unchanged

4. **P3: Delete Todo**:
   - Create 5 todos
   - Delete todo ID 3
   - View list and verify only 4 remain
   - Verify ID 3 not present

5. **Edge Cases**:
   - Create with empty title (should fail)
   - Update with invalid ID (should show error)
   - Delete with invalid ID (should show error)
   - View when list is empty (should show friendly message)

**Test Approach**:
- Mock stdin/stdout for input/output capture
- Simulate user menu choices as input
- Verify output matches expected format
- Check repository state after operations

### Performance Tests

**Test Requirements** (SC-003, SC-006):

1. **ID Uniqueness Test**:
   - Create 1000 todos
   - Verify all IDs are unique
   - Verify IDs are sequential (1-1000)

2. **Large Dataset Test**:
   - Create 500 todos
   - Perform 100 random operations (create, read, update, delete)
   - Verify no performance degradation (< 5 seconds per operation)
   - Verify memory usage remains reasonable

3. **Startup/Shutdown Test**:
   - Measure application startup time (should be < 1 second)
   - Measure application shutdown time (should be < 1 second)

## Implementation Phases

### Phase 0: Project Setup
**Goal**: Initialize project structure and documentation

**Tasks**:
1. Create directory structure (`src/`, `tests/`, `specs/`)
2. Create empty module files (`__init__.py`)
3. Write README.md with project overview
4. Create empty `requirements.txt` (no dependencies)
5. Verify Python 3.13+ installation

**Deliverable**: Empty project structure ready for implementation

---

### Phase 1: Domain Model Implementation
**Goal**: Implement Todo entity with validation

**Tasks**:
1. Create `src/models/todo.py` with dataclass
2. Implement `__post_init__` for title validation
3. Implement `update()` method (returns new instance)
4. Implement `mark_complete()` method (returns new instance)
5. Write unit tests (`tests/unit/test_todo_model.py`)
6. Run tests and verify all pass

**Acceptance Criteria**:
- Todo creation succeeds with valid title
- Todo creation fails with empty/whitespace title
- Todo instances are immutable (frozen dataclass)
- Default values set correctly (description="", completed=False)
- All unit tests pass

**Deliverable**: Fully tested Todo entity

---

### Phase 2: Repository Implementation
**Goal**: Implement in-memory CRUD operations

**Tasks**:
1. Create `src/repository/todo_repository.py`
2. Implement `__init__` (initialize storage and ID counter)
3. Implement `create()` method
4. Implement `get_by_id()` method
5. Implement `get_all()` method (sorted by ID)
6. Implement `update()` method
7. Implement `delete()` method
8. Implement `mark_complete()` method
9. Implement `exists()` helper method
10. Write unit tests (`tests/unit/test_repository.py`)
11. Write performance tests (ID uniqueness, large dataset)
12. Run tests and verify all pass

**Acceptance Criteria**:
- All CRUD operations work correctly
- IDs are auto-incremented and unique
- Repository handles not-found cases gracefully
- Update preserves completion status
- 1000+ creates maintain ID uniqueness
- All unit tests pass

**Deliverable**: Fully tested repository layer

---

### Phase 3: Validation Layer Implementation
**Goal**: Centralize input validation logic

**Tasks**:
1. Create `src/validation/validators.py`
2. Implement `validate_title()` function
3. Implement `validate_id()` function
4. Implement `validate_description()` function
5. Write unit tests (`tests/unit/test_validators.py`)
6. Run tests and verify all pass

**Acceptance Criteria**:
- Title validation matches domain model rules
- ID validation parses and validates numeric input
- Functions return consistent tuple format
- No exceptions raised (errors in return values)
- All unit tests pass

**Deliverable**: Fully tested validation layer

---

### Phase 4: Display Formatter Implementation
**Goal**: Implement output formatting logic

**Tasks**:
1. Create `src/cli/display.py`
2. Implement `format_todo_list()` function
3. Implement `format_single_todo()` function
4. Implement `format_error()` function
5. Implement `format_success()` function
6. Implement helper functions (status icon, padding)
7. Write unit tests (`tests/unit/test_display.py`)
8. Run tests and verify all pass

**Acceptance Criteria**:
- List formatting shows ID, status, title in table format
- Status icons display correctly (✔ vs ✘)
- Empty list shows friendly message
- Error messages formatted consistently
- All unit tests pass

**Deliverable**: Fully tested display formatter

---

### Phase 5: CLI Commands Implementation
**Goal**: Implement command handlers for all operations

**Tasks**:
1. Create `src/cli/commands.py`
2. Implement `handle_create()` command
3. Implement `handle_list()` command
4. Implement `handle_update()` command
5. Implement `handle_delete()` command
6. Implement `handle_complete()` command
7. Add input validation to all commands
8. Add error handling to all commands
9. Add success confirmations to all commands
10. Write unit tests for each command handler
11. Run tests and verify all pass

**Acceptance Criteria**:
- All commands handle valid input correctly
- All commands validate input (empty titles, invalid IDs)
- All commands handle repository errors gracefully
- All commands display appropriate messages
- All commands use display formatter consistently
- All unit tests pass

**Deliverable**: Fully tested command handlers

---

### Phase 6: Menu System Implementation
**Goal**: Implement main menu loop and user interaction

**Tasks**:
1. Create `src/cli/menu.py`
2. Implement `TodoMenu` class with `run()` method
3. Implement menu display logic
4. Implement choice validation (1-6)
5. Implement command dispatch (route choice to handler)
6. Implement exit logic
7. Add error handling for unexpected input
8. Test menu navigation manually

**Acceptance Criteria**:
- Menu displays all options clearly
- Choice validation accepts 1-6, rejects others
- Commands execute correctly based on choice
- Exit option terminates application
- Invalid input shows error and re-displays menu
- Manual testing confirms all flows work

**Deliverable**: Functional menu system

---

### Phase 7: Entry Point Implementation
**Goal**: Create application entry point

**Tasks**:
1. Create `src/main.py`
2. Implement `main()` function
3. Initialize repository
4. Initialize menu with repository
5. Add welcome message
6. Add error handling (KeyboardInterrupt, exceptions)
7. Add goodbye message
8. Test application end-to-end manually

**Acceptance Criteria**:
- Application starts with welcome message
- Repository initialized correctly
- Menu system runs
- Ctrl+C exits gracefully
- Exceptions caught and displayed
- Application exits with appropriate message
- Manual testing confirms all user stories work

**Deliverable**: Complete working application

---

### Phase 8: Integration Testing
**Goal**: Verify end-to-end scenarios work correctly

**Tasks**:
1. Create `tests/integration/test_cli_integration.py`
2. Write integration test for P1 (Create and View)
3. Write integration test for P2 (Mark Complete)
4. Write integration test for P3 (Update)
5. Write integration test for P3 (Delete)
6. Write integration tests for edge cases
7. Mock stdin/stdout for input/output capture
8. Run integration tests and verify all pass

**Acceptance Criteria**:
- All user stories pass integration tests
- Edge cases handled correctly
- Input/output captured and verified
- All integration tests pass

**Deliverable**: Fully tested application with integration coverage

---

### Phase 9: Documentation and Final Validation
**Goal**: Complete documentation and verify all requirements

**Tasks**:
1. Update README.md with usage instructions
2. Add code comments and docstrings where needed
3. Create quickstart.md guide
4. Run all tests (unit + integration)
5. Manual testing of all user stories
6. Verify constitutional compliance
7. Verify all functional requirements (FR-001 to FR-018)
8. Verify all success criteria (SC-001 to SC-010)
9. Performance testing (startup time, large datasets)

**Acceptance Criteria**:
- All tests pass (unit + integration)
- All user stories work correctly
- All functional requirements satisfied
- All success criteria met
- Constitution compliance verified
- Documentation complete
- Code quality meets standards (type hints, docstrings)

**Deliverable**: Production-ready application with complete documentation

---

## Risk Analysis and Mitigation

### Risk 1: ID Collision with Large Datasets
**Impact**: High - would violate FR-015 (unique IDs)
**Likelihood**: Low - simple counter is reliable
**Mitigation**:
- Performance test with 1000+ creates to verify uniqueness
- Use Python's built-in integer (no overflow in Python 3)
- Document ID counter approach in code

### Risk 2: Memory Usage with Large Todo Lists
**Impact**: Medium - could affect SC-006 (500+ todos without degradation)
**Likelihood**: Low - in-memory storage is efficient for this scale
**Mitigation**:
- Performance test with 500 todos
- Monitor memory usage during testing
- Document reasonable limits in README

### Risk 3: User Input Validation Edge Cases
**Impact**: Medium - could violate SC-005 (100% invalid operations caught)
**Likelihood**: Medium - many edge cases to consider
**Mitigation**:
- Comprehensive validation tests (empty, whitespace, non-numeric, special chars)
- Centralized validation layer ensures consistency
- Integration tests cover all error paths

### Risk 4: CLI Display Formatting Issues
**Impact**: Low - affects SC-008 (consistent formatting) but not functionality
**Likelihood**: Medium - terminal differences across platforms
**Mitigation**:
- Use ASCII characters for broad compatibility (✔ ✘)
- Test on Windows, Linux, macOS terminals
- Fallback to text indicators if symbols don't render

### Risk 5: Python Version Incompatibility
**Impact**: High - constitutional requirement (Python 3.13+)
**Likelihood**: Low - using standard library features only
**Mitigation**:
- Document Python 3.13+ requirement clearly
- Use type hints compatible with 3.13+
- Test on Python 3.13 specifically

## Definition of Done

This feature is complete when:

- [ ] All 9 implementation phases completed
- [ ] All functional requirements (FR-001 to FR-018) satisfied
- [ ] All success criteria (SC-001 to SC-010) met
- [ ] All unit tests pass (100% of testable functions covered)
- [ ] All integration tests pass (all user stories verified)
- [ ] Performance tests pass (1000+ operations, 500+ todos)
- [ ] Constitution compliance verified (all 6 principles)
- [ ] Code quality standards met (type hints, docstrings, naming)
- [ ] Documentation complete (README, quickstart, code comments)
- [ ] Manual testing completed on target platforms
- [ ] No persistence mechanisms present (verified)
- [ ] Application startup/shutdown < 1 second (verified)

## Next Steps

1. **Review this plan** with stakeholders for approval
2. **Run `/sp.tasks`** to generate detailed implementation tasks from this plan
3. **Begin Phase 0** (Project Setup) after plan approval
4. **Follow Red-Green-Refactor** TDD cycle as per constitution
5. **Create ADRs** for any significant architectural decisions made during implementation (if needed)

---

**Plan Status**: Draft - Ready for Review
**Estimated Complexity**: Low-Medium (straightforward implementation, well-defined requirements)
**Estimated Timeline**: 9 phases (can be completed incrementally)
