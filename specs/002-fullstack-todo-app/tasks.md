# Tasks: Full-Stack Todo Web Application

**Input**: Design documents from `/specs/002-fullstack-todo-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api.yaml

**Tests**: TDD is MANDATORY per constitution (Principle III). Tests MUST be written FIRST, approved, FAIL, then implement.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5, US6)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md monorepo structure:
- Backend: `backend/src/`, `backend/tests/`
- Frontend: `frontend/src/`, `frontend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and monorepo structure

- [x] T001 Create monorepo directory structure (backend/, frontend/, specs/, history/)
- [x] T002 [P] Initialize backend Python project with Poetry in backend/pyproject.toml
- [x] T003 [P] Initialize frontend Next.js project with TypeScript in frontend/package.json
- [x] T004 [P] Create backend .env.example with DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS, ENVIRONMENT
- [x] T005 [P] Create frontend .env.local.example with NEXT_PUBLIC_API_URL, NEXT_PUBLIC_BETTER_AUTH_URL
- [x] T006 [P] Add .gitignore for backend (.env, __pycache__, .pytest_cache, *.pyc)
- [x] T007 [P] Add .gitignore for frontend (.env.local, .next, node_modules)
- [x] T008 [P] Create backend README.md with setup instructions
- [x] T009 [P] Create frontend README.md with setup instructions
- [x] T010 [P] Create root-level docker-compose.yml for local development environment

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [x] T011 Install backend dependencies in backend/pyproject.toml (FastAPI 0.109+, SQLModel 0.0.14+, PyJWT 2.8+, python-dotenv, psycopg2-binary, uvicorn)
- [x] T012 Install backend dev dependencies (pytest 7.4+, pytest-asyncio, pytest-cov, httpx)
- [x] T013 Create backend/src/__init__.py (empty init file)
- [x] T014 Implement environment configuration in backend/src/config.py (load DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS from .env)
- [x] T015 Implement database connection in backend/src/database.py (SQLModel engine with connection pooling: size=10, max_overflow=20)
- [x] T016 Create database initialization function in backend/src/database.py (create_all for development, Alembic for production)
- [x] T017 Create FastAPI app entry point in backend/src/main.py with CORS middleware
- [x] T018 Configure pytest in backend/pytest.ini (asyncio_mode=auto, testpaths=tests, coverage minimum 80%)
- [x] T019 Create pytest fixtures in backend/tests/conftest.py (test database, test client, auth token generators)

### Frontend Foundation

- [x] T020 Install frontend dependencies in frontend/package.json (Next.js 14+, React 18+, Better Auth, axios)
- [x] T021 Install frontend dev dependencies (TypeScript 5+, @types/react, @types/node, Jest 29+, @testing-library/react, @testing-library/jest-dom)
- [x] T022 Configure TypeScript in frontend/tsconfig.json (strict mode enabled)
- [x] T023 Configure Jest in frontend/jest.config.js (testEnvironment: jsdom, setupFilesAfterEnv for testing-library)
- [x] T024 Create Next.js root layout in frontend/src/app/layout.tsx
- [x] T025 Create Next.js home page in frontend/src/app/page.tsx (redirect to /tasks if authenticated, else /login)
- [x] T026 Create TypeScript interfaces in frontend/src/lib/types.ts (User, Task, AuthResponse, ErrorResponse)
- [x] T027 Configure Better Auth in frontend/src/lib/auth.ts (email/password provider, JWT config)
- [x] T028 Implement API client with JWT interceptor in frontend/src/lib/api-client.ts (axios instance, auto-attach Bearer token, handle 401/403)
- [x] T029 Implement Next.js middleware for route protection in frontend/src/middleware.ts (protect /tasks routes, allow /login and /signup)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts and authenticate securely via Better Auth with JWT tokens

**Independent Test**: Create new account → Login → Receive JWT token → Verify token works for API requests → Logout → Verify protected routes redirect to login

### Tests for User Story 1 (TDD - Write FIRST, ensure FAIL)

