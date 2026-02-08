# Research Document: Full-Stack Todo Web Application

**Feature**: 002-fullstack-todo-app
**Date**: 2026-02-08
**Status**: Complete

## Purpose

This document captures research findings and technology decisions made during Phase 0 planning. All "NEEDS CLARIFICATION" items from Technical Context have been resolved through research and documented below.

## Research Areas

### 1. Better Auth Integration with FastAPI Backend

**Question**: How to integrate Better Auth (Next.js-centric) with a separate FastAPI backend?

**Decision**: Use Better Auth for frontend authentication only; FastAPI backend verifies JWT tokens independently

**Rationale**:
- Better Auth is designed for Next.js and handles user authentication UI/UX
- Better Auth issues JWT tokens that can be verified by any backend with the shared secret
- FastAPI backend implements standalone JWT verification middleware using PyJWT
- This approach maintains frontend/backend separation while leveraging Better Auth's frontend features

**Alternatives Considered**:
1. **Better Auth for full-stack** - Rejected: Better Auth is Next.js-specific, doesn't integrate directly with FastAPI
2. **Custom auth implementation** - Rejected: Reinventing the wheel; Better Auth provides battle-tested UI components and flows
3. **Auth0/Supabase Auth** - Rejected: Better Auth is simpler for this use case and meets all requirements

**Implementation Pattern**:
```python
# FastAPI middleware (pseudo-code)
import jwt
from fastapi import Request, HTTPException

async def verify_jwt_middleware(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
        request.state.user_id = payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**References**:
- Better Auth documentation: https://better-auth.com/docs
- PyJWT documentation: https://pyjwt.readthedocs.io/
- FastAPI middleware guide: https://fastapi.tiangolo.com/tutorial/middleware/

---

### 2. JWT Token Flow Architecture

**Question**: How does the JWT flow between Next.js frontend and FastAPI backend?

**Decision**: Standard bearer token flow with client-side token storage

**Flow**:
1. User registers/logs in via Better Auth (Next.js frontend)
2. Better Auth issues JWT token containing user_id claim
3. Frontend stores JWT token (httpOnly cookie or secure localStorage)
4. Frontend API client automatically attaches JWT to all requests: `Authorization: Bearer <token>`
5. Backend JWT middleware verifies token signature using BETTER_AUTH_SECRET
6. Backend extracts user_id from verified token and attaches to request context
7. Backend API handlers use authenticated user_id for all database queries

**Rationale**:
- Industry-standard approach used by major applications
- Stateless (no server-side session storage required)
- Secure when combined with HTTPS and proper secret management
- Scalable across multiple backend instances

**Alternatives Considered**:
1. **Session-based auth** - Rejected: Requires shared session store (Redis), adds complexity, less scalable
2. **OAuth2 with refresh tokens** - Deferred: Current scope doesn't require long-lived sessions; can add later if needed
3. **API keys** - Rejected: Less secure, no user context in token

**Security Considerations**:
- JWT tokens transmitted only over HTTPS in production
- BETTER_AUTH_SECRET must be strong (minimum 32 characters, random)
- Token expiration time set appropriately (e.g., 24 hours)
- Frontend handles 401 responses by redirecting to login
- No sensitive user data in JWT payload (only user_id)

---

### 3. SQLModel Database Schema for User Isolation

**Question**: How to design database schema to enforce user isolation at query level?

**Decision**: Every task has user_id foreign key; all queries filter by authenticated user_id

**Schema Design**:
```python
# SQLModel schema (pseudo-code)
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)  # Better Auth user ID
    email: str = Field(unique=True, index=True)
    # Other fields managed by Better Auth
    tasks: list["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)  # CRITICAL: Indexed for performance
    title: str = Field(min_length=1, max_length=500)
    description: str | None = Field(default=None)
    completed: bool = Field(default=False, index=True)  # Indexed for filtering
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="tasks")
```

**Rationale**:
- Foreign key constraint enforces referential integrity
- Index on user_id enables fast filtering (required for <1 second query performance)
- Index on completed enables efficient filtering by status
- SQLModel provides automatic validation and type safety
- Relationship defines clear ownership model

**Enforcement Pattern**:
```python
# All queries MUST filter by authenticated user_id
def get_user_tasks(user_id: str, session: Session) -> list[Task]:
    return session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()

