'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { apiClient } from '@/lib/api-client'
import type { Task } from '@/lib/types'

interface TaskItemProps {
  task: Task
  onToggle?: (taskId: number) => void
  onDelete?: (taskId: number) => void
  onUpdate?: () => void
}

export default function TaskItem({ task, onToggle, onDelete, onUpdate }: TaskItemProps) {
  const router = useRouter()
  const [isUpdating, setIsUpdating] = useState(false)
  const formattedDate = new Date(task.created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })

  const handleToggleComplete = async () => {
    if (isUpdating) return

    setIsUpdating(true)
    try {
      await apiClient.put(`/api/${task.user_id}/tasks/${task.id}`, {
        completed: !task.completed,
      })

      onUpdate?.()
      onToggle?.(task.id)
    } catch (error) {
      console.error('Failed to update task:', error)
    } finally {
      setIsUpdating(false)
    }
  }

  const handleEdit = () => {
    router.push(`/tasks/${task.id}`)
  }

  return (
    <div className="border border-gray-200 rounded-lg p-4 mb-3 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex items-start flex-1">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggleComplete}
            disabled={isUpdating}
            className="mt-1 mr-3 h-5 w-5 text-blue-600 rounded focus:ring-blue-500 disabled:opacity-50"
            aria-label={`Mark "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
          />

          <div className="flex-1">
            <h3
              className={`text-lg font-medium ${
                task.completed ? 'line-through text-gray-500' : 'text-gray-900'
              }`}
            >
              {task.title}
            </h3>

            {task.description && (
              <p
                className={`mt-1 text-sm ${
                  task.completed ? 'text-gray-400' : 'text-gray-600'
                }`}
              >
                {task.description}
              </p>
            )}

            <p className="mt-2 text-xs text-gray-400">Created: {formattedDate}</p>
          </div>
        </div>

        <div className="ml-4 flex gap-2">
          <button
            onClick={handleEdit}
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
            aria-label={`Edit "${task.title}"`}
          >
            Edit
          </button>

          {onDelete && (
            <button
              onClick={() => onDelete(task.id)}
              className="text-red-600 hover:text-red-800 text-sm font-medium"
              aria-label={`Delete "${task.title}"`}
            >
              Delete
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
