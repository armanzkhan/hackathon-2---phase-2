'use client'

import { useEffect, useState, useRef } from 'react'
import { logout, getUserId } from '@/lib/auth'
import TaskList from '@/components/TaskList'
import TaskForm from '@/components/TaskForm'

export default function TasksPage() {
  const [userId, setUserId] = useState<string | null>(null)
  const taskListRef = useRef<{ refetch: () => void }>(null)

  useEffect(() => {
    const id = getUserId()
    setUserId(id)
  }, [])

  const handleLogout = () => {
    logout()
  }

  const handleTaskCreated = () => {
    // Refresh task list after creating a task
    window.location.reload()
  }

  if (!userId) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-600">Loading...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
          <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition-colors"
          >
            Logout
          </button>
        </div>

        {/* Create Task Form */}
        <div className="bg-white shadow rounded-lg p-6 mb-6">
          <TaskForm userId={userId} onSuccess={handleTaskCreated} />
        </div>

        {/* Task List */}
        <div className="bg-white shadow rounded-lg p-6">
          <TaskList userId={userId} />
        </div>
      </div>
    </div>
  )
}
