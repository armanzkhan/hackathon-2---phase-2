/**
 * T048: Login page
 *
 * Renders AuthForm with mode="login", calls /api/auth/login, stores token, redirects to /tasks.
 */

import AuthForm from '@/components/AuthForm'

export default function LoginPage() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="w-full max-w-md px-4">
        <AuthForm mode="login" />
      </div>
    </div>
  )
}
