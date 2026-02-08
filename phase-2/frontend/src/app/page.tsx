'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function Home() {
  const router = useRouter()

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('auth_token')

    if (token) {
      // Redirect to tasks if authenticated
      router.push('/tasks')
    } else {
      // Redirect to login if not authenticated
      router.push('/login')
    }
  }, [router])

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-4">Todo App</h1>
        <p className="text-gray-600">Redirecting...</p>
      </div>
    </div>
  )
}
