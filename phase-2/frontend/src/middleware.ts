/**
 * Next.js middleware for route protection.
 *
 * Protects /tasks routes and redirects unauthenticated users to /login.
 */

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Get token from cookies or localStorage (cookies preferred for SSR)
  const token = request.cookies.get('auth_token')?.value

  // Public routes that don't require authentication
  const publicRoutes = ['/login', '/signup', '/']
  const isPublicRoute = publicRoutes.some((route) => pathname.startsWith(route))

  // If accessing a protected route without a token, redirect to login
  if (!token && !isPublicRoute) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('redirect', pathname)
    return NextResponse.redirect(loginUrl)
  }

  // If accessing login/signup with a token, redirect to tasks
  if (token && (pathname === '/login' || pathname === '/signup')) {
    return NextResponse.redirect(new URL('/tasks', request.url))
  }

  return NextResponse.next()
}

// Configure which routes to run middleware on
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - api routes
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}
