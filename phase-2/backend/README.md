# Todo Backend - FastAPI Application

Backend API for the Full-Stack Todo Web Application built with FastAPI, SQLModel, and PostgreSQL.

## Features

- **Authentication**: JWT-based authentication with Better Auth integration
- **Task Management**: CRUD operations for todo tasks with user isolation
- **Security**: User-level data isolation, JWT verification on all endpoints
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM
- **Testing**: pytest with 80%+ code coverage requirement

## Technology Stack

- **Framework**: FastAPI 0.109+
- **ORM**: SQLModel 0.0.14+
- **Database**: PostgreSQL (Neon Serverless)
- **Authentication**: JWT tokens with PyJWT 2.8+
- **Testing**: pytest 7.4+ with coverage
- **Python**: 3.11+

## Setup

### Prerequisites

- Python 3.11 or higher
- Poetry (Python package manager)
- PostgreSQL database (or Neon account)

### Installation

1. **Install dependencies**:
   ```bash
   poetry install
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and secrets
   ```

3. **Initialize database**:
   ```bash
   poetry run python -c "from src.database import init_db; init_db()"
   ```

4. **Run development server**:
   ```bash
   poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at: http://localhost:8000

5. **View API documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Testing

### Run all tests:
```bash
poetry run pytest
```

### Run with coverage:
```bash
poetry run pytest --cov=src --cov-report=html
```

### Run specific test file:
```bash
poetry run pytest tests/test_auth.py
```

### View coverage report:
```bash
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

## Project Structure

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
│   │   ├── auth.py          # Auth DTOs
│   │   └── task.py          # Task DTOs
│   └── services/            # Business logic layer
│       └── task_service.py  # Task operations
├── tests/                   # Test suite
│   ├── conftest.py          # Pytest fixtures
│   ├── test_auth.py         # Authentication tests
│   ├── test_tasks.py        # Task CRUD tests
│   └── test_user_isolation.py # Security tests
├── .env.example             # Environment template
├── pyproject.toml           # Poetry dependencies
├── pytest.ini               # Pytest configuration
└── README.md                # This file
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login and receive JWT token

### Tasks (JWT required)
- `GET /api/{user_id}/tasks` - Get all user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{task_id}` - Get specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task

### Query Parameters
- `GET /api/{user_id}/tasks?completed=true` - Filter by completion status

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | Yes | JWT signing secret (min 32 chars) |
| `CORS_ORIGINS` | Yes | Allowed frontend origins (comma-separated) |
| `ENVIRONMENT` | Yes | `development` or `production` |

## Security

- All task endpoints require valid JWT authentication
- User isolation enforced at database query level
- Cross-user data access returns 403 Forbidden
- Passwords are hashed with bcrypt
- Secrets managed via environment variables

## Development

### Code Quality
```bash
# Run linter
poetry run ruff check src/

# Format code
poetry run ruff format src/
```

### Database Migrations
```bash
# Generate migration (if using Alembic)
poetry run alembic revision --autogenerate -m "Description"

# Apply migrations
poetry run alembic upgrade head

# Rollback migration
poetry run alembic downgrade -1
```

## Troubleshooting

### Database Connection Errors
- Verify `DATABASE_URL` is correct in `.env`
- Ensure PostgreSQL server is running
- Check network connectivity to Neon

### Import Errors
- Run `poetry install` to ensure all dependencies are installed
- Verify you're using Python 3.11+

### Test Failures
- Ensure test database is configured
- Check that all fixtures in `conftest.py` are working
- Run tests with `-v` flag for verbose output

## License

MIT License - See LICENSE file for details
