# Tasks: Todo In-Memory Console Application

**Input**: Design documents from `/specs/001-todo-crud/`
**Prerequisites**: plan.md (complete), spec.md (complete), data-model.md (complete), contracts/ (complete)

**Tests**: Per constitution requirements, this project follows strict TDD (Test-Driven Development). All test tasks are included and MUST be completed in Red-Green-Refactor cycle.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (this project)
- All paths relative to `phase-1/` directory

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure per plan.md Phase 0

- [ ] T001 Create root directory structure (src/, tests/, specs/, history/)
- [ ] T002 Create module directories (src/models/, src/repository/, src/cli/, src/validation/)
- [ ] T003 [P] Create test directories (tests/unit/, tests/integration/)
- [ ] T004 [P] Create empty __init__.py files in src/ and src/cli/
- [ ] T005 [P] Create empty requirements.txt file (no external dependencies per constitution)
- [ ] T006 [P] Create README.md with project overview and usage instructions

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 [P] Implement Todo entity as frozen dataclass in src/models/todo.py
- [ ] T008 [P] Implement TodoRepository class with __init__ method in src/repository/todo_repository.py
- [ ] T009 [P] Implement validation functions in src/validation/validators.py (validate_title, validate_id, validate_description)
- [ ] T010 [P] Implement display formatter functions in src/cli/display.py (format_todo_list, format_single_todo, format_error, format_success)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Todos (Priority: P1) 🎯 MVP

**Goal**: Enable users to create todos and view them in a formatted list

**Independent Test**: Create several todos with different titles and descriptions, then list them to verify all are displayed correctly with proper formatting and status indicators

### Tests for User Story 1 (TDD - RED Phase)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T011 [P] [US1] Write test for Todo creation with valid title in tests/unit/test_todo_model.py
- [ ] T012 [P] [US1] Write test for Todo creation with empty title (should fail) in tests/unit/test_todo_model.py
- [ ] T013 [P] [US1] Write test for Todo creation with whitespace-only title (should fail) in tests/unit/test_todo_model.py
- [ ] T014 [P] [US1] Write test for Todo default values (description="", completed=False) in tests/unit/test_todo_model.py
- [ ] T015 [P] [US1] Write test for repository create() operation in tests/unit/test_repository.py
- [ ] T016 [P] [US1] Write test for repository get_all() with empty storage in tests/unit/test_repository.py
- [ ] T017 [P] [US1] Write test for repository get_all() with multiple todos in tests/unit/test_repository.py
- [ ] T018 [P] [US1] Write test for ID auto-increment (1, 2, 3...) in tests/unit/test_repository.py
- [ ] T019 [P] [US1] Write test for validate_title() with valid input in tests/unit/test_validators.py
- [ ] T020 [P] [US1] Write test for validate_title() with empty input in tests/unit/test_validators.py
- [ ] T021 [P] [US1] Write test for format_todo_list() with empty list in tests/unit/test_display.py
- [ ] T022 [P] [US1] Write test for format_todo_list() with multiple todos in tests/unit/test_display.py
- [ ] T023 [US1] Run all unit tests and verify they FAIL (RED phase complete)

### Implementation for User Story 1 (TDD - GREEN Phase)

- [ ] T024 [US1] Implement Todo.__post_init__ with title validation in src/models/todo.py
- [ ] T025 [US1] Implement TodoRepository.create() method in src/repository/todo_repository.py
- [ ] T026 [US1] Implement TodoRepository.get_all() method with sorting in src/repository/todo_repository.py
- [ ] T027 [US1] Implement validate_title() function in src/validation/validators.py
- [ ] T028 [US1] Implement format_todo_list() function in src/cli/display.py
- [ ] T029 [US1] Implement format_error() function in src/cli/display.py
- [ ] T030 [US1] Implement format_success() function in src/cli/display.py
- [ ] T031 [US1] Run all User Story 1 tests and verify they PASS (GREEN phase complete)

