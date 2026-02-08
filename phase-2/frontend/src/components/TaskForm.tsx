'use client'

import { useState, FormEvent } from 'react'
import { apiClient } from '@/lib/api-client'

interface TaskFormProps {
  userId: string
  onSuccess?: () => void
}

export default function TaskForm({ userId, onSuccess }: TaskFormProps) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')

    // Validation
    if (!title.trim()) {
      setError('Title is required')
      return
    }

    setIsLoading(true)

    try {
      await apiClient.post(`/api/${userId}/tasks`, {
        title: title.trim(),
        description: description.trim(),
      })

      // Clear form
      setTitle('')
      setDescription('')

      // Call success callback
      onSuccess?.()
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to create task'
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-gray-50 p-4 rounded-lg">
      <h3 className="text-lg font-semibold mb-4">Create New Task</h3>

      {/* Title Input */}
      <div className="mb-4">
        <label htmlFor="task-title" className="block text-sm font-medium text-gray-700 mb-1">
          Title *
        </label>
        <input
          id="task-title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter task title"
          disabled={isLoading}
        />
      </div>

      {/* Description Input */}
      <div className="mb-4">
        <label htmlFor="task-description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="task-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter task description (optional)"
          disabled={isLoading}
        />
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded text-sm">
          {error}
        </div>
      )}

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading}
        className={`w-full font-medium py-2 px-4 rounded transition-colors ${
          isLoading
            ? 'bg-gray-400 cursor-not-allowed'
            : 'bg-blue-500 hover:bg-blue-700 text-white'
        }`}
      >
        {isLoading ? 'Creating...' : 'Create Task'}
      </button>
    </form>
  )
}
