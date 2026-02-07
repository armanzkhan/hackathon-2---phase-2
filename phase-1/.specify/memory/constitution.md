# Todo In-Memory Console Application – Phase I Constitution

## Mission
Design and implement a Python-based command-line Todo application using strict Spec-Driven Development.

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All source code must be generated exclusively from approved specifications. Manual coding, refactoring, or logic injection is strictly prohibited. Each feature must correspond to an explicit specification file under `specs/<feature>/`.

### II. In-Memory Only Storage
The application must store all data in runtime memory only. No file-based persistence, databases, web frameworks, background services, or external storage systems are permitted.

### III. Python 3.13+ Requirement
Python version must be 3.13 or higher. All code must be compatible with modern Python features and type hints.

### IV. CLI-First Interface
The system must be runnable via a CLI entry point. All interactions happen through command-line interface with human-readable output. Clear commands and deterministic behavior are mandatory.

### V. Modular Architecture
Strict separation of concerns is required:
- **CLI Layer**: Command parsing and user interaction
- **Domain Model**: Business logic and Todo entities
- **Data Handling**: In-memory storage management

Each module must follow the Single Responsibility Principle.

### VI. Clean Code Standards
- Human-readable CLI output
- Deterministic and predictable behavior
- Clear naming conventions
- Comprehensive inline documentation
- Type hints for all function signatures

## Technology Stack

### Required
- Python 3.13+
- Standard library only (no external dependencies initially)
- CLI-based interface

### Explicitly Forbidden
- File-based persistence (no .json, .txt, .db files)
- Database systems (SQLite, PostgreSQL, etc.)
- Web frameworks (Flask, FastAPI, Django)
- Background services or daemons
- AI or LLM integrations
- External API calls for core functionality

## Development Workflow

### Specification Process
1. Feature requirements captured in `specs/<feature>/spec.md`
2. Architecture decisions documented in `specs/<feature>/plan.md`
3. Implementation tasks defined in `specs/<feature>/tasks.md`
4. All artifacts approved before implementation begins

### Implementation Process
1. **Red Phase**: Write failing tests based on tasks
2. **Green Phase**: Implement minimal code to pass tests
3. **Refactor Phase**: Clean up while keeping tests green
4. All phases must be approved and documented

### Quality Gates
- No code without corresponding spec
- No implementation without failing tests first
- All tests must pass before feature is considered complete
- Code review against constitution compliance

## Governance

This constitution supersedes all other practices and conventions. Any amendments require:
1. Documented rationale for the change
2. User approval before implementation
3. Migration plan for existing code if applicable

All development activities, code reviews, and PRs must verify compliance with these principles. Violations should be flagged immediately and corrected before proceeding.

**Version**: 1.0.0 | **Ratified**: 2026-02-07 | **Last Amended**: 2026-02-07