### CLI Integration for User Story 1

- [ ] T032 [US1] Implement handle_create() command in src/cli/commands.py
- [ ] T033 [US1] Implement handle_list() command in src/cli/commands.py
- [ ] T034 [US1] Write integration test for create-and-list workflow in tests/integration/test_cli_integration.py
- [ ] T035 [US1] Run integration tests and verify they PASS

### Refactoring for User Story 1 (TDD - REFACTOR Phase)

- [ ] T036 [US1] Add comprehensive docstrings to Todo entity in src/models/todo.py
- [ ] T037 [US1] Add comprehensive docstrings to repository methods in src/repository/todo_repository.py
- [ ] T038 [US1] Add type hints validation (run mypy if available)
- [ ] T039 [US1] Run ALL tests again to ensure refactoring didn't break anything

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can create and view todos through CLI commands.

---

## Phase 4: User Story 2 - Mark Todos as Complete (Priority: P2)

**Goal**: Enable users to mark todos as complete and distinguish completed from incomplete items

**Independent Test**: Create several incomplete todos, mark specific ones as complete, then verify the list shows correct completion status (✔ vs ✘) for each item

### Tests for User Story 2 (TDD - RED Phase)

- [ ] T040 [P] [US2] Write test for repository mark_complete() operation in tests/unit/test_repository.py
- [ ] T041 [P] [US2] Write test for mark_complete() with non-existent ID (should raise KeyError) in tests/unit/test_repository.py
- [ ] T042 [P] [US2] Write test for idempotent mark_complete() (marking twice) in tests/unit/test_repository.py
- [ ] T043 [P] [US2] Write test for completion status preservation in repository operations in tests/unit/test_repository.py
- [ ] T044 [P] [US2] Write test for format_todo_list() displaying ✔ and ✘ symbols in tests/unit/test_display.py
- [ ] T045 [P] [US2] Write test for validate_id() with valid numeric input in tests/unit/test_validators.py
- [ ] T046 [P] [US2] Write test for validate_id() with non-numeric input in tests/unit/test_validators.py
- [ ] T047 [P] [US2] Write test for validate_id() with negative/zero input in tests/unit/test_validators.py
- [ ] T048 [US2] Run all User Story 2 tests and verify they FAIL (RED phase complete)

### Implementation for User Story 2 (TDD - GREEN Phase)

- [ ] T049 [US2] Implement TodoRepository.mark_complete() method in src/repository/todo_repository.py
- [ ] T050 [US2] Implement TodoRepository.exists() helper method in src/repository/todo_repository.py
- [ ] T051 [US2] Implement validate_id() function in src/validation/validators.py
- [ ] T052 [US2] Update format_todo_list() to display ✔/✘ symbols in src/cli/display.py
- [ ] T053 [US2] Implement handle_complete() command in src/cli/commands.py
- [ ] T054 [US2] Run all User Story 2 tests and verify they PASS (GREEN phase complete)

### CLI Integration for User Story 2

- [ ] T055 [US2] Write integration test for create-mark-complete-list workflow in tests/integration/test_cli_integration.py
- [ ] T056 [US2] Write integration test for mark_complete with invalid ID in tests/integration/test_cli_integration.py
- [ ] T057 [US2] Run integration tests and verify they PASS

### Refactoring for User Story 2 (TDD - REFACTOR Phase)

- [ ] T058 [US2] Add comprehensive docstrings to mark_complete() method in src/repository/todo_repository.py
- [ ] T059 [US2] Add comprehensive docstrings to handle_complete() command in src/cli/commands.py
- [ ] T060 [US2] Run ALL tests (US1 + US2) to ensure no regressions

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can create, view, and mark todos as complete.

---

## Phase 5: User Story 3 - Update Todo Details (Priority: P3)

**Goal**: Enable users to update todo title and description while preserving completion status