- [x] T030 [P] [US1] Write integration test for user signup in backend/tests/test_auth.py (POST /api/auth/signup with valid email/password → 201 Created → returns user_id, email, token)
- [x] T031 [P] [US1] Write integration test for user login in backend/tests/test_auth.py (POST /api/auth/login with correct credentials → 200 OK → returns token)
- [x] T032 [P] [US1] Write integration test for invalid login in backend/tests/test_auth.py (POST /api/auth/login with wrong password → 401 Unauthorized)
- [x] T033 [P] [US1] Write integration test for duplicate email in backend/tests/test_auth.py (POST /api/auth/signup with existing email → 400 Bad Request)
- [x] T034 [P] [US1] Write integration test for missing JWT token in backend/tests/test_auth.py (GET /api/{user_id}/tasks without Authorization header → 401 Unauthorized)
- [x] T035 [P] [US1] Write integration test for invalid JWT token in backend/tests/test_auth.py (GET /api/{user_id}/tasks with malformed token → 401 Unauthorized)
- [x] T036 [P] [US1] Write integration test for expired JWT token in backend/tests/test_auth.py (GET /api/{user_id}/tasks with expired token → 401 Unauthorized)
- [x] T037 [P] [US1] Write component test for AuthForm in frontend/tests/components/AuthForm.test.tsx (renders email/password inputs, submits form, displays errors)
- [x] T038 [P] [US1] Write E2E test for signup flow in frontend/tests/e2e/auth-flow.spec.ts (navigate to signup → fill form → submit → redirected to tasks page)

**Run tests - verify ALL FAIL** ✅

### Implementation for User Story 1

**Backend - Database Models**:
- [x] T039 [P] [US1] Create User model in backend/src/models/user.py (SQLModel with id, email, password_hash, created_at, updated_at; relationship to tasks)
- [x] T040 [US1] Create database init/migration script in backend/src/models/__init__.py (import User model, configure SQLModel metadata)

**Backend - JWT Middleware**:
- [x] T041 [US1] Implement JWT verification middleware in backend/src/middleware/auth.py (decode token using BETTER_AUTH_SECRET, extract user_id, attach to request.state, raise 401 on invalid/expired token)
- [x] T042 [US1] Create middleware __init__.py in backend/src/middleware/__init__.py (export verify_jwt_middleware)

**Backend - Authentication Router**:
- [x] T043 [US1] Implement signup endpoint in backend/src/routers/auth.py (POST /api/auth/signup: validate email, hash password, create user, return JWT token)
- [x] T044 [US1] Implement login endpoint in backend/src/routers/auth.py (POST /api/auth/login: verify credentials, return JWT token)
- [x] T045 [US1] Create Pydantic schemas for auth in backend/src/schemas/auth.py (SignupRequest, LoginRequest, AuthResponse)
- [x] T046 [US1] Register auth router in backend/src/main.py (app.include_router for /api/auth routes, no JWT required)

**Frontend - Authentication Pages**:
- [x] T047 [P] [US1] Create AuthForm component in frontend/src/components/AuthForm.tsx (email/password inputs, submit button, error display, loading state)
- [x] T048 [P] [US1] Create login page in frontend/src/app/login/page.tsx (render AuthForm with mode="login", call /api/auth/login, store token, redirect to /tasks)
- [x] T049 [P] [US1] Create signup page in frontend/src/app/signup/page.tsx (render AuthForm with mode="signup", call /api/auth/signup, store token, redirect to /tasks)
- [x] T050 [US1] Add logout functionality in frontend/src/lib/auth.ts (clear token from storage, redirect to /login)

**Run tests - verify ALL PASS** ✅

**Checkpoint**: At this point, users can signup, login, and logout. JWT tokens are issued and verified. User Story 1 is fully functional and testable independently.

---

## Phase 4: User Story 2 - View Personal Task List (Priority: P1)

**Goal**: Authenticated users can view all their personal tasks in a list, seeing only tasks they own

**Independent Test**: Authenticate user → Create sample tasks for user → GET /api/{user_id}/tasks → Verify only user's tasks returned → Verify another user cannot see first user's tasks (403 Forbidden)

### Tests for User Story 2 (TDD - Write FIRST, ensure FAIL)