def get_task_by_id(task_id: int, user_id: str, session: Session) -> Task:
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return task
```

**Alternatives Considered**:
1. **Row-level security in PostgreSQL** - Considered but deferred: Adds database complexity; application-level enforcement is sufficient and more explicit
2. **Separate database per user** - Rejected: Massive operational overhead, not scalable
3. **Soft delete with user_id** - Deferred: Hard delete is simpler; can add soft delete later if needed

---

### 4. Neon PostgreSQL Connection Pooling

**Question**: How to configure connection pooling for Neon Serverless PostgreSQL?

**Decision**: Use SQLModel's built-in connection pooling with appropriate pool size limits

**Configuration**:
```python
# Database configuration (pseudo-code)
from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,          # Maximum connections in pool
    max_overflow=20,       # Additional connections if pool exhausted
    pool_timeout=30,       # Wait time for available connection
    pool_recycle=3600,     # Recycle connections after 1 hour
    echo=False,            # Set to True for SQL logging in development
)
```

**Rationale**:
- Neon has connection limits per project tier (typically 100 connections for free tier)
- Pool size of 10 + overflow of 20 = max 30 connections per backend instance
- Allows scaling to 3 backend instances without exceeding limits
- Connection recycling prevents stale connections
- QueuePool is production-ready and battle-tested

**Alternatives Considered**:
1. **No pooling** - Rejected: Poor performance, connection overhead for each request
2. **PgBouncer external pooler** - Deferred: Adds operational complexity; built-in pooling sufficient for current scale
3. **Async SQLAlchemy** - Deferred: FastAPI can use async, but SQLModel sync is simpler for MVP; can optimize later

**Monitoring**:
- Log connection pool metrics in production (pool size, overflow count)
- Alert if pool exhaustion occurs frequently (indicates need for scaling)

---

### 5. Next.js App Router Authentication Patterns

**Question**: How to implement authentication routing and protected routes in Next.js App Router?

**Decision**: Use Next.js middleware for route protection + client-side API hooks for auth state

**Pattern**:
```typescript
// middleware.ts (pseudo-code)
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth_token')
  const { pathname } = request.nextUrl

  // Public routes
  if (pathname === '/login' || pathname === '/signup') {
    return NextResponse.next()
  }

  // Protected routes require token
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}
```

**Client-Side Pattern**:
```typescript
// lib/api-client.ts (pseudo-code)
import axios from 'axios'

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
})