**Independent Test**: Create a todo, update its title and description, then verify the changes are reflected in the list view while completion status remains unchanged

### Tests for User Story 3 (TDD - RED Phase)

- [ ] T061 [P] [US3] Write test for repository update() with title only in tests/unit/test_repository.py
- [ ] T062 [P] [US3] Write test for repository update() with description only in tests/unit/test_repository.py
- [ ] T063 [P] [US3] Write test for repository update() with both title and description in tests/unit/test_repository.py
- [ ] T064 [P] [US3] Write test for update() preserving completion status in tests/unit/test_repository.py
- [ ] T065 [P] [US3] Write test for update() with non-existent ID (should raise KeyError) in tests/unit/test_repository.py
- [ ] T066 [P] [US3] Write test for update() with empty title (should raise ValueError) in tests/unit/test_repository.py
- [ ] T067 [US3] Run all User Story 3 tests and verify they FAIL (RED phase complete)

### Implementation for User Story 3 (TDD - GREEN Phase)

- [ ] T068 [US3] Implement TodoRepository.update() method in src/repository/todo_repository.py
- [ ] T069 [US3] Implement handle_update() command in src/cli/commands.py
- [ ] T070 [US3] Run all User Story 3 tests and verify they PASS (GREEN phase complete)

### CLI Integration for User Story 3

- [ ] T071 [US3] Write integration test for create-update-verify workflow in tests/integration/test_cli_integration.py
- [ ] T072 [US3] Write integration test for update with invalid ID in tests/integration/test_cli_integration.py
- [ ] T073 [US3] Write integration test for update with empty title in tests/integration/test_cli_integration.py
- [ ] T074 [US3] Run integration tests and verify they PASS

### Refactoring for User Story 3 (TDD - REFACTOR Phase)

- [ ] T075 [US3] Add comprehensive docstrings to update() method in src/repository/todo_repository.py
- [ ] T076 [US3] Add comprehensive docstrings to handle_update() command in src/cli/commands.py
- [ ] T077 [US3] Run ALL tests (US1 + US2 + US3) to ensure no regressions

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently. Users can create, view, mark complete, and update todos.

---

## Phase 6: User Story 4 - Delete Todos (Priority: P3)

**Goal**: Enable users to delete todos they no longer need

**Independent Test**: Create several todos, delete specific ones by ID, then verify they no longer appear in the list view

### Tests for User Story 4 (TDD - RED Phase)

- [ ] T078 [P] [US4] Write test for repository delete() with existing ID in tests/unit/test_repository.py
- [ ] T079 [P] [US4] Write test for repository delete() with non-existent ID (returns False) in tests/unit/test_repository.py
- [ ] T080 [P] [US4] Write test for idempotent delete() (deleting twice) in tests/unit/test_repository.py
- [ ] T081 [P] [US4] Write test for ID not reused after deletion in tests/unit/test_repository.py
- [ ] T082 [US4] Run all User Story 4 tests and verify they FAIL (RED phase complete)

### Implementation for User Story 4 (TDD - GREEN Phase)

- [ ] T083 [US4] Implement TodoRepository.delete() method in src/repository/todo_repository.py
- [ ] T084 [US4] Implement handle_delete() command in src/cli/commands.py
- [ ] T085 [US4] Run all User Story 4 tests and verify they PASS (GREEN phase complete)

### CLI Integration for User Story 4

- [ ] T086 [US4] Write integration test for create-delete-verify workflow in tests/integration/test_cli_integration.py
- [ ] T087 [US4] Write integration test for delete with invalid ID in tests/integration/test_cli_integration.py
- [ ] T088 [US4] Write integration test for ID not reused after deletion in tests/integration/test_cli_integration.py
- [ ] T089 [US4] Run integration tests and verify they PASS

### Refactoring for User Story 4 (TDD - REFACTOR Phase)

