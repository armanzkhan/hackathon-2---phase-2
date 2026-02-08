# Full-Stack Todo Application

A secure, multi-user todo application built with Next.js, FastAPI, and PostgreSQL.

## 🚀 Features

- ✅ User authentication (JWT-based)
- ✅ Create, read, update, and delete tasks
- ✅ Filter tasks by completion status
- ✅ User isolation (users can only access their own tasks)
- ✅ Responsive UI with Tailwind CSS
- ✅ Comprehensive test coverage

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Testing**: Jest, React Testing Library, Playwright

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **ORM**: SQLModel
- **Database**: PostgreSQL (Neon)
- **Authentication**: JWT with bcrypt
- **Testing**: pytest

## 📁 Project Structure

```
phase-2/
├── frontend/              # Next.js application
│   ├── src/
│   │   ├── app/          # Next.js App Router pages
│   │   ├── components/   # React components
│   │   └── lib/          # Utilities and API client
│   ├── tests/            # Frontend tests
│   └── vercel.json       # Vercel deployment config
│
├── backend/              # FastAPI application
│   ├── src/
│   │   ├── routers/      # API endpoints
│   │   ├── services/     # Business logic
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── middleware/   # JWT authentication
│   ├── tests/            # Backend tests
│   ├── api/              # Vercel serverless entry point
│   └── vercel.json       # Vercel deployment config
│
└── specs/                # Project specifications
```

## 🏃‍♂️ Local Development

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL database (or Neon account)

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Run development server
uvicorn src.main:app --reload
# API available at http://localhost:8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local
# Edit .env.local with your API URL

# Run development server
npm run dev
# App available at http://localhost:3000
```

### Running Tests

**Backend:**
```bash
cd backend
pytest                    # Run all tests
pytest --cov=src         # Run with coverage
```

**Frontend:**
```bash
cd frontend
npm test                 # Run unit tests
npm run test:e2e        # Run E2E tests
```

## 🌐 Deployment

This application is configured for deployment on Vercel.

**See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.**

### Quick Deploy

1. **Set up Neon Database**: Create a PostgreSQL database at [neon.tech](https://neon.tech)
2. **Deploy Backend**: Import to Vercel, set root directory to `backend`, add environment variables
3. **Deploy Frontend**: Import to Vercel, set root directory to `frontend`, add environment variables
4. **Update CORS**: Add frontend URL to backend's `CORS_ORIGINS`

## 🔐 Environment Variables

### Backend
```bash
DATABASE_URL=postgresql://user:password@host:5432/database
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
```

### Frontend
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_SECRET=same-as-backend
```

## 📝 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/login` - Login and get JWT token

### Tasks (Require JWT Authentication)
- `GET /api/{user_id}/tasks` - Get all tasks (with optional `?completed=true/false` filter)
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task

## 🔒 Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- User isolation at database level
- CORS protection
- User ID verification (403 Forbidden on mismatch)
- SQL injection protection (SQLModel/SQLAlchemy)

## 📊 Testing Coverage

- **Backend**: 80%+ code coverage with pytest
- **Frontend**: 70%+ code coverage with Jest
- E2E tests with Playwright

## 🤝 Contributing

This is a Phase II implementation for a hackathon project. For development:

1. Follow the test-driven development (TDD) workflow
2. Ensure all tests pass before committing
3. Follow the existing code structure and patterns
4. Add tests for new features

## 📄 License

This project is part of a hackathon submission.

## 🙏 Acknowledgments

- Built with [Next.js](https://nextjs.org/)
- Backend powered by [FastAPI](https://fastapi.tiangolo.com/)
- Database from [Neon](https://neon.tech/)
- Deployed on [Vercel](https://vercel.com/)
