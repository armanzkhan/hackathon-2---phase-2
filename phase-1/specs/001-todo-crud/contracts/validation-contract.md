# Validation Contract: Input Validation Rules

**Feature**: 001-todo-crud | **Date**: 2026-02-07

## Purpose

This contract defines the validation rules and interface for all user input validation in the Todo application. Centralized validation ensures consistency across CLI commands and tests.

## Interface Definition

```python
def validate_title(title: str) -> tuple[bool, str]:
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
        (True, "")

        >>> validate_title("")
        (False, "Title cannot be empty")

        >>> validate_title("   ")
        (False, "Title cannot be empty")

        >>> validate_title("  Valid Title  ")
        (True, "")
    """

def validate_id(id_str: str) -> tuple[bool, int, str]:
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
        (True, 1, "")

        >>> validate_id("42")
        (True, 42, "")

        >>> validate_id("abc")
        (False, 0, "Invalid ID format. Please enter a number.")

        >>> validate_id("-5")
        (False, 0, "ID must be positive")

        >>> validate_id("0")
        (False, 0, "ID must be positive")

        >>> validate_id("  123  ")
        (True, 123, "")
    """

def validate_description(description: str) -> tuple[bool, str]:
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
        (True, "")

        >>> validate_description("Any text")
        (True, "")

        >>> validate_description("Very long text" * 1000)
        (True, "")
    """
```

## Validation Rules

### Rule 1: Title Validation

**Requirement**: FR-003 (System MUST validate that todo titles are non-empty)

**Logic**:
1. Strip leading/trailing whitespace from input
2. Check if resulting string is empty
3. If empty, return (False, "Title cannot be empty")
4. Otherwise, return (True, "")

**Valid Examples**:
- "Buy groceries" → Valid
- "A" → Valid (single character OK)
- "  Task with spaces  " → Valid (stripped to "Task with spaces")
- "Title\nwith\nnewlines" → Valid (newlines allowed)
- "Special chars !@#$%^" → Valid (all chars allowed)

**Invalid Examples**:
- "" → Invalid (empty string)
- "   " → Invalid (whitespace-only)
- "\t" → Invalid (tab only)
- "\n\n" → Invalid (newlines only)
- "  \t  \n  " → Invalid (mixed whitespace)

**Error Message**: "Title cannot be empty"

### Rule 2: ID Validation

**Requirement**: FR-013 (System MUST provide clear error messages for invalid IDs)

**Logic**:
1. Strip leading/trailing whitespace from input
2. Try to parse as integer
3. If parse fails, return (False, 0, "Invalid ID format. Please enter a number.")
4. If integer <= 0, return (False, 0, "ID must be positive")
5. Otherwise, return (True, parsed_id, "")

**Valid Examples**:
- "1" → Valid (parsed to 1)
- "42" → Valid (parsed to 42)
- "999" → Valid (parsed to 999)
- "  123  " → Valid (stripped and parsed to 123)
- "007" → Valid (parsed to 7, leading zeros ignored)

**Invalid Examples**:
- "abc" → Invalid (not numeric)
- "1.5" → Invalid (float not allowed)
- "1,000" → Invalid (comma not allowed)
- "" → Invalid (empty string)
- "-5" → Invalid (negative not allowed)
- "0" → Invalid (zero not allowed)
- "1e10" → Invalid (scientific notation not allowed)

**Error Messages**:
- "Invalid ID format. Please enter a number." (non-numeric)
- "ID must be positive" (zero or negative)

### Rule 3: Description Validation

**Requirement**: None (descriptions have no restrictions)

**Logic**:
1. Always return (True, "")
2. No validation performed

**Valid Examples**:
- "" → Valid (empty OK)
- "Any text" → Valid
- "Very long text..." → Valid (no length limit)
- "Special chars !@#$%^&*()" → Valid
- "\n\t\r" → Valid (whitespace OK)

**Invalid Examples**:
- None (all inputs valid)

## Return Value Contract

### Tuple Format

All validation functions return tuples with consistent structure:

**For boolean result (title, description)**:
```python
(is_valid: bool, error_message: str)
```

**For parsed result (ID)**:
```python
(is_valid: bool, parsed_value: int, error_message: str)
```

### Error Message Convention