- [ ] T090 [US4] Add comprehensive docstrings to delete() method in src/repository/todo_repository.py
- [ ] T091 [US4] Add comprehensive docstrings to handle_delete() command in src/cli/commands.py
- [ ] T092 [US4] Run ALL tests (US1 + US2 + US3 + US4) to ensure no regressions

**Checkpoint**: All user stories should now be independently functional. All CRUD operations are complete.

---

## Phase 7: Menu System and Application Entry Point

**Purpose**: Integrate all commands into menu-driven interface and create application entry point

- [ ] T093 Implement TodoMenu class with run() method in src/cli/menu.py
- [ ] T094 Implement menu display and choice validation in src/cli/menu.py
- [ ] T095 Implement command dispatch logic (route choice to handlers) in src/cli/menu.py
- [ ] T096 Implement exit logic in src/cli/menu.py
- [ ] T097 Implement main() function in src/main.py
- [ ] T098 Add welcome and goodbye messages in src/main.py
- [ ] T099 Add error handling (KeyboardInterrupt, unexpected exceptions) in src/main.py
- [ ] T100 Write manual test for complete menu navigation workflow
- [ ] T101 Test application startup time (< 1 second per constitution)
- [ ] T102 Test application shutdown time (< 1 second per constitution)

**Checkpoint**: Complete working application with menu system

---

## Phase 8: Performance and Edge Case Testing

**Purpose**: Verify performance requirements and edge case handling per spec success criteria

- [ ] T103 [P] Write performance test for 1000+ creates (ID uniqueness) in tests/unit/test_repository.py
- [ ] T104 [P] Write performance test for 500+ todos (no degradation) in tests/unit/test_repository.py
- [ ] T105 [P] Write edge case test for whitespace-only title in tests/unit/test_validators.py
- [ ] T106 [P] Write edge case test for very long description (thousands of chars) in tests/unit/test_todo_model.py
- [ ] T107 [P] Write edge case test for large ID values in tests/unit/test_repository.py
- [ ] T108 [P] Write test for get_by_id() with non-existent ID (returns None) in tests/unit/test_repository.py
- [ ] T109 Run all performance and edge case tests and verify they PASS

**Checkpoint**: All performance criteria met, all edge cases handled

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

### Documentation

- [ ] T110 [P] Update README.md with complete usage instructions
- [ ] T111 [P] Verify all docstrings are complete and accurate across all modules
- [ ] T112 [P] Verify all type hints are present and correct across all modules

### Constitution Compliance Verification

- [ ] T113 Verify no file I/O operations exist (grep for open, read, write, file operations)
- [ ] T114 Verify no database imports (grep for sqlite, psycopg, pymongo, etc.)
- [ ] T115 Verify no web framework imports (grep for flask, fastapi, django, etc.)
- [ ] T116 Verify no external dependencies in requirements.txt
- [ ] T117 Verify Python 3.13+ compatibility (check type hints, features used)
- [ ] T118 Verify all functions have type hints
- [ ] T119 Verify CLI-only interface (no GUI imports)

### Functional Requirements Verification

- [ ] T120 Verify FR-001: Create todo with title and optional description
- [ ] T121 Verify FR-002: Auto-generated unique IDs
- [ ] T122 Verify FR-003: Title validation (non-empty)
- [ ] T123 Verify FR-004: New todos default to completed=False
- [ ] T124 Verify FR-005: In-memory only storage
- [ ] T125 Verify FR-006: View all todos with ID, title, status
- [ ] T126 Verify FR-007: Visual indicators (✔ and ✘)
- [ ] T127 Verify FR-008: Friendly message when no todos exist
- [ ] T128 Verify FR-009: Update todo by ID
- [ ] T129 Verify FR-010: Update preserves completion status
- [ ] T130 Verify FR-011: Mark todo as complete
- [ ] T131 Verify FR-012: Delete todo by ID
- [ ] T132 Verify FR-013: Clear error messages for invalid IDs
- [ ] T133 Verify FR-014: Validation error messages for empty titles
- [ ] T134 Verify FR-015: ID uniqueness throughout runtime
- [ ] T135 Verify FR-016: CLI interface for all operations
- [ ] T136 Verify FR-017: Human-readable output
- [ ] T137 Verify FR-018: Success confirmations for operations

