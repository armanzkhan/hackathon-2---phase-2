'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { apiClient } from '@/lib/api-client'
import { getUserId } from '@/lib/auth'
import type { Task } from '@/lib/types'

export default function TaskEditPage() {
  const router = useRouter()
  const params = useParams()
  const taskId = params.id as string

  const [userId, setUserId] = useState<string | null>(null)
  const [task, setTask] = useState<Task | null>(null)
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [completed, setCompleted] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const id = getUserId()
    setUserId(id)
  }, [])

  useEffect(() => {
    if (userId && taskId) {
      fetchTask()
    }
  }, [userId, taskId])

  const fetchTask = async () => {
    if (!userId) return

    try {
      setIsLoading(true)
      const response = await apiClient.get<Task>(`/api/${userId}/tasks/${taskId}`)
      const taskData = response.data

      setTask(taskData)
      setTitle(taskData.title)
      setDescription(taskData.description || '')
      setCompleted(taskData.completed)
    } catch (err: any) {
      setError('Failed to load task. It may not exist or you may not have access.')
      console.error('Error fetching task:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!userId || !taskId) return

    if (!title.trim()) {
      setError('Title is required')
      return
    }

    setIsSaving(true)
    setError('')

    try {
      await apiClient.put(`/api/${userId}/tasks/${taskId}`, {
        title: title.trim(),
        description: description.trim(),
        completed,
      })

      router.push('/tasks')
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to update task'
      setError(errorMessage)
    } finally {
      setIsSaving(false)
    }
  }

  const handleCancel = () => {
    router.push('/tasks')
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-600">Loading task...</p>
      </div>
    )
  }

  if (!task && !isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error || 'Task not found'}</p>
          <button
            onClick={handleCancel}
            className="text-blue-600 hover:text-blue-800"
          >
            Back to Tasks
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <button
            onClick={handleCancel}
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            ← Back to Tasks
          </button>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">Edit Task</h1>

          <form onSubmit={handleSubmit}>
            {/* Title Input */}
            <div className="mb-4">
              <label htmlFor="edit-title" className="block text-sm font-medium text-gray-700 mb-1">
                Title *
              </label>
              <input
                id="edit-title"
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter task title"
                disabled={isSaving}
              />
            </div>

            {/* Description Input */}
            <div className="mb-4">
              <label htmlFor="edit-description" className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                id="edit-description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={5}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter task description (optional)"
                disabled={isSaving}
              />
            </div>

            {/* Completed Checkbox */}
            <div className="mb-6">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={completed}
                  onChange={(e) => setCompleted(e.target.checked)}
                  className="mr-2 h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
                  disabled={isSaving}
                />
                <span className="text-sm font-medium text-gray-700">Mark as completed</span>
              </label>
            </div>

            {/* Error Message */}
            {error && (
              <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded text-sm">
                {error}
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-3">
              <button
                type="submit"
                disabled={isSaving}
                className={`flex-1 font-medium py-2 px-4 rounded transition-colors ${
                  isSaving
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-blue-500 hover:bg-blue-700 text-white'
                }`}
              >
                {isSaving ? 'Saving...' : 'Save Changes'}
              </button>

              <button
                type="button"
                onClick={handleCancel}
                disabled={isSaving}
                className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-medium py-2 px-4 rounded transition-colors disabled:opacity-50"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