- [x] T051 [P] [US2] Write integration test for getting user tasks in backend/tests/test_tasks.py (GET /api/{user_id}/tasks with valid JWT → 200 OK → returns array of user's tasks)
- [x] T052 [P] [US2] Write integration test for empty task list in backend/tests/test_tasks.py (GET /api/{user_id}/tasks for user with no tasks → 200 OK → returns empty array)
- [x] T053 [P] [US2] Write integration test for user isolation in backend/tests/test_user_isolation.py (User A creates task → User B tries GET /api/userA/tasks → 403 Forbidden)
- [x] T054 [P] [US2] Write integration test for user_id mismatch in backend/tests/test_user_isolation.py (JWT has user_id "A" → GET /api/userB/tasks → 403 Forbidden)
- [x] T055 [P] [US2] Write component test for TaskList in frontend/tests/components/TaskList.test.tsx (renders list of tasks, displays task titles, shows empty state)
- [x] T056 [P] [US2] Write component test for TaskItem in frontend/tests/components/TaskItem.test.tsx (displays title, description, completed status, timestamps)

**Run tests - verify ALL FAIL** ✅

### Implementation for User Story 2

**Backend - Task Model**:
- [x] T057 [US2] Create Task model in backend/src/models/task.py (SQLModel with id, user_id FK, title, description, completed, created_at, updated_at; indexes on user_id and completed; relationship to user)

**Backend - Task Service**:
- [x] T058 [US2] Implement get_user_tasks in backend/src/services/task_service.py (query tasks filtering by user_id, order by created_at desc, enforce ownership)
- [x] T059 [US2] Create service __init__.py in backend/src/services/__init__.py (export task_service functions)

**Backend - Task Router**:
- [x] T060 [US2] Implement GET /api/{user_id}/tasks endpoint in backend/src/routers/tasks.py (verify user_id matches JWT, call task_service, return task list)
- [x] T061 [US2] Create Pydantic schemas for tasks in backend/src/schemas/task.py (TaskResponse with all fields)
- [x] T062 [US2] Register tasks router in backend/src/main.py (app.include_router with JWT middleware dependency)

**Frontend - Task List UI**:
- [x] T063 [P] [US2] Create TaskItem component in frontend/src/components/TaskItem.tsx (display title, description, completed checkbox, timestamps, actions)
- [x] T064 [US2] Create TaskList component in frontend/src/components/TaskList.tsx (fetch tasks from API, render TaskItem for each, show loading state, handle errors, display empty state)
- [x] T065 [US2] Create task list page in frontend/src/app/tasks/page.tsx (render TaskList component, require authentication)

**Run tests - verify ALL PASS** ✅

**Checkpoint**: At this point, authenticated users can view their task list. User isolation is enforced (403 on cross-user access). User Stories 1 AND 2 are fully functional.

---

## Phase 5: User Story 3 - Create New Tasks (Priority: P1)

**Goal**: Authenticated users can create new todo tasks with title and optional description

**Independent Test**: Authenticate user → POST /api/{user_id}/tasks with title → Verify task created with user_id, default completed=false → GET tasks → Verify new task appears

### Tests for User Story 3 (TDD - Write FIRST, ensure FAIL)

- [x] T066 [P] [US3] Write integration test for creating task in backend/tests/test_tasks.py (POST /api/{user_id}/tasks with title → 201 Created → returns task with id, user_id, completed=false)
- [x] T067 [P] [US3] Write integration test for creating task with description in backend/tests/test_tasks.py (POST /api/{user_id}/tasks with title and description → both fields saved)
- [x] T068 [P] [US3] Write integration test for empty title validation in backend/tests/test_tasks.py (POST /api/{user_id}/tasks with empty title → 400 Bad Request → validation error)
- [x] T069 [P] [US3] Write integration test for cross-user creation in backend/tests/test_user_isolation.py (JWT user_id "A" → POST /api/userB/tasks → 403 Forbidden)
- [x] T070 [P] [US3] Write component test for TaskForm in frontend/tests/components/TaskForm.test.tsx (renders title/description inputs, submits form, displays validation errors)

**Run tests - verify ALL FAIL** ✅

### Implementation for User Story 3

**Backend - Task Service**:
- [x] T071 [US3] Implement create_task in backend/src/services/task_service.py (validate title not empty, create task with user_id from JWT, set completed=false, return created task)

**Backend - Task Router**:
- [x] T072 [US3] Implement POST /api/{user_id}/tasks endpoint in backend/src/routers/tasks.py (verify user_id matches JWT, validate request body, call task_service.create_task, return 201 Created)
- [x] T073 [US3] Create Pydantic schema for task creation in backend/src/schemas/task.py (TaskCreateRequest with title required, description optional)

**Frontend - Task Creation UI**:
- [x] T074 [US3] Create TaskForm component in frontend/src/components/TaskForm.tsx (title input required, description textarea optional, submit button, validation, error display)
- [x] T075 [US3] Add task creation to task list page in frontend/src/app/tasks/page.tsx (render TaskForm, on submit call API, refresh task list, show success/error messages)

**Run tests - verify ALL PASS** ✅

**Checkpoint**: At this point, users can signup, login, view tasks, and create new tasks. User Stories 1, 2, AND 3 are fully functional (MVP complete!).

---

## Phase 6: User Story 4 - Update Task Status and Details (Priority: P2)

**Goal**: Authenticated users can update their tasks (title, description, completed status)

**Independent Test**: Create task → PUT /api/{user_id}/tasks/{id} with updated fields → Verify changes saved → Verify updated_at timestamp changed → Verify other user cannot update (403)

### Tests for User Story 4 (TDD - Write FIRST, ensure FAIL)

- [x] T076 [P] [US4] Write integration test for updating task in backend/tests/test_tasks.py (PUT /api/{user_id}/tasks/{id} with new title → 200 OK → changes saved, updated_at changed)
- [x] T077 [P] [US4] Write integration test for marking task complete in backend/tests/test_tasks.py (PUT with completed=true → status updated)
- [x] T078 [P] [US4] Write integration test for empty title validation on update in backend/tests/test_tasks.py (PUT with empty title → 400 Bad Request)
- [x] T079 [P] [US4] Write integration test for cross-user update in backend/tests/test_user_isolation.py (User A tries PUT /api/userB/tasks/{id} → 403 Forbidden)
- [x] T080 [P] [US4] Write integration test for updating non-existent task in backend/tests/test_tasks.py (PUT /api/{user_id}/tasks/9999 → 404 Not Found)

**Run tests - verify ALL FAIL** ✅

### Implementation for User Story 4

**Backend - Task Service**:
- [x] T081 [US4] Implement update_task in backend/src/services/task_service.py (verify ownership, validate title if provided, update fields, set updated_at=now(), return updated task)
- [x] T082 [US4] Implement get_task_with_ownership in backend/src/services/task_service.py (get task by id, verify user_id matches, raise 403 if mismatch, raise 404 if not found)

**Backend - Task Router**:
- [x] T083 [US4] Implement PUT /api/{user_id}/tasks/{task_id} endpoint in backend/src/routers/tasks.py (verify user_id matches JWT, call task_service.update_task, return updated task)
- [x] T084 [US4] Implement GET /api/{user_id}/tasks/{task_id} endpoint in backend/src/routers/tasks.py (verify user_id matches JWT, call task_service.get_task_with_ownership, return task)
- [x] T085 [US4] Create Pydantic schema for task update in backend/src/schemas/task.py (TaskUpdateRequest with optional title, description, completed)

**Frontend - Task Update UI**:
- [x] T086 [US4] Add task completion toggle to TaskItem component in frontend/src/components/TaskItem.tsx (checkbox for completed, on change call PUT /api/{user_id}/tasks/{id})
- [x] T087 [US4] Create task detail/edit page in frontend/src/app/tasks/[id]/page.tsx (fetch task, render TaskForm in edit mode, on submit call PUT endpoint, redirect to list)
- [x] T088 [US4] Add edit button to TaskItem in frontend/src/components/TaskItem.tsx (navigate to /tasks/{id} on click)

**Run tests - verify ALL PASS** ✅

**Checkpoint**: At this point, users can update task title, description, and completion status. User Stories 1-4 are fully functional.

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P2)