- Empty string ("") indicates success (no error)
- Non-empty string contains human-readable error message
- Error messages are complete sentences
- Error messages are actionable (tell user what's wrong)
- Error messages use consistent tone (friendly but firm)

**Examples**:
- ✅ Good: "Title cannot be empty"
- ✅ Good: "Invalid ID format. Please enter a number."
- ❌ Bad: "error" (not descriptive)
- ❌ Bad: "INVALID INPUT" (too aggressive)
- ❌ Bad: "id bad" (not grammatical)

## Error Handling Strategy

### No Exceptions

Validation functions **never raise exceptions**. This is intentional:

**Rationale**:
- Validation failures are expected, not exceptional
- Exceptions add complexity to caller code
- Tuple returns make error handling explicit
- Consistent return format simplifies testing

**Example**:
```python
# Instead of try/except
is_valid, error = validate_title(user_input)
if not is_valid:
    print(f"Error: {error}")
    return

# Not this:
try:
    validate_title(user_input)  # Raises exception
except ValidationError as e:
    print(f"Error: {e}")
    return
```

### Caller Responsibility

Callers must check the `is_valid` flag:

```python
# Correct usage
is_valid, error = validate_title(title)
if not is_valid:
    # Handle error
    display_error(error)
    return

# Incorrect (ignoring validation)
is_valid, error = validate_title(title)
# Proceed without checking is_valid ← BUG
```

## Usage Examples

### Example 1: Title Validation in CLI

```python
def handle_create(repository: TodoRepository):
    title = input("Enter title: ")

    # Validate title
    is_valid, error = validate_title(title)
    if not is_valid:
        print(f"✘ Error: {error}")
        return

    # Title is valid, proceed
    description = input("Enter description (optional): ")
    todo = repository.create(title, description)
    print(f"✔ Todo created with ID {todo.id}")
```

### Example 2: ID Validation in CLI

```python
def handle_delete(repository: TodoRepository):
    id_str = input("Enter todo ID: ")

    # Validate and parse ID
    is_valid, todo_id, error = validate_id(id_str)
    if not is_valid:
        print(f"✘ Error: {error}")
        return

    # ID is valid, check if exists
    if not repository.exists(todo_id):
        print(f"✘ Error: Todo with ID {todo_id} not found")
        return

    # Delete todo
    repository.delete(todo_id)
    print(f"✔ Todo {todo_id} deleted successfully")
```

### Example 3: Multiple Validations

```python
def handle_update(repository: TodoRepository):
    # Validate ID
    id_str = input("Enter todo ID: ")
    is_valid, todo_id, error = validate_id(id_str)
    if not is_valid:
        print(f"✘ Error: {error}")
        return

    # Check existence
    if not repository.exists(todo_id):
        print(f"✘ Error: Todo with ID {todo_id} not found")
        return

    # Get new title
    new_title = input("Enter new title (or press Enter to skip): ")
    if new_title:
        # Validate new title
        is_valid, error = validate_title(new_title)
        if not is_valid:
            print(f"✘ Error: {error}")
            return
    else:
        new_title = None  # No change

    # Get new description (no validation needed)
    new_description = input("Enter new description (or press Enter to skip): ")
    if not new_description:
        new_description = None  # No change

    # Update todo
    updated = repository.update(todo_id, new_title, new_description)
    print(f"✔ Todo {todo_id} updated successfully")
```

## Testing Requirements

### Unit Tests Required

1. **Title Validation**:
   - ✅ Valid title (normal text)
   - ✅ Valid title (single character)
   - ✅ Valid title (with leading/trailing spaces)
   - ✅ Valid title (with special characters)
   - ❌ Invalid title (empty string)
   - ❌ Invalid title (whitespace only)
   - ❌ Invalid title (tabs only)
   - ❌ Invalid title (newlines only)
   - ❌ Invalid title (mixed whitespace)

2. **ID Validation**:
   - ✅ Valid ID (positive integer)
   - ✅ Valid ID (large number)
   - ✅ Valid ID (with leading/trailing spaces)
   - ✅ Valid ID (with leading zeros)
   - ❌ Invalid ID (empty string)
   - ❌ Invalid ID (non-numeric)
   - ❌ Invalid ID (float)
   - ❌ Invalid ID (negative)
   - ❌ Invalid ID (zero)
   - ❌ Invalid ID (scientific notation)

3. **Description Validation**:
   - ✅ Valid description (any string)
   - ✅ Valid description (empty string)
   - ✅ Valid description (very long string)
   - ✅ Valid description (special characters)

4. **Return Format**:
   - ✅ Title validation returns (bool, str)
   - ✅ ID validation returns (bool, int, str)
   - ✅ Description validation returns (bool, str)
   - ✅ Error messages are non-empty on failure
   - ✅ Error messages are empty ("") on success

## Edge Cases

### Unicode and Special Characters

**Title**:
- Emoji in title → Valid (✅ "Buy groceries 🛒")
- Unicode characters → Valid (✅ "Café meeting")
- Mixed scripts → Valid (✅ "Task 任务 مهمة")

**ID**:
- Unicode digits → Invalid (❌ "①②③")
- Roman numerals → Invalid (❌ "VII")
- Spelled numbers → Invalid (❌ "seven")

### Whitespace Variations

**Title**:
- Tab characters → Strip and check (✅ "\tTask" becomes "Task")
- Newlines → Strip and check (✅ "Task\n" becomes "Task")
- Mixed whitespace → Strip and check (✅ " \t\nTask\n\t " becomes "Task")

**ID**:
- Leading spaces → Strip before parse (✅ "  42" becomes 42)
- Trailing spaces → Strip before parse (✅ "42  " becomes 42)
- Internal spaces → Invalid (❌ "4 2" cannot parse)

### Boundary Values

**ID**:
- Minimum valid → 1 (✅)
- Maximum valid → No limit (Python arbitrary precision integers)
- Zero → Invalid (❌)
- Negative → Invalid (❌)

**Title/Description**:
- Minimum length → 1 character after strip (title), 0 (description)
- Maximum length → No limit (memory constrained only)

## Contract Versioning

**Version**: 1.0.0
**Date**: 2026-02-07
**Status**: Draft

**Breaking Changes**:
- None (initial version)

**Non-Breaking Changes**:
- None (initial version)

## Related Contracts

- [Repository Contract](./repository-contract.md) - TodoRepository interface
- [Data Model](../data-model.md) - Todo entity specification

## Compliance

This contract must be satisfied by the validation functions in `src/validation/validators.py`. All unit tests in `tests/unit/test_validators.py` must verify contract compliance.
