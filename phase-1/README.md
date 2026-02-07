# Todo In-Memory Console Application

A Python 3.13+ command-line todo management application with full CRUD operations stored entirely in runtime memory.

## Features

- ✅ Create todos with title and optional description
- ✅ View all todos in formatted list
- ✅ Mark todos as complete (✔) or incomplete (✘)
- ✅ Update todo details
- ✅ Delete todos
- ✅ In-memory storage only (no persistence)
- ✅ Human-readable CLI interface

## Requirements

- Python 3.13 or higher
- No external dependencies (standard library only)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd phase-1

# Verify Python version
python --version  # Should be 3.13+
```

## Usage

```bash
# Run the application
python src/main.py
```

### Menu Options

1. **Create a new todo** - Add a todo with title and optional description
2. **View all todos** - Display all todos with ID, status, and title
3. **Update a todo** - Modify title and description of existing todo
4. **Delete a todo** - Remove a todo by ID
5. **Mark todo as complete** - Change status to completed (✔)
6. **Exit** - Quit the application

### Example Session

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

Enter your choice (1-6): 1
Enter title: Buy groceries
Enter description (optional): Milk, eggs, bread
✔ Todo created with ID 1

Enter your choice (1-6): 2
=== Your Todos ===
ID | Status | Title
----|--------|-------------------
1   | ✘      | Buy groceries
```

## Development

### Project Structure

```
phase-1/
├── src/
│   ├── models/          # Domain entities
│   ├── repository/      # In-memory CRUD operations
│   ├── cli/             # User interface
│   ├── validation/      # Input validation
│   └── main.py          # Application entry point
├── tests/
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── specs/               # Specifications and documentation
└── README.md
```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test file
python -m unittest tests/unit/test_todo_model.py

# Run with coverage (if coverage installed)
coverage run -m unittest discover tests
coverage report
```

## Architecture

**Three-Layer Design**:

1. **Domain Model** (`src/models/`): Todo entity with validation
2. **Repository** (`src/repository/`): In-memory storage and CRUD operations
3. **CLI Interface** (`src/cli/`): User interaction and display formatting

**Key Principles**:
- Spec-Driven Development
- In-memory only (no persistence)
- Test-Driven Development (TDD)
- Immutable domain entities
- Clear separation of concerns

## Constitution Compliance

This project strictly adheres to the constitution:

- ✅ **Spec-Driven Development**: All code from approved specifications
- ✅ **In-Memory Only**: No file I/O, databases, or external storage
- ✅ **Python 3.13+**: Modern Python with type hints
- ✅ **CLI-First**: Command-line interface only
- ✅ **Modular Architecture**: Clean separation of layers
- ✅ **Clean Code**: Type hints, docstrings, clear naming

## Technical Details

- **Language**: Python 3.13+
- **Dependencies**: Standard library only
- **Storage**: Dictionary (dict) for O(1) lookups
- **ID Generation**: Simple counter (1, 2, 3...)
- **Testing**: unittest framework
- **Performance**: < 5 seconds per operation, 500+ todos supported

## Limitations

- Data is ephemeral (lost on exit)
- Single-user application
- No persistence or data export
- No search or filtering
- No due dates or priorities
- English language only

## License

[Your License Here]

## Contributing

Please read the constitution and specifications before contributing:
- `specs/001-todo-crud/spec.md` - Requirements
- `specs/001-todo-crud/plan.md` - Architecture
- `specs/001-todo-crud/tasks.md` - Implementation tasks
- `.specify/memory/constitution.md` - Project principles
