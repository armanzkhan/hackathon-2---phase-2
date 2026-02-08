<!--
Sync Impact Report:
- Version change: Template → 1.0.0
- Modified principles: All (initial constitution creation)
- Added sections: Core Principles (4), Architecture Principles, Security Rules, Governance
- Removed sections: Template placeholders
- Templates requiring updates: All templates verified (✅)
- Follow-up TODOs: None
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### I. Mission-Driven Development
Transform the Phase I in-memory console Todo app into a secure, multi-user, full-stack web application using strict Spec-Driven Development. Every decision and implementation must serve this transformation goal while maintaining the integrity and quality established in Phase I.

### II. Specification-First (NON-NEGOTIABLE)
All backend and frontend code must be generated exclusively from specifications. Manual coding or ad-hoc changes are strictly forbidden. Every feature, API endpoint, database schema, and UI component must originate from approved specification documents following the Spec-Kit conventions.

### III. Test-Driven Development (NON-NEGOTIABLE)
TDD mandatory for all implementation:
- Tests written first → User approved → Tests fail → Then implement
- Red-Green-Refactor cycle strictly enforced
- Backend: pytest with coverage requirements
- Frontend: Jest/React Testing Library for components
- Integration tests for API contracts and user flows
- Database tests for query correctness and user isolation

### IV. Security-First Architecture
Security is not optional and must be enforced at every layer:
- JWT must be verified on every API request (no exceptions)
- User ID from token must match URL user_id parameters
- Unauthorized requests must return HTTP 401
- Cross-user data access is prohibited at the database query level
- Environment variables must be used for all secrets and database URLs
- No credentials or secrets in code or configuration files

## Architecture Principles

### Technology Stack
- **Frontend**: Next.js App Router (server-first rendering)
- **Backend**: FastAPI with SQLModel ORM
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens
- **API Protocol**: Stateless REST with JSON payloads
- **Project Structure**: Monorepo using Spec-Kit conventions

### Separation of Concerns
- Frontend and backend must share no runtime state
- Strict separation of frontend, backend, specs, and configuration directories
- Frontend communicates with backend exclusively via REST API
- Backend owns all business logic and data access
- Frontend owns presentation and user interaction only

### Data Persistence
- All task data must be persisted in Neon Serverless PostgreSQL
- No in-memory state for production data
- Database migrations must be versioned and tracked
- Task ownership must be enforced at the database query level

### User Isolation (NON-NEGOTIABLE)
- Every task must belong to exactly one user
- User ID must be extracted from validated JWT token
- Database queries must filter by user_id automatically
- API endpoints must verify user ownership before operations
- No shared or public tasks allowed

## Security Rules

### Authentication & Authorization
- JWT tokens required for all API requests (no guest access)
- Token validation happens before any business logic
- Token must contain valid user_id claim
- Expired or invalid tokens must be rejected immediately

### Request Validation
- User ID from JWT must match user_id in URL/payload
- Cross-user operations return HTTP 401 (not 404)
- Input validation must occur before database queries
- SQL injection prevention via parameterized queries only

### Environment Security
- `.env` files for local development (gitignored)
- Environment variables for production secrets
- No hardcoded database URLs or API keys
- Separate environments for dev, test, production

## Project Organization

### Monorepo Structure
```
phase-2/
├── .specify/           # Spec-Kit templates and scripts
│   ├── memory/         # Constitution and memory
│   └── templates/      # Spec, plan, tasks templates
├── specs/              # Feature specifications
│   └── <feature>/      # Per-feature spec.md, plan.md, tasks.md
├── history/            # Historical records
│   ├── prompts/        # Prompt History Records (PHRs)
│   └── adr/            # Architecture Decision Records
├── backend/            # FastAPI application
├── frontend/           # Next.js application
└── .env.example        # Environment template
```

### Spec-Driven Workflow
1. Create feature specification (`/sp.specify`)
2. Generate architectural plan (`/sp.plan`)
3. Generate testable tasks (`/sp.tasks`)
4. Implement with TDD (`/sp.implement`)
5. Document decisions as ADRs (`/sp.adr`)
6. Record prompts as PHRs (automatic)

## Quality Standards

### Code Quality
- Type hints required for all Python functions (backend)
- TypeScript strict mode for all frontend code
- No `any` types unless explicitly justified in ADR
- Linting must pass (Ruff for Python, ESLint for TypeScript)
- Code formatting automated (Black/Ruff for Python, Prettier for TypeScript)

### Testing Requirements
- Minimum 80% code coverage for backend
- All API endpoints must have integration tests
- Frontend components must have unit tests
- End-to-end tests for critical user flows
- Security tests for authentication and authorization

### Documentation
- API endpoints documented with OpenAPI/Swagger
- Database schema documented with ER diagrams
- README with setup and run instructions
- ADRs for all significant architectural decisions

## Governance

### Constitution Authority
- This constitution supersedes all other development practices
- All code reviews must verify compliance with constitutional principles
- Violations must be corrected before merge
- Amendments require documented rationale and version increment

### Amendment Process
1. Propose amendment with justification
2. Document impact on existing code and specs
3. Update constitution with version bump (semantic versioning)
4. Propagate changes to dependent templates
5. Create ADR documenting the amendment decision

### Version Control
- Constitution versioning follows semantic versioning:
  - MAJOR: Backward incompatible principle changes
  - MINOR: New principles or major expansions
  - PATCH: Clarifications, wording, typo fixes
- All amendments must update `LAST_AMENDED_DATE`
- Version history tracked via git commits

### Compliance Review
- All PRs must pass constitutional compliance checks
- Spec-first violations are grounds for immediate rejection
- Security violations require immediate remediation
- Test coverage below threshold blocks merge

**Version**: 1.0.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-08
