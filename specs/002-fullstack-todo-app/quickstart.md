# Quickstart Guide: Full-Stack Todo Web Application

**Feature**: 002-fullstack-todo-app
**Date**: 2026-02-08
**Status**: Ready for Implementation

## Purpose

This guide provides step-by-step instructions to set up and run the Full-Stack Todo Web Application locally for development and testing.

## Prerequisites

### Required Software

1. **Python 3.11+**
   - Verify: `python --version` or `python3 --version`
   - Download: https://www.python.org/downloads/

2. **Node.js 18+ and npm**
   - Verify: `node --version` and `npm --version`
   - Download: https://nodejs.org/

3. **PostgreSQL** (or use Neon cloud database)
   - Option A: Install PostgreSQL locally (https://www.postgresql.org/download/)
   - Option B: Use Neon Serverless PostgreSQL (https://neon.tech/) (Recommended)

4. **Git**
   - Verify: `git --version`
   - Download: https://git-scm.com/downloads

5. **Poetry** (Python dependency management, recommended)
   - Install: `pip install poetry`
   - Verify: `poetry --version`
   - Alternative: Use pip with requirements.txt

### Optional Tools

- **Docker** (for containerized deployment): https://www.docker.com/
- **Postman** or **Insomnia** (for API testing): https://www.postman.com/
- **VS Code** or **PyCharm** (recommended IDEs)

---

## Quick Start (5 Minutes)

### 1. Clone Repository

```bash
git clone <repository-url>
cd phase-2
git checkout 002-fullstack-todo-app
```

### 2. Set Up Neon PostgreSQL Database

1. Go to https://neon.tech/ and create a free account
2. Create a new project: "todo-app"
3. Copy the connection string (looks like: `postgresql://user:password@host/dbname`)
4. Save it for the next step

### 3. Configure Backend Environment

```bash
cd backend

# Create .env file from template
cp .env.example .env

# Edit .env with your database URL and secret
# Use a text editor or:
nano .env
```

**Required .env variables**:
```bash
DATABASE_URL=postgresql://user:password@host:5432/dbname  # From Neon
BETTER_AUTH_SECRET=your-super-secret-key-minimum-32-characters-long
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
```

**Generate strong secret**:
```bash
# On Linux/Mac:
openssl rand -base64 32

# On Windows (PowerShell):
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})
```

### 4. Install Backend Dependencies

**Option A: Using Poetry (Recommended)**
```bash
cd backend
poetry install
```

**Option B: Using pip**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Initialize Database

```bash
cd backend

# Option A: Using Poetry
poetry run python -c "from src.database import init_db; init_db()"

# Option B: Using activated venv
python -c "from src.database import init_db; init_db()"
```

### 6. Run Backend Server

```bash
cd backend

# Option A: Using Poetry
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Option B: Using activated venv
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend running at: http://localhost:8000
API docs at: http://localhost:8000/docs (Swagger UI)

### 7. Configure Frontend Environment

Open a **new terminal** window:

```bash
cd frontend

# Create .env.local file from template
cp .env.local.example .env.local

# Edit .env.local
nano .env.local
```

**Required .env.local variables**:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

### 8. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 9. Run Frontend Development Server

```bash
cd frontend
npm run dev
```

Frontend running at: http://localhost:3000

### 10. Test the Application

1. Open browser: http://localhost:3000
2. Click "Sign Up" and create an account
3. Login with your credentials
4. Create a new task
5. View, update, and delete tasks

---

## Detailed Setup Instructions

### Backend Setup (FastAPI + SQLModel)

#### Directory Structure
```
backend/
├── src/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment configuration
│   ├── database.py          # Database connection and init
│   ├── models/              # SQLModel database models
│   │   ├── user.py          # User model
│   │   └── task.py          # Task model
│   ├── middleware/          # Request middleware
│   │   └── auth.py          # JWT verification
│   ├── routers/             # API route handlers
│   │   ├── auth.py          # Authentication endpoints
│   │   └── tasks.py         # Task CRUD endpoints
│   ├── schemas/             # Pydantic request/response models
│   │   └── task.py          # Task DTOs
│   └── services/            # Business logic
│       └── task_service.py  # Task operations
├── tests/                   # Test suite
├── .env                     # Environment variables (git-ignored)
├── .env.example             # Environment template
├── pyproject.toml           # Poetry dependencies
└── README.md                # Backend documentation
```

#### Dependencies (pyproject.toml)

```toml
[tool.poetry]
name = "todo-backend"
version = "1.0.0"
description = "FastAPI backend for Full-Stack Todo App"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.109.0"
uvicorn = {extras = ["standard"], version = "^0.27.0"}
sqlmodel = "^0.0.14"
psycopg2-binary = "^2.9.9"  # PostgreSQL adapter
pyjwt = "^2.8.0"
python-dotenv = "^1.0.0"
pydantic-settings = "^2.1.0"

[tool.poetry.dev-dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
pytest-cov = "^4.1.0"
httpx = "^0.25.0"  # For TestClient

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

#### Running Tests

```bash
cd backend

# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=html

# Run specific test file
poetry run pytest tests/test_tasks.py

# Run specific test
poetry run pytest tests/test_tasks.py::test_user_cannot_access_other_user_tasks
```

#### Database Migrations (Alembic)

```bash
cd backend

# Initialize Alembic (first time only)
poetry run alembic init alembic

# Generate migration from model changes
poetry run alembic revision --autogenerate -m "Create user and task tables"

# Apply migrations
poetry run alembic upgrade head

# Rollback last migration
poetry run alembic downgrade -1

# View migration history
poetry run alembic history
```

---

### Frontend Setup (Next.js + Better Auth)

#### Directory Structure
```
frontend/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home page
│   │   ├── login/page.tsx   # Login page
│   │   ├── signup/page.tsx  # Signup page
│   │   └── tasks/           # Task pages
│   │       ├── page.tsx     # Task list
│   │       └── [id]/page.tsx # Task detail
│   ├── components/          # React components
│   │   ├── TaskList.tsx
│   │   ├── TaskForm.tsx
│   │   └── AuthForm.tsx
│   ├── lib/                 # Utilities
│   │   ├── auth.ts          # Better Auth config
│   │   ├── api-client.ts    # API client with JWT
│   │   └── types.ts         # TypeScript types
│   └── middleware.ts        # Next.js middleware
├── tests/                   # Test suite
├── .env.local               # Environment variables (git-ignored)
├── .env.local.example       # Environment template
├── package.json             # npm dependencies
└── README.md                # Frontend documentation
```

#### Dependencies (package.json)

```json
{
  "name": "todo-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "jest",
    "test:watch": "jest --watch"
  },
  "dependencies": {
    "next": "^14.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "better-auth": "latest",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "typescript": "^5.3.0",
    "eslint": "^8.56.0",
    "eslint-config-next": "^14.1.0",
    "@testing-library/react": "^14.1.0",
    "@testing-library/jest-dom": "^6.1.0",
    "jest": "^29.7.0",
    "jest-environment-jsdom": "^29.7.0"
  }
}
```

#### Running Tests

```bash
cd frontend

# Run all tests
npm test

# Run in watch mode (auto-rerun on file changes)
npm run test:watch

# Run E2E tests (requires Playwright)
npm run test:e2e
```

---

## Common Development Tasks

### 1. Create a New API Endpoint

**Backend** (`backend/src/routers/tasks.py`):
```python
from fastapi import APIRouter, Depends
from src.middleware.auth import get_current_user

router = APIRouter()

@router.get("/api/{user_id}/tasks/summary")
async def get_task_summary(user_id: str, current_user: str = Depends(get_current_user)):
    # Verify user_id matches authenticated user
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Access denied")

    # Implement business logic
    return {"total": 10, "completed": 3}
```

**Update OpenAPI Contract** (`specs/002-fullstack-todo-app/contracts/api.yaml`):
```yaml
/api/{user_id}/tasks/summary:
  get:
    summary: Get task summary
    # ...
```

**Write Tests First** (TDD):
```python
def test_get_task_summary(client, auth_headers):
    response = client.get("/api/user1/tasks/summary", headers=auth_headers)
    assert response.status_code == 200
    assert "total" in response.json()
```

### 2. Add a New React Component

**Component** (`frontend/src/components/TaskSummary.tsx`):
```typescript
import { useState, useEffect } from 'react'
import { apiClient } from '@/lib/api-client'

export function TaskSummary({ userId }: { userId: string }) {
  const [summary, setSummary] = useState({ total: 0, completed: 0 })

  useEffect(() => {
    apiClient.get(`/api/${userId}/tasks/summary`)
      .then(res => setSummary(res.data))
      .catch(err => console.error(err))
  }, [userId])

  return <div>Total: {summary.total}, Completed: {summary.completed}</div>
}
```

**Write Tests First** (TDD):
```typescript
import { render, screen, waitFor } from '@testing-library/react'
import { TaskSummary } from './TaskSummary'

test('displays task summary', async () => {
  render(<TaskSummary userId="user1" />)
  await waitFor(() => {
    expect(screen.getByText(/Total: 10/)).toBeInTheDocument()
  })
})
```

### 3. Run Both Frontend and Backend Simultaneously

**Option A: Two Terminal Windows**
```bash
# Terminal 1: Backend
cd backend && poetry run uvicorn src.main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev
```

**Option B: Using Docker Compose** (after implementation)
```bash
docker-compose up
```

### 4. Debug Authentication Issues

**Check JWT Token**:
```bash
# Decode JWT (use jwt.io or):
python -c "import jwt; print(jwt.decode('YOUR_TOKEN', options={'verify_signature': False}))"
```

**Common Issues**:
1. **401 Unauthorized**: Missing or invalid token
   - Verify token is in Authorization header: `Bearer <token>`
   - Check token hasn't expired
   - Verify BETTER_AUTH_SECRET matches between frontend and backend

2. **403 Forbidden**: User_id mismatch
   - JWT user_id doesn't match URL user_id
   - Verify user is accessing their own resources

3. **CORS Errors**: Frontend can't reach backend
   - Verify CORS_ORIGINS in backend .env includes frontend URL
   - Check backend CORS middleware is configured

---

## Environment Variables Reference

### Backend (.env)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| DATABASE_URL | Yes | Neon PostgreSQL connection string | `postgresql://user:pass@host/db` |
| BETTER_AUTH_SECRET | Yes | JWT signing secret (min 32 chars) | `super-secret-key-123...` |
| CORS_ORIGINS | Yes | Allowed frontend origins (comma-separated) | `http://localhost:3000` |
| ENVIRONMENT | Yes | Deployment environment | `development` or `production` |

### Frontend (.env.local)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| NEXT_PUBLIC_API_URL | Yes | Backend API base URL | `http://localhost:8000` |
| NEXT_PUBLIC_BETTER_AUTH_URL | Yes | Better Auth callback URL | `http://localhost:3000` |

---

## Troubleshooting

### Backend Won't Start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`
- **Solution**: Install dependencies with `poetry install` or `pip install -r requirements.txt`

**Error**: `sqlalchemy.exc.OperationalError: could not connect to server`
- **Solution**: Verify DATABASE_URL is correct and Neon database is accessible

**Error**: `Port 8000 already in use`
- **Solution**: Kill existing process or use different port: `uvicorn src.main:app --port 8001`

### Frontend Won't Start

**Error**: `Cannot find module 'next'`
- **Solution**: Run `npm install` in frontend directory

**Error**: `Network Error` when calling API
- **Solution**: Verify backend is running and NEXT_PUBLIC_API_URL is correct

**Error**: `CORS policy blocked`
- **Solution**: Add frontend URL to CORS_ORIGINS in backend .env

### Database Issues

**Error**: `relation "task" does not exist`
- **Solution**: Run database initialization: `python -c "from src.database import init_db; init_db()"`

**Error**: `Too many connections`
- **Solution**: Check connection pool settings in backend/src/database.py; reduce pool_size if needed

---

## Production Deployment (Future)

### Backend Deployment (Heroku Example)

```bash
# Install Heroku CLI
heroku login

# Create app
heroku create todo-app-backend

# Set environment variables
heroku config:set DATABASE_URL=<neon-url>
heroku config:set BETTER_AUTH_SECRET=<secret>
heroku config:set CORS_ORIGINS=https://your-frontend.com

# Deploy
git push heroku 002-fullstack-todo-app:main
```

### Frontend Deployment (Vercel Example)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel

# Set environment variables in Vercel dashboard
NEXT_PUBLIC_API_URL=https://todo-app-backend.herokuapp.com
```

---

## Next Steps

1. ✅ **Backend Setup Complete** - Backend running at http://localhost:8000
2. ✅ **Frontend Setup Complete** - Frontend running at http://localhost:3000
3. ✅ **Database Initialized** - Tables created in Neon PostgreSQL
4. **Run Tests** - Verify everything works: `poetry run pytest` and `npm test`
5. **Begin Implementation** - Run `/sp.tasks` to generate implementation tasks
6. **Follow TDD** - Write tests first, then implement features

---

**Quickstart Status**: ✅ Complete and ready for development
**Estimated Setup Time**: 15-30 minutes (depending on internet speed and familiarity)
**Next Command**: `/sp.tasks` to generate implementation tasks
