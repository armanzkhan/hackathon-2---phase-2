/**
 * Better Auth configuration.
 *
 * Configures Better Auth with email/password provider and JWT settings.
 */

// Auth configuration
export const authConfig = {
  providers: {
    email: {
      enabled: true,
    },
  },
  jwt: {
    secret: process.env.NEXT_PUBLIC_BETTER_AUTH_SECRET || 'development-secret',
    expiresIn: '24h',
  },
  callbacks: {
    redirect: {
      afterLogin: '/tasks',
      afterSignup: '/tasks',
      afterLogout: '/login',
    },
  },
}

// Auth helper functions
export const isAuthenticated = (): boolean => {
  if (typeof window === 'undefined') return false
  const token = localStorage.getItem('auth_token')
  return !!token
}

export const getAuthToken = (): string | null => {
  if (typeof window === 'undefined') return null
  return localStorage.getItem('auth_token')
}

export const setAuthToken = (token: string): void => {
  if (typeof window === 'undefined') return
  localStorage.setItem('auth_token', token)
}

export const clearAuthToken = (): void => {
  if (typeof window === 'undefined') return
  localStorage.removeItem('auth_token')
}

export const getUserId = (): string | null => {
  const token = getAuthToken()
  if (!token) return null

  try {
    // Decode JWT to extract user_id (simple base64 decode, no verification)
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.user_id || null
  } catch (error) {
    console.error('Failed to decode token:', error)
    return null
  }
}

export const logout = (): void => {
  clearAuthToken()
  if (typeof window !== 'undefined') {
    window.location.href = '/login'
  }
}
