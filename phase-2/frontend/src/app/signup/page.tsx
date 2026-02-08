/**
 * T049: Signup page
 *
 * Renders AuthForm with mode="signup", calls /api/auth/signup, stores token, redirects to /tasks.
 */

import AuthForm from '@/components/AuthForm'

export default function SignupPage() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="w-full max-w-md px-4">
        <AuthForm mode="signup" />
      </div>
    </div>
  )
}
