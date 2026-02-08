/**
 * Component tests for TaskList.
 *
 * T055: Tests rendering task list, displaying task titles, and showing empty state.
 */

import { render, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import TaskList from '@/components/TaskList'
import { apiClient } from '@/lib/api-client'

// Mock the API client
jest.mock('@/lib/api-client')

// Mock TaskItem component to simplify testing
jest.mock('@/components/TaskItem', () => ({
  __esModule: true,
  default: ({ task }: { task: any }) => (
    <div data-testid={`task-item-${task.id}`}>{task.title}</div>
  ),
}))

describe('TaskList Component', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders list of tasks', async () => {
    // Mock API response with tasks
    const mockTasks = [
      {
        id: 1,
        user_id: 'user1',
        title: 'Task 1',
        description: 'Description 1',
        completed: false,
        created_at: '2026-02-08T10:00:00Z',
        updated_at: '2026-02-08T10:00:00Z',
      },
      {
        id: 2,
        user_id: 'user1',
        title: 'Task 2',
        description: 'Description 2',
        completed: true,
        created_at: '2026-02-08T11:00:00Z',
        updated_at: '2026-02-08T11:00:00Z',
      },
    ]

    ;(apiClient.get as jest.Mock).mockResolvedValue({ data: mockTasks })

    render(<TaskList userId="user1" />)

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByTestId('task-item-1')).toBeInTheDocument()
      expect(screen.getByTestId('task-item-2')).toBeInTheDocument()
    })
  })

  it('displays task titles', async () => {
    const mockTasks = [
      {
        id: 1,
        user_id: 'user1',
        title: 'Buy groceries',
        description: 'Milk, eggs, bread',
        completed: false,
        created_at: '2026-02-08T10:00:00Z',
        updated_at: '2026-02-08T10:00:00Z',
      },
    ]

    ;(apiClient.get as jest.Mock).mockResolvedValue({ data: mockTasks })

    render(<TaskList userId="user1" />)

    await waitFor(() => {
      expect(screen.getByText('Buy groceries')).toBeInTheDocument()
    })
  })

  it('shows empty state when no tasks', async () => {
    // Mock API response with empty array
    ;(apiClient.get as jest.Mock).mockResolvedValue({ data: [] })

    render(<TaskList userId="user1" />)

    await waitFor(() => {
      expect(screen.getByText(/no tasks/i)).toBeInTheDocument()
    })
  })

  it('shows loading state while fetching', () => {
    // Mock API to delay response
    ;(apiClient.get as jest.Mock).mockImplementation(
      () =>
        new Promise((resolve) =>
          setTimeout(() => resolve({ data: [] }), 1000)
        )
    )

    render(<TaskList userId="user1" />)

    expect(screen.getByText(/loading/i)).toBeInTheDocument()
  })

  it('displays error message on API failure', async () => {
    // Mock API to reject
    ;(apiClient.get as jest.Mock).mockRejectedValue(
      new Error('Failed to fetch tasks')
    )

    render(<TaskList userId="user1" />)

    await waitFor(() => {
      expect(screen.getByText(/failed to load tasks/i)).toBeInTheDocument()
    })
  })
})
