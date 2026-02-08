---
id: 001
title: Phase II Constitution Creation
stage: constitution
date: 2026-02-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-todo-crud
user: Arman
command: /sp.constitution
labels: ["constitution", "governance", "security", "architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - None (constitution document)
---

## Prompt

/sp.constitution

# Phase II Constitution — Todo Full-Stack Web Application

## Mission
Transform the Phase I in-memory console Todo app into a secure, multi-user,
full-stack web application using strict Spec-Driven Development.

## Non-Negotiable Rules
1. All backend and frontend code must be generated exclusively from specifications.
2. Manual coding or ad-hoc changes are strictly forbidden.
3. The project must be organized as a monorepo using Spec-Kit conventions.
4. All task data must be persisted in Neon Serverless PostgreSQL.
5. Authentication must be implemented using Better Auth with JWT.
6. Every API request must require a valid JWT token.
7. Task ownership must be enforced at the database query level.
8. Frontend and backend must share no runtime state.
9. Environment variables must be used for secrets and database URLs.

## Architecture Principles
- Frontend: Next.js App Router (server-first)
- Backend: FastAPI with SQLModel
- Stateless REST API secured via JWT
- Strict separation of frontend, backend, specs, and configuration
- User isolation is mandatory

## Security Rules
- JWT must be verified on every request
- User ID from token must match URL user_id
- Unauthorized requests must return HTTP 401
- Cross-user data access is prohibited

## Response snapshot

Created comprehensive Phase II constitution (v1.0.0) with the following structure:

**Core Principles (4):**
1. Mission-Driven Development
2. Specification-First (NON-NEGOTIABLE)
3. Test-Driven Development (NON-NEGOTIABLE)
4. Security-First Architecture

**Architecture Principles:**
- Technology Stack (Next.js, FastAPI, Neon PostgreSQL, Better Auth)
- Separation of Concerns (frontend/backend isolation)
- Data Persistence (no in-memory production data)
- User Isolation (NON-NEGOTIABLE, database-level enforcement)

**Security Rules:**
- Authentication & Authorization (JWT required for all requests)
- Request Validation (user_id matching, 401 for cross-user access)
- Environment Security (no hardcoded secrets)

**Project Organization:**
- Monorepo structure defined
- Spec-Driven Workflow (6 steps)

**Quality Standards:**
- Code Quality (type hints, strict TypeScript)
- Testing Requirements (80% coverage, integration tests)
- Documentation (OpenAPI, ER diagrams, ADRs)

**Governance:**
- Constitution Authority (supersedes all practices)
- Amendment Process (5 steps)
- Version Control (semantic versioning)
- Compliance Review (blocking violations)

Constitution file created at: `.specify/memory/constitution.md`

## Outcome

- ✅ Impact: Established foundational governance document for Phase II full-stack development
- 🧪 Tests: None (governance document, not code)
- 📁 Files: Created/updated `.specify/memory/constitution.md`
- 🔁 Next prompts: `/sp.specify` to create feature specifications based on constitutional principles
- 🧠 Reflection: Constitution successfully captures security-first, spec-driven, TDD-mandatory approach for multi-user todo app transformation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (constitution creation)
- Prompt variant (if applicable): Direct constitution content provided by user
- Next experiment (smallest change to try): Validate template consistency with new constitutional requirements