**Goal**: Authenticated users can permanently delete their tasks

**Independent Test**: Create task → DELETE /api/{user_id}/tasks/{id} → Verify task deleted (204 No Content) → GET tasks → Verify task not in list → Verify other user cannot delete (403)

### Tests for User Story 5 (TDD - Write FIRST, ensure FAIL)

- [x] T089 [P] [US5] Write integration test for deleting task in backend/tests/test_tasks.py (DELETE /api/{user_id}/tasks/{id} → 204 No Content → task removed from database)
- [x] T090 [P] [US5] Write integration test for cross-user delete in backend/tests/test_user_isolation.py (User A tries DELETE /api/userB/tasks/{id} → 403 Forbidden)
- [x] T091 [P] [US5] Write integration test for deleting non-existent task in backend/tests/test_tasks.py (DELETE /api/{user_id}/tasks/9999 → 404 Not Found)

**Run tests - verify ALL FAIL** ✅

### Implementation for User Story 5

**Backend - Task Service**:
- [x] T092 [US5] Implement delete_task in backend/src/services/task_service.py (verify ownership via get_task_with_ownership, delete from database, return None)

**Backend - Task Router**:
- [x] T093 [US5] Implement DELETE /api/{user_id}/tasks/{task_id} endpoint in backend/src/routers/tasks.py (verify user_id matches JWT, call task_service.delete_task, return 204 No Content)