### Success Criteria Verification

- [ ] T138 Verify SC-001: Create todo confirmation in < 5 seconds
- [ ] T139 Verify SC-002: View list in < 3 seconds
- [ ] T140 Verify SC-003: Data integrity with 1000+ operations
- [ ] T141 Verify SC-004: Error messages are clear and actionable
- [ ] T142 Verify SC-005: 100% invalid operations caught
- [ ] T143 Verify SC-006: No degradation with 500+ todos
- [ ] T144 Verify SC-007: All CRUD operations work through CLI
- [ ] T145 Verify SC-008: List formatting is consistent and scannable
- [ ] T146 Verify SC-009: Startup/shutdown < 1 second
- [ ] T147 Verify SC-010: Deterministic behavior (same inputs → same outputs)

### Final Testing

- [ ] T148 Run complete test suite (all unit + integration tests)
- [ ] T149 Verify 100% test pass rate
- [ ] T150 Manual end-to-end testing of all user stories
- [ ] T151 Verify quickstart.md instructions are accurate and complete

**Checkpoint**: Production-ready application with complete verification

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories CAN proceed in parallel (if staffed) after Phase 2
  - Or sequentially in priority order (P1 → P2 → P3)
- **Menu System (Phase 7)**: Depends on all user story CLI commands being complete
- **Performance Testing (Phase 8)**: Can run after Foundational phase, parallel with user stories
- **Polish (Phase 9)**: Depends on all phases being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent from US1 but integrates with create/view
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent from US1/US2 but requires todos to exist
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Independent from US1/US2/US3 but requires todos to exist

### Within Each User Story (TDD Cycle)

1. **RED Phase**: Write ALL tests first, verify they FAIL
2. **GREEN Phase**: Implement code to make tests PASS (minimal implementation)
3. **CLI Integration**: Write integration tests, implement CLI commands
4. **REFACTOR Phase**: Clean up code, add docstrings, verify tests still PASS

### Parallel Opportunities

- **Phase 1 (Setup)**: Tasks T003, T004, T005, T006 can run in parallel
- **Phase 2 (Foundational)**: Tasks T007, T008, T009, T010 can run in parallel (different files)
- **Phase 3 (US1) - RED Phase**: Tasks T011-T022 can run in parallel (all test writing)
- **Phase 4 (US2) - RED Phase**: Tasks T040-T047 can run in parallel (all test writing)
- **Phase 5 (US3) - RED Phase**: Tasks T061-T066 can run in parallel (all test writing)
- **Phase 6 (US4) - RED Phase**: Tasks T078-T081 can run in parallel (all test writing)
- **Phase 8 (Performance)**: Tasks T103-T108 can run in parallel (different test files)
- **Phase 9 (Documentation)**: Tasks T110-T112 can run in parallel
- **User Stories**: After Phase 2, US1, US2, US3, US4 can be worked on by different team members in parallel

---

## Parallel Example: User Story 1

```bash
# RED Phase - Launch all test writing tasks together:
Task T011: "Write test for Todo creation with valid title in tests/unit/test_todo_model.py"
Task T012: "Write test for Todo creation with empty title in tests/unit/test_todo_model.py"
Task T013: "Write test for Todo creation with whitespace-only title in tests/unit/test_todo_model.py"
Task T014: "Write test for Todo default values in tests/unit/test_todo_model.py"
Task T015: "Write test for repository create() operation in tests/unit/test_repository.py"
Task T016: "Write test for repository get_all() with empty storage in tests/unit/test_repository.py"
Task T017: "Write test for repository get_all() with multiple todos in tests/unit/test_repository.py"
Task T018: "Write test for ID auto-increment in tests/unit/test_repository.py"
Task T019: "Write test for validate_title() with valid input in tests/unit/test_validators.py"
Task T020: "Write test for validate_title() with empty input in tests/unit/test_validators.py"
Task T021: "Write test for format_todo_list() with empty list in tests/unit/test_display.py"
Task T022: "Write test for format_todo_list() with multiple todos in tests/unit/test_display.py"

# Then run Task T023 to verify all tests FAIL

# GREEN Phase - Sequential implementation (tests must pass in order):
# Tasks T024-T031 run sequentially because they build on each other
```

