---
id: 003
title: Full-Stack Todo App Implementation Plan
stage: plan
date: 2026-02-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-fullstack-todo-app
branch: 002-fullstack-todo-app
user: Arman
command: /sp.plan
labels: ["plan", "architecture", "design", "fullstack", "todo", "jwt", "security"]
links:
  spec: ../../../specs/002-fullstack-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-fullstack-todo-app/plan.md
  - specs/002-fullstack-todo-app/research.md
  - specs/002-fullstack-todo-app/data-model.md
  - specs/002-fullstack-todo-app/contracts/api.yaml
  - specs/002-fullstack-todo-app/quickstart.md
tests:
  - Constitutional compliance check (all gates passed)
  - Data model validation (user isolation enforced)
  - API contract validation (OpenAPI 3.0 compliant)
---

## Prompt

/sp.plan

# Phase II Implementation Plan — Full-Stack Todo App

## Step 1: Monorepo Initialization
- Create Spec-Kit monorepo structure
- Add .spec-kit/config.yaml
- Setup /specs directories by category

## Step 2: Backend Foundation
- Initialize FastAPI app
- Configure SQLModel with Neon PostgreSQL
- Load DATABASE_URL from environment

## Step 3: Authentication Middleware
- Implement JWT verification middleware
- Decode token using BETTER_AUTH_SECRET
- Attach authenticated user to request context

## Step 4: API Implementation
- Implement task CRUD endpoints
- Enforce user ownership in all queries
- Return proper HTTP status codes

## Step 5: Frontend Foundation
- Initialize Next.js App Router project
- Configure Better Auth
- Enable JWT token issuance

## Step 6: Frontend API Client
- Create centralized API client
- Automatically attach JWT to all requests
- Handle 401/403 responses globally

## Step 7: UI Implementation
- Build authentication pages
- Build task management UI
- Connect UI to backend APIs

## Step 8: Validation
- Verify all endpoints require JWT
- Confirm users cannot access others' tasks
- Validate persistence in Neon DB

## Completion Criteria
- All Phase II requirements satisfied
- Secure multi-user behavior confirmed
- Code generated from specifications

## Response snapshot

Created comprehensive implementation plan with Phase 0 research and Phase 1 design artifacts:

**Plan Document** (plan.md):
- Technical context fully specified (Python 3.11+, FastAPI, Next.js 14+, Neon PostgreSQL)
- Constitutional compliance verified (all 6 gates passed)
- Monorepo structure defined (backend/, frontend/, specs/, history/)
- 5 implementation milestones with acceptance criteria
- Risk assessment with 8 identified risks and mitigations
- Success metrics aligned with specification criteria

**Phase 0: Research** (research.md):
- 8 research areas resolved (Better Auth integration, JWT flow, database design, etc.)
- Decision: Better Auth for frontend, PyJWT for backend verification
- Decision: Standard bearer token flow with client-side storage
- Decision: User isolation via user_id FK with indexed queries
- Decision: SQLModel QueuePool connection pooling (size 10, overflow 20)
- Decision: Next.js middleware + API interceptors for auth routing
- Decision: RESTful design with user_id in path for explicit validation
- Decision: 3-layer testing (unit, integration, E2E)
- Decision: Standard HTTP status codes (401 Unauthorized, 403 Forbidden)
- All "NEEDS CLARIFICATION" items resolved with rationale and alternatives

**Phase 1: Design & Contracts**:

1. **Data Model** (data-model.md):
   - User entity: id (UUID), email, password_hash, timestamps
   - Task entity: id (auto-increment), user_id (FK), title, description, completed, timestamps
   - Indexes: user_id (CRITICAL for <1s queries), completed, composite (user_id, completed)
   - Relationships: User 1:Many Task with cascade delete
   - 6 data access patterns with SQLModel code examples
   - User isolation enforcement patterns (ownership verification)
   - Database constraints and validation rules
   - Migration strategy (Alembic for production)

2. **API Contracts** (contracts/api.yaml):
   - OpenAPI 3.0 specification with 6 endpoints
   - Authentication: POST /api/auth/signup, POST /api/auth/login
   - Tasks: GET/POST /api/{user_id}/tasks, GET/PUT/DELETE /api/{user_id}/tasks/{task_id}
   - JWT bearer token security scheme
   - Complete request/response schemas with validation rules
   - HTTP status codes documented (200, 201, 204, 400, 401, 403, 404, 500)
   - Error response format with field-level validation errors
   - Examples for all endpoints

3. **Quickstart Guide** (quickstart.md):
   - 10-step quick start (5 minutes to running application)
   - Detailed setup instructions for backend (FastAPI + SQLModel)
   - Detailed setup instructions for frontend (Next.js + Better Auth)
   - Environment variable reference with all required vars
   - Common development tasks (new endpoint, new component)
   - Troubleshooting guide (7 common issues with solutions)
   - Testing instructions (pytest for backend, Jest for frontend)
   - Database migration workflow (Alembic)
   - Production deployment examples (Heroku, Vercel)

**Key Architectural Decisions**:
- Monorepo with separate backend/ and frontend/ directories
- JWT verification in FastAPI middleware (every request)
- User_id in URL path for explicit ownership validation
- Database-level user isolation via indexed user_id filtering
- Stateless REST API (no shared runtime state)
- Better Auth for frontend auth UI, PyJWT for backend verification
- CORS configured to allow frontend → backend communication
- Connection pooling (10+20 connections per backend instance)

**Constitutional Compliance**:
✅ Specification-First: All design from approved spec.md
✅ TDD: Tests will be written before implementation
✅ Security-First: JWT on all requests, user_id matching, database-level isolation
✅ Technology Stack: Next.js + FastAPI + Neon PostgreSQL + Better Auth
✅ Separation of Concerns: Frontend/backend independent, REST API only
✅ User Isolation: Foreign key + indexed queries + ownership verification

**Risk Mitigation**:
- Better Auth integration: Research phase identified pattern
- JWT secret sync: Single BETTER_AUTH_SECRET env var
- Cross-user leaks: Database filtering + dedicated integration tests
- CORS errors: Explicit middleware + integration tests
- Connection limits: Pooling configured for 3 instances

## Outcome

- ✅ Impact: Complete architectural plan with research, data model, API contracts, and setup guide
- 🧪 Tests: Constitutional compliance validated (all gates passed)
- 📁 Files: Created plan.md, research.md, data-model.md, contracts/api.yaml, quickstart.md
- 🔁 Next prompts: `/sp.tasks` to generate dependency-ordered implementation tasks
- 🧠 Reflection: Plan successfully captures security-first architecture with JWT verification on all requests, database-level user isolation, and separation of concerns. All research questions resolved with documented decisions and alternatives. Data model enforces user ownership via foreign key and indexed queries. API contract provides complete OpenAPI spec. Quickstart enables 15-minute setup. Ready for task generation and TDD implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitutional Check - PASS (all 6 gates), Data Model - PASS (user isolation enforced), API Contract - PASS (OpenAPI 3.0 valid)
- Prompt variant (if applicable): User provided structured plan outline with 8 steps and completion criteria
- Next experiment (smallest change to try): Validate that generated tasks align with prioritized user stories (P1 first) and constitutional TDD requirement (tests before code)