**Frontend - Task Deletion UI**:
- [x] T094 [US5] Add delete button to TaskItem in frontend/src/components/TaskItem.tsx (confirm dialog, on confirm call DELETE endpoint, remove from list)
- [x] T095 [US5] Add error handling for delete operations in frontend/src/components/TaskItem.tsx (display error message if delete fails)

**Run tests - verify ALL PASS** ✅

**Checkpoint**: At this point, users can delete tasks. User Stories 1-5 are fully functional.

---

## Phase 8: User Story 6 - Filter Tasks by Completion Status (Priority: P3)

**Goal**: Authenticated users can filter task list to show only completed or incomplete tasks

**Independent Test**: Create completed and incomplete tasks → GET /api/{user_id}/tasks?completed=false → Verify only incomplete tasks returned → GET ?completed=true → Verify only completed tasks returned

### Tests for User Story 6 (TDD - Write FIRST, ensure FAIL)

- [x] T096 [P] [US6] Write integration test for filtering incomplete tasks in backend/tests/test_tasks.py (GET /api/{user_id}/tasks?completed=false → returns only incomplete tasks)
- [x] T097 [P] [US6] Write integration test for filtering completed tasks in backend/tests/test_tasks.py (GET /api/{user_id}/tasks?completed=true → returns only completed tasks)
- [x] T098 [P] [US6] Write integration test for filtered list with user isolation in backend/tests/test_user_isolation.py (GET /api/{user_id}/tasks?completed=false → still only returns user's tasks, not other users')

**Run tests - verify ALL FAIL** ✅

### Implementation for User Story 6

**Backend - Task Service**:
- [x] T099 [US6] Update get_user_tasks in backend/src/services/task_service.py (add optional completed parameter, filter query by completed status if provided, use composite index)

**Backend - Task Router**:
- [x] T100 [US6] Update GET /api/{user_id}/tasks endpoint in backend/src/routers/tasks.py (add optional query parameter completed: bool | None, pass to task_service)

**Frontend - Task Filtering UI**:
- [x] T101 [US6] Add filter controls to TaskList in frontend/src/components/TaskList.tsx (radio buttons or dropdown: All, Incomplete, Completed)
- [x] T102 [US6] Update TaskList API call to include completed query parameter based on filter selection

**Run tests - verify ALL PASS** ✅

**Checkpoint**: All user stories (1-6) are now fully functional and independently testable. Application complete!

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and production readiness

### Documentation

- [ ] T103 [P] Update backend README.md with complete setup instructions, environment variables, running tests, API documentation link
- [ ] T104 [P] Update frontend README.md with setup instructions, environment variables, running tests, component documentation
- [ ] T105 [P] Create root-level README.md with project overview, quickstart link, architecture diagram, deployment instructions
- [ ] T106 [P] Generate OpenAPI/Swagger documentation in backend/src/main.py (configure FastAPI app with title, description, version, contact)
- [ ] T107 [P] Create API documentation page accessible at http://localhost:8000/docs

### Security Hardening

- [ ] T108 Audit all backend endpoints to verify JWT middleware is applied (no endpoint bypasses authentication)
- [ ] T109 Audit all database queries to verify user_id filtering (no queries miss user isolation)
- [ ] T110 Add rate limiting middleware to backend auth endpoints in backend/src/middleware/rate_limit.py (prevent brute force attacks)
- [ ] T111 Add input sanitization for title and description fields in backend/src/schemas/task.py (prevent XSS)
- [ ] T112 Add HTTPS enforcement for production in backend/src/main.py (redirect HTTP to HTTPS)

### Performance Optimization

- [ ] T113 [P] Verify database indexes on tasks.user_id and tasks.completed in backend/src/models/task.py
- [ ] T114 [P] Add database query logging in development mode in backend/src/database.py (echo=True when ENVIRONMENT=development)
- [ ] T115 Test API performance with 1000 tasks per user (verify <1 second response time per SC-003)
- [ ] T116 Optimize frontend TaskList rendering for large lists (virtualization if needed)

### Testing & Quality

