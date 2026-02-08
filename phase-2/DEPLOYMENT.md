# Vercel Deployment Guide

This guide walks you through deploying the Full-Stack Todo Application to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI** (optional): Install with `npm install -g vercel`
3. **PostgreSQL Database**: Set up a Neon database at [neon.tech](https://neon.tech) (free tier available)
4. **GitHub Account**: For connecting your repository to Vercel

## Step 1: Set Up Neon PostgreSQL Database

1. Go to [neon.tech](https://neon.tech) and create a free account
2. Create a new project (e.g., "todo-app-db")
3. Copy the connection string (looks like: `postgresql://user:password@host/database`)
4. Save this for later - you'll need it as `DATABASE_URL`

## Step 2: Deploy Backend to Vercel

### Option A: Via Vercel Dashboard (Recommended)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your Git repository
3. **Framework Preset**: Select "Other"
4. **Root Directory**: Set to `backend`
5. Click "Environment Variables" and add:
   ```
   DATABASE_URL=postgresql://your-neon-connection-string
   BETTER_AUTH_SECRET=your-secret-key-min-32-chars
   CORS_ORIGINS=https://your-frontend.vercel.app
   ENVIRONMENT=production
   ```
6. Click "Deploy"
7. **Save the backend URL** (e.g., `https://your-backend.vercel.app`)

### Option B: Via Vercel CLI

```bash
cd backend
vercel

# Follow prompts, then add environment variables:
vercel env add DATABASE_URL
vercel env add BETTER_AUTH_SECRET
vercel env add CORS_ORIGINS
vercel env add ENVIRONMENT

# Redeploy with environment variables:
vercel --prod
```

## Step 3: Deploy Frontend to Vercel

### Option A: Via Vercel Dashboard

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your Git repository (or create a new project)
3. **Framework Preset**: Next.js will be auto-detected
4. **Root Directory**: Set to `frontend`
5. Click "Environment Variables" and add:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.vercel.app
   NEXT_PUBLIC_BETTER_AUTH_SECRET=same-secret-as-backend
   ```
6. Click "Deploy"

### Option B: Via Vercel CLI

```bash
cd frontend
vercel

# Add environment variables:
vercel env add NEXT_PUBLIC_API_URL
vercel env add NEXT_PUBLIC_BETTER_AUTH_SECRET

# Redeploy:
vercel --prod
```

## Step 4: Update CORS Settings

After deploying the frontend, you'll have the frontend URL. Update the backend's `CORS_ORIGINS` environment variable:

1. Go to your backend project in Vercel Dashboard
2. Settings → Environment Variables
3. Edit `CORS_ORIGINS` to include your frontend URL:
   ```
   https://your-frontend.vercel.app
   ```
4. Redeploy the backend

## Step 5: Test Your Deployment

1. Visit your frontend URL (e.g., `https://your-frontend.vercel.app`)
2. Sign up for a new account
3. Create a task
4. Test all CRUD operations

## Environment Variables Reference

### Backend (`backend/.env`)

```bash
DATABASE_URL=postgresql://user:password@host:5432/database
BETTER_AUTH_SECRET=min-32-character-secret-key
CORS_ORIGINS=https://your-frontend.vercel.app,https://your-frontend-staging.vercel.app
ENVIRONMENT=production
```

### Frontend (`frontend/.env.local`)

```bash
NEXT_PUBLIC_API_URL=https://your-backend.vercel.app
NEXT_PUBLIC_BETTER_AUTH_SECRET=same-as-backend-secret
```

## Troubleshooting

### Backend Issues

**Error: "Module not found"**
- Ensure `requirements.txt` is in the `backend` directory
- Check that all dependencies are listed

**Error: "Database connection failed"**
- Verify `DATABASE_URL` is correct
- Check that your Neon database is running
- Ensure the database allows connections from Vercel IPs

**Error: "CORS error"**
- Update `CORS_ORIGINS` to include your frontend URL
- Redeploy backend after updating environment variables

### Frontend Issues

**Error: "Failed to fetch tasks"**
- Verify `NEXT_PUBLIC_API_URL` points to your backend URL
- Check backend logs for errors
- Ensure backend is deployed and running

**Error: "Invalid token"**
- Ensure `NEXT_PUBLIC_BETTER_AUTH_SECRET` matches backend secret exactly
- Clear browser localStorage and try signing in again

## Database Migrations

For production deployments, you may want to run database migrations manually:

```bash
# Connect to your Neon database
psql "postgresql://user:password@host/database"

# Or use a migration tool like Alembic (not yet configured)
```

## Monitoring & Logs

- **Backend Logs**: Vercel Dashboard → Your Backend Project → Logs
- **Frontend Logs**: Vercel Dashboard → Your Frontend Project → Logs
- **Database Metrics**: Neon Dashboard → Your Project → Metrics

## Custom Domains (Optional)

1. Go to your project in Vercel Dashboard
2. Settings → Domains
3. Add your custom domain
4. Follow DNS configuration instructions
5. Update `CORS_ORIGINS` in backend to include your custom domain

## Security Best Practices

1. **Secret Keys**: Use strong, randomly generated secrets (32+ characters)
2. **HTTPS Only**: Vercel provides HTTPS by default
3. **Environment Variables**: Never commit `.env` files to Git
4. **Database**: Use Neon's IP allowlist if available
5. **Rate Limiting**: Consider adding rate limiting middleware (not yet implemented)

## Continuous Deployment

Vercel automatically deploys when you push to your Git repository:

1. **Production**: Push to `main` branch
2. **Preview**: Push to any other branch (e.g., `develop`)

## Scaling

Vercel's free tier includes:
- Unlimited deployments
- 100GB bandwidth
- Serverless function invocations

For production apps with high traffic, consider upgrading to Pro plan.

## Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Neon Documentation**: [neon.tech/docs](https://neon.tech/docs)
- **FastAPI on Vercel**: [vercel.com/guides/python](https://vercel.com/guides/python)
