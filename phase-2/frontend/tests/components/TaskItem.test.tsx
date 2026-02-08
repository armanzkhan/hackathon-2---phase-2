/**
 * Component tests for TaskItem.
 *
 * T056: Tests displaying title, description, completed status, and timestamps.
 */

import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import TaskItem from '@/components/TaskItem'
import type { Task } from '@/lib/types'

describe('TaskItem Component', () => {
  const mockTask: Task = {
    id: 1,
    user_id: 'user1',
    title: 'Test Task',
    description: 'Test Description',
    completed: false,
    created_at: '2026-02-08T10:30:00Z',
    updated_at: '2026-02-08T11:00:00Z',
  }

  it('displays task title', () => {
    render(<TaskItem task={mockTask} />)

    expect(screen.getByText('Test Task')).toBeInTheDocument()
  })

  it('displays task description', () => {
    render(<TaskItem task={mockTask} />)

    expect(screen.getByText('Test Description')).toBeInTheDocument()
  })

  it('displays task without description', () => {
    const taskNoDesc = { ...mockTask, description: null }
    render(<TaskItem task={taskNoDesc} />)

    expect(screen.getByText('Test Task')).toBeInTheDocument()
    expect(screen.queryByText('Test Description')).not.toBeInTheDocument()
  })

  it('shows completed status as unchecked', () => {
    render(<TaskItem task={mockTask} />)

    const checkbox = screen.getByRole('checkbox')
    expect(checkbox).toBeInTheDocument()
    expect(checkbox).not.toBeChecked()
  })

  it('shows completed status as checked', () => {
    const completedTask = { ...mockTask, completed: true }
    render(<TaskItem task={completedTask} />)

    const checkbox = screen.getByRole('checkbox')
    expect(checkbox).toBeChecked()
  })

  it('displays created timestamp', () => {
    render(<TaskItem task={mockTask} />)

    // Check that some date/time is displayed (format may vary)
    expect(screen.getByText(/2026|Feb|08/)).toBeInTheDocument()
  })

  it('renders delete button when onDelete prop provided', () => {
    const mockDelete = jest.fn()
    render(<TaskItem task={mockTask} onDelete={mockDelete} />)

    const deleteButton = screen.getByRole('button', { name: /delete/i })
    expect(deleteButton).toBeInTheDocument()
  })

  it('does not render delete button when onDelete prop not provided', () => {
    render(<TaskItem task={mockTask} />)

    const deleteButton = screen.queryByRole('button')
    expect(deleteButton).not.toBeInTheDocument()
  })
})