- [ ] T117 Run full backend test suite and verify 80%+ code coverage (pytest --cov=backend/src --cov-report=html)
- [ ] T118 Run frontend component tests (npm test in frontend/)
- [ ] T119 Run E2E tests for all user flows (Playwright tests in frontend/tests/e2e/)
- [ ] T120 Fix any failing tests and achieve 100% pass rate
- [ ] T121 Run linting and formatting on backend code (ruff check backend/src/)
- [ ] T122 Run linting and formatting on frontend code (npm run lint in frontend/)

### Deployment Preparation

- [ ] T123 Create Dockerfile for backend in backend/Dockerfile (Python 3.11 base, install dependencies, expose port 8000)
- [ ] T124 Create Dockerfile for frontend in frontend/Dockerfile (Node 18 base, build Next.js, expose port 3000)
- [ ] T125 Update docker-compose.yml with backend, frontend, and postgres services for local testing
- [ ] T126 Create deployment guide in docs/deployment.md (Heroku, Vercel, Docker, environment variables)
- [ ] T127 Create .env.production.example with production environment variable templates
- [ ] T128 Verify quickstart.md instructions work end-to-end (follow guide from scratch)

### Error Handling & Logging

- [ ] T129 Implement structured logging in backend in backend/src/logging_config.py (configure Python logging with JSON formatter)
- [ ] T130 Add request logging middleware in backend/src/middleware/logging.py (log all requests with duration, status code, user_id)
- [ ] T131 Add error logging for 500 errors in backend/src/main.py (exception handler logs stack traces)
- [ ] T132 Implement user-friendly error messages in frontend in frontend/src/lib/error-handler.ts (map API errors to human-readable messages)
- [ ] T133 Add global error boundary in frontend in frontend/src/app/error.tsx (catch React errors, display friendly message)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

All user stories depend on Foundational (Phase 2) completing first. After that:

- **User Story 1 (P1)**: Can start immediately after Foundational - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational - Requires Task model (can be in parallel with US3)
- **User Story 3 (P1)**: Can start after Foundational - Requires Task model (can be in parallel with US2)
- **User Story 4 (P2)**: Can start after Foundational - Integrates with US2 (view tasks) and US3 (create tasks) but independently testable
- **User Story 5 (P2)**: Can start after Foundational - Independent from other stories
- **User Story 6 (P3)**: Depends on US2 (view tasks) - Extends filtering capability

### Within Each User Story (TDD Workflow)

1. **Tests FIRST**: Write all tests for the story, verify they FAIL (Red)
2. **Models**: Create database models (can be parallel if multiple models)
3. **Services**: Implement business logic (depends on models)
4. **Routers/Endpoints**: Implement API endpoints (depends on services)
5. **Frontend Components**: Implement UI (can be parallel with backend if API contract is defined)
6. **Integration**: Connect frontend to backend
7. **Tests PASS**: Run tests, verify they all PASS (Green)
8. **Refactor**: Clean up code while keeping tests passing

### Parallel Opportunities

**Within Setup (Phase 1)**: All tasks marked [P] can run in parallel (T002-T010)

**Within Foundational (Phase 2)**: Backend and Frontend foundations can run in parallel
- Backend tasks (T011-T019) can run in parallel with Frontend tasks (T020-T029)

**Across User Stories**: Once Foundational is complete, user stories can run in parallel
- Recommend: US1 first (authentication blocks testing other stories)
- Then: US2 and US3 in parallel (both P1, both use Task model)
- Then: US4, US5, US6 can proceed

**Within Each User Story**: All test tasks marked [P] can run in parallel, all model tasks marked [P] can run in parallel

---

## Parallel Example: User Story 2

```bash
# After Foundational phase completes:

# STEP 1: Launch all tests for User Story 2 together (TDD - write FIRST):
Task T051: "Write integration test for getting user tasks"
Task T052: "Write integration test for empty task list"
Task T053: "Write integration test for user isolation"
Task T054: "Write integration test for user_id mismatch"
Task T055: "Write component test for TaskList"
Task T056: "Write component test for TaskItem"

# Verify ALL tests FAIL (Red) ✅

# STEP 2: Implement User Story 2:
Task T057: "Create Task model" (blocking for service)
Task T058: "Implement get_user_tasks service"
Task T059: "Create service __init__.py"
Task T060: "Implement GET /api/{user_id}/tasks endpoint"
Task T061: "Create Pydantic schemas"
Task T062: "Register tasks router"

# STEP 3: Frontend (can be parallel with backend if API contract known):
Task T063: "Create TaskItem component" [P]
Task T064: "Create TaskList component"
Task T065: "Create task list page"

# STEP 4: Run tests - verify ALL PASS (Green) ✅
```

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only) - Recommended