---

## Parallel Example: Foundational Phase

```bash
# Launch all foundational components together (different files, no dependencies):
Task T007: "Implement Todo entity as frozen dataclass in src/models/todo.py"
Task T008: "Implement TodoRepository class with __init__ method in src/repository/todo_repository.py"
Task T009: "Implement validation functions in src/validation/validators.py"
Task T010: "Implement display formatter functions in src/cli/display.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T010) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T011-T039)
4. Complete Phase 7: Menu System (T093-T102) - Basic menu with just create/view
5. **STOP and VALIDATE**: Test User Story 1 independently
6. Deploy/demo if ready (MVP complete!)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (mark complete feature)
4. Add User Story 3 → Test independently → Deploy/Demo (update feature)
5. Add User Story 4 → Test independently → Deploy/Demo (delete feature)
6. Complete Phase 8 + 9 → Final validation → Production ready
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers after Foundational phase:

1. Team completes Setup (Phase 1) together
2. Team completes Foundational (Phase 2) together - BLOCKS all user stories
3. Once Foundational is done:
   - Developer A: User Story 1 (Phase 3) - T011-T039
   - Developer B: User Story 2 (Phase 4) - T040-T060
   - Developer C: User Story 3 (Phase 5) - T061-T077
   - Developer D: User Story 4 (Phase 6) - T078-T092
4. Stories complete and integrate independently
5. Team reconvenes for Phase 7 (Menu System integration)
6. Team completes Phase 8 + 9 together (Performance and Polish)

---

## Task Summary

**Total Tasks**: 151 tasks

**Tasks by Phase**:
- Phase 1 (Setup): 6 tasks
- Phase 2 (Foundational): 4 tasks
- Phase 3 (User Story 1 - MVP): 29 tasks
- Phase 4 (User Story 2): 21 tasks
- Phase 5 (User Story 3): 17 tasks
- Phase 6 (User Story 4): 15 tasks
- Phase 7 (Menu System): 10 tasks
- Phase 8 (Performance): 7 tasks
- Phase 9 (Polish & Verification): 42 tasks

**Tasks by User Story**:
- User Story 1 (Create and View): 29 tasks (T011-T039)
- User Story 2 (Mark Complete): 21 tasks (T040-T060)
- User Story 3 (Update): 17 tasks (T061-T077)
- User Story 4 (Delete): 15 tasks (T078-T092)

**Parallel Opportunities Identified**: 45+ tasks marked with [P]

**Independent Test Criteria**:
- US1: Create todos and verify list display with proper formatting
- US2: Mark todos complete and verify status indicators (✔ vs ✘)
- US3: Update todo details and verify completion status preserved
- US4: Delete todos and verify removal from list

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1) + minimal Phase 7 (menu with create/view only) = **45 tasks for MVP**

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story follows strict TDD: RED (tests fail) → GREEN (tests pass) → REFACTOR (clean up)
- Per constitution: No code without tests, no tests without spec, no implementation without failing tests first
- Verify tests fail before implementing (RED phase)
- Verify tests pass after implementing (GREEN phase)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All 18 functional requirements (FR-001 to FR-018) must be verified in Phase 9
- All 10 success criteria (SC-001 to SC-010) must be verified in Phase 9
- Constitution compliance is non-negotiable - verify throughout implementation
