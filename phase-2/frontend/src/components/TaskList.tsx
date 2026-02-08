'use client'

import { useState, useEffect } from 'react'
import { apiClient } from '@/lib/api-client'
import type { Task } from '@/lib/types'
import TaskItem from './TaskItem'

interface TaskListProps {
  userId: string
}

type FilterOption = 'all' | 'incomplete' | 'completed'

export default function TaskList({ userId }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [filter, setFilter] = useState<FilterOption>('all')

  useEffect(() => {
    fetchTasks()
  }, [userId, filter])

  const fetchTasks = async () => {
    try {
      setIsLoading(true)
      setError('')

      // Build query parameters based on filter
      let url = `/api/${userId}/tasks`
      if (filter === 'incomplete') {
        url += '?completed=false'
      } else if (filter === 'completed') {
        url += '?completed=true'
      }

      const response = await apiClient.get<Task[]>(url)
      setTasks(response.data)
    } catch (err) {
      setError('Failed to load tasks. Please try again.')
      console.error('Error fetching tasks:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleToggle = async (_taskId: number) => {
    // Refresh list after toggle
    await fetchTasks()
  }

  const handleDelete = async (taskId: number) => {
    if (!window.confirm('Are you sure you want to delete this task? This action cannot be undone.')) {
      return
    }

    try {
      await apiClient.delete(`/api/${userId}/tasks/${taskId}`)

      // Refresh list after deletion
      await fetchTasks()
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to delete task'
      setError(`Failed to delete task: ${errorMessage}`)
      console.error('Error deleting task:', err)
    }
  }

  const handleUpdate = async () => {
    // Refresh list after any update
    await fetchTasks()
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-gray-600">Loading tasks...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">{error}</p>
        <button
          onClick={fetchTasks}
          className="mt-2 text-red-600 hover:text-red-800 font-medium"
        >
          Try Again
        </button>
      </div>
    )
  }

  const emptyMessage = () => {
    if (filter === 'completed') return 'No completed tasks'
    if (filter === 'incomplete') return 'No incomplete tasks'
    return 'No tasks yet'
  }

  return (
    <div>
      {/* Filter Controls */}
      <div className="mb-4 flex gap-2">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            filter === 'all'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          All
        </button>
        <button
          onClick={() => setFilter('incomplete')}
          className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            filter === 'incomplete'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Incomplete
        </button>
        <button
          onClick={() => setFilter('completed')}
          className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            filter === 'completed'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Completed
        </button>
      </div>

      {/* Task List */}
      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">{emptyMessage()}</p>
          <p className="text-gray-400 mt-2">
            {filter === 'all' && 'Create your first task to get started!'}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onToggle={handleToggle}
              onDelete={handleDelete}
              onUpdate={handleUpdate}
            />
          ))}
        </div>
      )}
    </div>
  )
}