// Automatically attach JWT to all requests
apiClient.interceptors.request.use((config) => {
  const token = getToken() // from cookie or localStorage
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle 401 responses globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - redirect to login
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
```

**Rationale**:
- Middleware runs on server-side, protects routes before rendering
- Interceptors centralize JWT attachment and error handling
- No need to manually add auth headers to every API call
- Automatic redirect on 401 improves UX

**Alternatives Considered**:
1. **Client-side only protection** - Rejected: Weaker security, flash of unauthorized content
2. **Server Components for all auth** - Considered: Good pattern but adds complexity for MVP; can migrate later
3. **NextAuth.js** - Rejected: Better Auth is sufficient and simpler for this use case

---

### 6. API Contract Design (REST Endpoint Structure)

**Question**: What should the REST API endpoint structure be for task operations?

**Decision**: RESTful design with user_id in path for explicitness and validation

**Endpoints**:
```
POST   /api/auth/signup           - Register new user
POST   /api/auth/login            - Login and receive JWT
POST   /api/auth/logout           - Logout (client-side token removal)

GET    /api/{user_id}/tasks       - Get all tasks for user
POST   /api/{user_id}/tasks       - Create new task for user
GET    /api/{user_id}/tasks/{id}  - Get specific task
PUT    /api/{user_id}/tasks/{id}  - Update specific task
DELETE /api/{user_id}/tasks/{id}  - Delete specific task

Query parameters for GET /api/{user_id}/tasks:
  ?completed=true|false  - Filter by completion status
```

**Rationale**:
- User_id in path makes ownership explicit and enables middleware validation
- Standard HTTP verbs (GET, POST, PUT, DELETE) for CRUD operations
- Query parameters for filtering (completed status)
- RESTful design is widely understood and well-supported by tooling
- Path structure enables easy middleware check: JWT user_id must match path user_id

**Validation**:
```python
# Middleware validation (pseudo-code)
def validate_user_id_match(request: Request, path_user_id: str):
    authenticated_user_id = request.state.user_id  # From JWT
    if authenticated_user_id != path_user_id:
        raise HTTPException(status_code=403, detail="User ID mismatch")
```

**Alternatives Considered**:
1. **User_id from token only** (not in path) - Rejected: Less explicit, harder to validate at middleware level
2. **GraphQL** - Rejected: Overkill for simple CRUD; REST is simpler for this use case
3. **Nested resources** `/api/users/{user_id}/tasks` - Rejected: User_id is always from JWT, no need for users resource

---

### 7. Testing Strategy (Unit, Integration, E2E)

**Question**: What testing layers are needed to ensure quality and security?

**Decision**: Three-layer testing strategy with focus on integration and security tests

**Testing Layers**:

1. **Unit Tests** (Backend)
   - Test individual functions in isolation
   - Mock database and external dependencies
   - Tools: pytest with unittest.mock
   - Coverage target: 80%+ for services and routers

2. **Integration Tests** (Backend)
   - Test API endpoints end-to-end with test database
   - Verify JWT authentication and authorization
   - Test user isolation (critical security requirement)
   - Tools: pytest with TestClient, SQLite in-memory for speed
   - Key test cases:
     - User cannot access another user's tasks (403 Forbidden)
     - Missing JWT returns 401 Unauthorized
     - Invalid JWT returns 401 Unauthorized
     - User_id mismatch returns 403 Forbidden

3. **Component Tests** (Frontend)
   - Test React components in isolation
   - Mock API responses
   - Tools: Jest + React Testing Library
   - Focus on user interactions and error handling

4. **End-to-End Tests** (Full Stack)
   - Test complete user flows in real browser
   - Tools: Playwright
   - Key flows:
     - User registration → login → create task → view task → update task → delete task
     - Authentication failure scenarios
     - Cross-user access prevention

**Example Integration Test**:
```python
def test_user_cannot_access_other_user_tasks(client, auth_headers_user1, auth_headers_user2):
    # User 1 creates a task
    response = client.post(
        "/api/user1/tasks",
        json={"title": "User 1 Task"},
        headers=auth_headers_user1
    )
    task_id = response.json()["id"]

    # User 2 tries to access User 1's task
    response = client.get(
        f"/api/user1/tasks/{task_id}",
        headers=auth_headers_user2  # User 2's JWT
    )

    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]
```

**Rationale**:
- Integration tests catch security vulnerabilities (user isolation)
- E2E tests validate real user experience
- Component tests ensure UI handles edge cases
- Three layers provide comprehensive coverage

**Alternatives Considered**:
1. **Manual testing only** - Rejected: Not scalable, misses edge cases, no regression protection
2. **E2E tests only** - Rejected: Slow, fragile, poor feedback loop
3. **Unit tests only** - Rejected: Misses integration issues and security vulnerabilities

---

### 8. Error Handling and HTTP Status Code Conventions

**Question**: What HTTP status codes and error response format should be used?

**Decision**: Standard HTTP status codes with consistent JSON error format

**Status Codes**:
- **200 OK**: Successful GET, PUT operations
- **201 Created**: Successful POST (task created)
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Validation errors (empty title, invalid data)
- **401 Unauthorized**: Missing, invalid, or expired JWT token
- **403 Forbidden**: Valid JWT but user_id mismatch (cross-user access attempt)
- **404 Not Found**: Resource doesn't exist (task ID not found)
- **500 Internal Server Error**: Unexpected server errors (database connection failure)

**Error Response Format**:
```json
{
  "detail": "Human-readable error message",
  "error_code": "OPTIONAL_MACHINE_READABLE_CODE",
  "field_errors": {
    "title": "Title cannot be empty"
  }
}
```

**Rationale**:
- Standard HTTP codes are widely understood
- Clear distinction between authentication (401) and authorization (403) errors
- Consistent JSON format enables frontend error handling
- Field-level errors help with form validation UX

**Frontend Error Handling**:
```typescript
// Error handling pattern (pseudo-code)
try {
  await apiClient.post('/api/user1/tasks', taskData)
} catch (error) {
  if (error.response?.status === 400) {
    // Show validation errors
    setFieldErrors(error.response.data.field_errors)
  } else if (error.response?.status === 401) {
    // Redirect to login (handled by interceptor)
  } else if (error.response?.status === 403) {
    // Show access denied message
    showError("You don't have permission to perform this action")
  } else {
    // Generic error
    showError("Something went wrong. Please try again.")
  }
}
```

**Alternatives Considered**:
1. **Custom error codes** - Deferred: HTTP codes are sufficient for MVP; can add custom codes later if needed
2. **Always return 200 with error in body** - Rejected: Anti-pattern, breaks HTTP semantics
3. **Detailed stack traces in errors** - Rejected: Security risk, leaks implementation details

---

## Environment Variable Management

**Decision**: Use .env files for local development, environment variables in production

**Required Variables**:
```bash
# Backend (.env)
DATABASE_URL=postgresql://user:password@host:5432/dbname
BETTER_AUTH_SECRET=<strong-random-secret-32-chars-min>
CORS_ORIGINS=http://localhost:3000,https://app.example.com
ENVIRONMENT=development|production

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

**Security Rules**:
- Never commit .env files to git (add to .gitignore)
- Provide .env.example files with dummy values as templates
- Use strong random secrets for BETTER_AUTH_SECRET (minimum 32 characters)
- Rotate secrets periodically in production
- Use separate secrets for development and production environments

**Rationale**:
- Environment variables are the standard for 12-factor apps
- Prevents hardcoding secrets in source code
- Enables different configurations for dev/staging/prod
- .env files simplify local development setup

---

## CORS Configuration

**Decision**: Configure CORS in FastAPI backend to allow frontend origin

**Configuration**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

**Rationale**:
- Required for browser to allow cross-origin requests (frontend → backend)
- allow_credentials=True enables sending cookies and Authorization headers
- Environment variable allows different origins for dev/prod
- Explicitly list allowed methods and headers for security

**Development**: `CORS_ORIGINS=http://localhost:3000`
**Production**: `CORS_ORIGINS=https://app.example.com,https://www.example.com`

---

## Database Migration Strategy

**Decision**: Use Alembic (SQLModel's migration tool) for production migrations

**Approach**:
1. **Development**: SQLModel create_all() for rapid iteration
2. **Production**: Alembic migrations for versioned schema changes

**Rationale**:
- SQLModel can auto-create tables in development (create_all())
- Alembic provides migration versioning and rollback for production
- Avoids manual SQL scripts
- Migrations tracked in git for audit trail

**Migration Workflow**:
```bash
# Generate migration from model changes
alembic revision --autogenerate -m "Add tasks table"

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

**Deferred**: Full Alembic setup can be done during implementation phase; document in quickstart.md

---

## Summary of Resolutions

| Original Question | Resolution | Document Section |
|-------------------|------------|------------------|
| Better Auth + FastAPI integration | JWT verification in FastAPI middleware | Section 1 |
| JWT token flow | Standard bearer token with client-side storage | Section 2 |
| User isolation database design | user_id FK + indexed queries | Section 3 |
| Neon PostgreSQL connection pooling | SQLModel QueuePool with size limits | Section 4 |
| Next.js authentication routing | Middleware + API interceptors | Section 5 |
| API endpoint structure | RESTful with user_id in path | Section 6 |
| Testing strategy | 3-layer: unit, integration, E2E | Section 7 |
| Error handling conventions | Standard HTTP codes + JSON format | Section 8 |

All "NEEDS CLARIFICATION" items from Technical Context have been resolved. Implementation can proceed with confidence.

---

**Research Status**: ✅ Complete
**Next Phase**: Phase 1 - Design & Contracts (data-model.md, api.yaml, quickstart.md)
