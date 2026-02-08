# Todo Frontend - Next.js Application

Frontend web application for the Full-Stack Todo Web Application built with Next.js, TypeScript, and Better Auth.

## Features

- **Authentication**: User signup and login with Better Auth
- **Task Management**: View, create, update, and delete todo tasks
- **Real-time Updates**: Task list updates after operations
- **Responsive Design**: Mobile-friendly UI
- **Error Handling**: Global error handling for 401/403 responses

## Technology Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript 5+
- **UI Library**: React 18+
- **Authentication**: Better Auth
- **HTTP Client**: Axios
- **Testing**: Jest + React Testing Library + Playwright
- **Node**: 18+

## Setup

### Prerequisites

- Node.js 18 or higher
- npm or yarn
- Backend API running (see backend/README.md)

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your backend API URL
   ```

3. **Run development server**:
   ```bash
   npm run dev
   ```

   The application will be available at: http://localhost:3000

4. **Build for production**:
   ```bash
   npm run build
   npm start
   ```

## Testing

### Run unit and component tests:
```bash
npm test
```

### Run tests in watch mode:
```bash
npm run test:watch
```

### Run E2E tests:
```bash
npm run test:e2e
```

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home page
│   │   ├── login/           # Login page
│   │   ├── signup/          # Signup page
│   │   └── tasks/           # Task management pages
│   ├── components/          # React components
│   │   ├── AuthForm.tsx     # Login/signup form
│   │   ├── TaskForm.tsx     # Create/edit task form
│   │   ├── TaskList.tsx     # Task list display
│   │   └── TaskItem.tsx     # Individual task component
│   ├── lib/                 # Utilities and services
│   │   ├── auth.ts          # Better Auth configuration
│   │   ├── api-client.ts    # Axios instance with JWT interceptor
│   │   └── types.ts         # TypeScript interfaces
│   └── middleware.ts        # Next.js middleware for route protection
├── tests/
│   ├── components/          # Component unit tests
│   └── e2e/                 # Playwright E2E tests
├── .env.local.example       # Environment template
├── next.config.js           # Next.js configuration
├── tsconfig.json            # TypeScript configuration
├── package.json             # Dependencies
└── README.md                # This file
```

## Pages and Routes

### Public Routes
- `/login` - User login page
- `/signup` - User registration page

### Protected Routes (require authentication)
- `/` - Home page (redirects to /tasks if authenticated, else /login)
- `/tasks` - Task list page
- `/tasks/[id]` - Task detail and edit page

## Components

### AuthForm
Handles user signup and login with email/password.

**Props**:
- `mode: 'login' | 'signup'` - Form mode

**Features**:
- Email and password validation
- Error display
- Loading states
- Redirect after successful authentication

### TaskList
Displays list of user's tasks.

**Features**:
- Fetches tasks from API
- Handles loading and error states
- Shows empty state when no tasks
- Filters by completion status

### TaskItem
Displays individual task with actions.

**Props**:
- `task: Task` - Task object

**Features**:
- Completion toggle
- Edit and delete buttons
- Timestamps display

### TaskForm
Form for creating or editing tasks.

**Props**:
- `mode: 'create' | 'edit'` - Form mode
- `initialData?: Task` - Initial task data for edit mode

**Features**:
- Title input (required)
- Description textarea (optional)
- Validation
- Submit handling

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Yes | Backend API base URL |
| `NEXT_PUBLIC_BETTER_AUTH_URL` | Yes | Better Auth callback URL |

## API Client

The app uses Axios with request/response interceptors:

### Request Interceptor
- Automatically attaches JWT token to all requests
- Header: `Authorization: Bearer <token>`

### Response Interceptor
- Handles 401 Unauthorized: Redirects to login
- Handles 403 Forbidden: Shows access denied message
- Provides consistent error handling

## Authentication Flow

1. User navigates to `/signup` or `/login`
2. User submits credentials via `AuthForm`
3. Frontend calls backend `/api/auth/signup` or `/api/auth/login`
4. Backend returns JWT token
5. Token stored in localStorage/cookies
6. API client attaches token to all subsequent requests
7. Protected routes accessible

## Development

### Code Quality
```bash
# Run ESLint
npm run lint

# Fix linting issues
npm run lint -- --fix
```

### TypeScript
```bash
# Type check
npx tsc --noEmit
```

## Deployment

### Vercel (Recommended)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

### Docker
```bash
# Build
docker build -t todo-frontend .

# Run
docker run -p 3000:3000 --env-file .env.local todo-frontend
```

## Troubleshooting

### API Connection Errors
- Verify `NEXT_PUBLIC_API_URL` is correct in `.env.local`
- Ensure backend server is running
- Check CORS configuration on backend

### Authentication Issues
- Clear browser localStorage/cookies
- Verify JWT token is being sent in requests
- Check backend auth configuration

### Build Errors
- Delete `.next` directory and rebuild
- Clear `node_modules` and reinstall dependencies
- Verify all environment variables are set

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

MIT License - See LICENSE file for details