1. Complete **Phase 1: Setup** (T001-T010)
2. Complete **Phase 2: Foundational** (T011-T029) - CRITICAL BLOCKING PHASE
3. Complete **Phase 3: User Story 1** (T030-T050) - Authentication
   - **STOP and VALIDATE**: Can users signup and login? ✅
4. Complete **Phase 4: User Story 2** (T051-T065) - View tasks
   - **STOP and VALIDATE**: Can users view their task list? User isolation works? ✅
5. Complete **Phase 5: User Story 3** (T066-T075) - Create tasks
   - **STOP and VALIDATE**: Can users create new tasks? ✅
6. **MVP COMPLETE!** 🎯 Deploy and demo
7. Continue with US4, US5, US6 as needed

### Incremental Delivery (All User Stories)

1. **Foundation**: Setup + Foundational (T001-T029)
2. **MVP**: User Stories 1-3 (T030-T075) → Test → Deploy
3. **Enhancement 1**: User Story 4 (T076-T088) → Test → Deploy
4. **Enhancement 2**: User Story 5 (T089-T095) → Test → Deploy
5. **Enhancement 3**: User Story 6 (T096-T102) → Test → Deploy
6. **Production Ready**: Polish (T103-T133) → Final testing → Production deployment

Each increment adds value without breaking previous functionality.

### Parallel Team Strategy

With 3 developers available:

1. **All together**: Complete Setup + Foundational (T001-T029)
2. **Split by user story** (once Foundational done):
   - **Developer A**: User Story 1 (Authentication) - T030-T050
   - **Developer B**: User Story 2 (View tasks) - T051-T065
   - **Developer C**: User Story 3 (Create tasks) - T066-T075
3. **Merge and integrate**: Test all stories together
4. **Continue in parallel**: Developers pick next priority stories (US4, US5, US6)

---

## Task Count Summary

**Total Tasks**: 133
- Phase 1 (Setup): 10 tasks
- Phase 2 (Foundational): 19 tasks (BLOCKING)
- Phase 3 (User Story 1 - Auth): 21 tasks (9 tests + 12 implementation)
- Phase 4 (User Story 2 - View): 15 tasks (6 tests + 9 implementation)
- Phase 5 (User Story 3 - Create): 10 tasks (5 tests + 5 implementation)
- Phase 6 (User Story 4 - Update): 13 tasks (5 tests + 8 implementation)
- Phase 7 (User Story 5 - Delete): 7 tasks (3 tests + 4 implementation)
- Phase 8 (User Story 6 - Filter): 7 tasks (3 tests + 4 implementation)
- Phase 9 (Polish): 31 tasks

**Test Tasks**: 31 (TDD mandatory per constitution)
**Implementation Tasks**: 102

**Parallel Opportunities**: 45 tasks marked [P] can run in parallel

**MVP Scope** (Recommended first delivery):
- Phases 1-5 (User Stories 1-3): 75 tasks
- Estimated time: 2-3 weeks for solo developer, 1-2 weeks for team of 3

---

## Notes

- **[P] marker**: Task can run in parallel with other [P] tasks (different files, no blocking dependencies)
- **[Story] label**: Maps task to user story for traceability and independent testing
- **TDD Required**: Constitution mandates tests FIRST → verify FAIL → implement → verify PASS
- **User Isolation**: CRITICAL security requirement - every task query must filter by user_id
- **JWT Verification**: MANDATORY on all task endpoints (no bypasses allowed)
- **Independent Stories**: Each user story should be completable and testable without others (except dependencies on Foundational phase)
- **File Paths**: All tasks include specific file paths for clarity
- **Checkpoints**: After each user story phase, STOP and validate that story works independently
- **Commit Strategy**: Commit after each task or logical group of tasks
- **Constitutional Compliance**: All tasks align with specification-first, TDD, security-first principles

---

**Tasks Status**: ✅ Complete and ready for implementation
**Next Command**: Begin with Phase 1 (Setup) or use `/sp.implement` to execute tasks automatically
**Recommended Start**: T001 (Create monorepo directory structure)
