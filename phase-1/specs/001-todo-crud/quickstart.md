# Quickstart Guide: Todo In-Memory Console Application

**Feature**: 001-todo-crud | **Date**: 2026-02-07

## Overview

This guide provides quick setup and development instructions for the Todo In-Memory Console Application. Follow these steps to understand, build, and test the application.

## Prerequisites

### Required

- **Python 3.13+**: Download from [python.org](https://www.python.org/downloads/)
- **Git**: For version control and branch management
- **Terminal/Command Line**: Basic command-line proficiency

### Verify Installation

```bash
# Check Python version (must be 3.13+)
python --version  # or python3 --version

# Check Git
git --version
```

## Project Structure

```
phase-1/
├── src/
│   ├── models/
│   │   └── todo.py              # Todo entity (dataclass)
│   ├── repository/
│   │   └── todo_repository.py   # In-memory CRUD operations
│   ├── cli/
│   │   ├── menu.py              # Main menu loop
│   │   ├── commands.py          # Command handlers
│   │   └── display.py           # Output formatting
│   ├── validation/
│   │   └── validators.py        # Input validation
│   └── main.py                  # Application entry point
├── tests/
│   ├── unit/                    # Unit tests for each module
│   └── integration/             # End-to-end CLI tests
├── specs/
│   └── 001-todo-crud/           # Feature specifications
│       ├── spec.md              # Requirements
│       ├── plan.md              # Implementation plan
│       ├── data-model.md        # Data structures
│       ├── contracts/           # Interface contracts
│       └── quickstart.md        # This file
└── README.md                    # Project overview
```

## Quick Start (Development)

### Step 1: Clone and Setup

```bash
# Navigate to project directory
cd phase-1

# Verify you're on the right branch
git branch --show-current
# Should show: 001-todo-crud

# No dependencies to install (standard library only)
```

### Step 2: Understand the Architecture

**Three-Layer Design**:

1. **Domain Model** (`src/models/`):
   - Todo entity (immutable dataclass)
   - Business logic and validation

2. **Repository** (`src/repository/`):
   - In-memory storage (dict)
   - CRUD operations
   - ID generation

3. **CLI Interface** (`src/cli/`):
   - User interaction (menu, commands)
   - Input validation and display formatting

**Data Flow**:
```
User Input → CLI Commands → Validation → Repository → Domain Model
                ↓                                         ↓
           Display ← Format ← Result ← Operation ← Storage
```

### Step 3: Read Key Documents

**Required Reading** (in order):

1. [spec.md](./spec.md) - Requirements and user stories
2. [plan.md](./plan.md) - Implementation plan and architecture
3. [data-model.md](./data-model.md) - Data structures and storage
4. [contracts/repository-contract.md](./contracts/repository-contract.md) - Repository interface
5. [contracts/validation-contract.md](./contracts/validation-contract.md) - Validation rules

### Step 4: Implementation Workflow

Follow the TDD (Test-Driven Development) cycle as per constitution:

**Red-Green-Refactor**:

1. **Red**: Write failing test
2. **Green**: Implement minimal code to pass
3. **Refactor**: Clean up while tests stay green

**Implementation Order** (per plan.md):

1. Domain Model (Todo entity)
2. Repository (CRUD operations)
3. Validation Layer
4. Display Formatter
5. CLI Commands
6. Menu System
7. Entry Point
8. Integration Tests

## Running Tests

### Unit Tests

```bash
# Run all unit tests
python -m unittest discover tests/unit

# Run specific test file
python -m unittest tests/unit/test_todo_model.py

# Run with verbose output
python -m unittest discover tests/unit -v
```

### Integration Tests

```bash
# Run integration tests
python -m unittest tests/integration/test_cli_integration.py -v
```

### All Tests

```bash
# Run everything
python -m unittest discover tests -v
```

### Test Coverage (Optional)

```bash
# Install coverage tool (dev dependency)
pip install coverage

# Run tests with coverage
coverage run -m unittest discover tests

# View coverage report
coverage report

# Generate HTML report
coverage html
# Open htmlcov/index.html in browser
```

## Running the Application

### Development Run

```bash
# From project root
python src/main.py
```

### Expected Output

```
Welcome to Todo Manager!
All data is stored in memory and will be lost on exit.

=== Todo Manager ===
1. Create a new todo
2. View all todos
3. Update a todo
4. Delete a todo
5. Mark todo as complete
6. Exit

Enter your choice (1-6): _
```

### Sample Session

```
Enter your choice (1-6): 1
Enter title: Buy groceries
Enter description (optional): Milk, eggs, bread
✔ Todo created with ID 1

Enter your choice (1-6): 1
Enter title: Call dentist
Enter description (optional):
✔ Todo created with ID 2

Enter your choice (1-6): 2
=== Your Todos ===
ID | Status | Title
----|--------|-------------------
1   | ✘      | Buy groceries
2   | ✘      | Call dentist

Enter your choice (1-6): 5
Enter todo ID: 1
✔ Todo 1 marked as complete

Enter your choice (1-6): 2
=== Your Todos ===
ID | Status | Title
----|--------|-------------------
1   | ✔      | Buy groceries
2   | ✘      | Call dentist

Enter your choice (1-6): 6
Goodbye!
```

## Development Commands

### Code Formatting (Optional)

```bash
# Install black formatter (dev dependency)
pip install black

# Format code
black src/ tests/

# Check formatting without changes
black --check src/ tests/
```

### Type Checking (Optional)

```bash
# Install mypy (dev dependency)
pip install mypy

# Run type checker
mypy src/

# Strict mode
mypy --strict src/
```

### Linting (Optional)

```bash
# Install pylint (dev dependency)
pip install pylint

# Lint code
pylint src/

# Check specific file
pylint src/models/todo.py
```

## Common Tasks

### Task 1: Add a New Feature

1. Read spec.md to understand requirements
2. Update plan.md with design approach
3. Write failing tests (RED)
4. Implement minimal code (GREEN)
5. Refactor for quality (REFACTOR)
6. Update documentation

### Task 2: Fix a Bug

1. Write test that reproduces bug
2. Verify test fails (confirms bug)
3. Fix the code
4. Verify test passes
5. Run all tests (ensure no regressions)

### Task 3: Refactor Code

1. Ensure all tests pass before starting
2. Make refactoring changes
3. Run tests after each small change
4. Keep tests green throughout
5. Commit when complete

### Task 4: Review Constitution Compliance

```bash
# Checklist:
- [ ] No file I/O (no open(), read(), write())
- [ ] No database connections
- [ ] No web frameworks imported
- [ ] Python 3.13+ features only
- [ ] All functions have type hints
- [ ] All code has docstrings
- [ ] CLI-only interface (no GUI)
```

## Troubleshooting

### Problem: Python version too old

```bash
# Check version
python --version

# Solution: Install Python 3.13+
# Download from python.org
```

### Problem: Module not found errors

```bash
# Ensure you're in project root
pwd  # Should show path/to/phase-1

# Run from root directory
python src/main.py

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Problem: Tests failing

```bash
# Run tests with verbose output
python -m unittest discover tests -v

# Check which tests fail
# Read error messages carefully
# Verify implementation matches spec
```

### Problem: Import errors in tests

```bash
# Tests should import from src
# Example:
from src.models.todo import Todo
from src.repository.todo_repository import TodoRepository

# Not:
from models.todo import Todo  # Wrong
```

## Best Practices

### 1. Follow TDD

- Write tests before implementation
- Keep tests small and focused
- One assertion per test (when possible)
- Test behavior, not implementation

### 2. Keep It Simple

- No premature optimization
- Smallest viable change
- Refactor only when tests are green
- YAGNI (You Aren't Gonna Need It)

### 3. Constitution Compliance

- Always check against constitution
- No persistence (in-memory only)
- Standard library only
- Type hints everywhere
- CLI-first interface

### 4. Code Quality

- Clear naming (functions, variables, classes)
- Comprehensive docstrings
- Type hints for all signatures
- Comments for complex logic only
- Consistent formatting

### 5. Git Workflow

```bash
# Work on feature branch
git status

# Commit often with clear messages
git add <files>
git commit -m "Implement Todo entity with validation"

# Push to remote
git push origin 001-todo-crud
```

## Performance Tips

### Memory Usage

- Dict storage is O(1) for lookups
- Immutable Todos prevent accidental mutation
- Python garbage collector handles cleanup
- No memory leaks (no circular references)

### Startup Time

- No file I/O on startup (< 1 second)
- No database connections
- Minimal initialization (empty repository)

### Operation Speed

- All operations are in-memory (fast)
- No network calls
- No disk I/O
- Deterministic performance

## Next Steps

### After Initial Implementation

1. **Run All Tests**: Verify 100% pass
2. **Manual Testing**: Try all user stories
3. **Performance Testing**: Create 500+ todos
4. **Constitution Review**: Verify compliance
5. **Documentation**: Update README

### Before Submitting

- [ ] All tests pass
- [ ] All user stories work
- [ ] Constitution compliance verified
- [ ] Code quality standards met
- [ ] Documentation complete
- [ ] No TODO/FIXME comments
- [ ] Clean git history

## Resources

### Documentation

- [Specification](./spec.md) - Requirements and user stories
- [Implementation Plan](./plan.md) - Architecture and phases
- [Data Model](./data-model.md) - Data structures
- [Repository Contract](./contracts/repository-contract.md) - Interface spec
- [Validation Contract](./contracts/validation-contract.md) - Validation rules

### Constitution

- [Project Constitution](../../.specify/memory/constitution.md) - Core principles
- Must follow Spec-Driven Development
- In-memory only (no persistence)
- Python 3.13+ required
- CLI-first interface
- Modular architecture

### Python Resources

- [Python 3.13 Docs](https://docs.python.org/3.13/)
- [dataclasses](https://docs.python.org/3/library/dataclasses.html) - For Todo entity
- [unittest](https://docs.python.org/3/library/unittest.html) - Testing framework
- [Type Hints](https://docs.python.org/3/library/typing.html) - Type annotations

## Support

### Getting Help

1. Read the spec.md and plan.md thoroughly
2. Check contracts/ for interface definitions
3. Review existing code and tests
4. Consult constitution for project rules

### Common Questions

**Q: Can I use external libraries?**
A: No. Constitution requires standard library only.

**Q: Can I add file persistence?**
A: No. Constitution forbids all persistence (files, databases, etc.).

**Q: Can I skip tests?**
A: No. Constitution requires TDD (tests first, then code).

**Q: Can I use Python 3.12?**
A: No. Constitution requires Python 3.13+.

**Q: Can I add a web interface?**
A: No. Constitution requires CLI-only interface.

## Summary

**Quick Steps**:
1. ✅ Verify Python 3.13+ installed
2. ✅ Read spec.md (requirements)
3. ✅ Read plan.md (architecture)
4. ✅ Follow TDD cycle (Red-Green-Refactor)
5. ✅ Run tests frequently
6. ✅ Check constitution compliance
7. ✅ Document as you go

**Remember**:
- Tests first, then code
- In-memory only (no persistence)
- Standard library only
- Type hints everywhere
- Constitution is law

**Have fun building! 🚀**
