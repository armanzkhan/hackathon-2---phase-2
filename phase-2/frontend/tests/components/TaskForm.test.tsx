/**
 * Component tests for TaskForm.
 *
 * T070: Tests rendering title/description inputs, submitting form, and displaying validation errors.
 */

import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import '@testing-library/jest-dom'
import TaskForm from '@/components/TaskForm'
import { apiClient } from '@/lib/api-client'

// Mock the API client
jest.mock('@/lib/api-client')

describe('TaskForm Component', () => {
  const mockOnSuccess = jest.fn()
  const mockUserId = 'user-123'

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders title and description inputs', () => {
    render(<TaskForm userId={mockUserId} onSuccess={mockOnSuccess} />)

    expect(screen.getByLabelText(/title/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /create task/i })).toBeInTheDocument()
  })

  it('submits form with title only', async () => {
    const user = userEvent.setup()
    ;(apiClient.post as jest.Mock).mockResolvedValue({
      data: {
        id: 1,
        user_id: mockUserId,
        title: 'New Task',
        description: null,
        completed: false,
        created_at: '2026-02-08T10:00:00Z',
        updated_at: '2026-02-08T10:00:00Z',
      },
    })

    render(<TaskForm userId={mockUserId} onSuccess={mockOnSuccess} />)

    await user.type(screen.getByLabelText(/title/i), 'New Task')
    await user.click(screen.getByRole('button', { name: /create task/i }))

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith(`/api/${mockUserId}/tasks`, {
        title: 'New Task',
        description: '',
      })
      expect(mockOnSuccess).toHaveBeenCalled()
    })
  })

  it('submits form with title and description', async () => {
    const user = userEvent.setup()
    ;(apiClient.post as jest.Mock).mockResolvedValue({
      data: {
        id: 1,
        user_id: mockUserId,
        title: 'Task Title',
        description: 'Task Description',
        completed: false,
        created_at: '2026-02-08T10:00:00Z',
        updated_at: '2026-02-08T10:00:00Z',
      },
    })

    render(<TaskForm userId={mockUserId} onSuccess={mockOnSuccess} />)

    await user.type(screen.getByLabelText(/title/i), 'Task Title')
    await user.type(screen.getByLabelText(/description/i), 'Task Description')
    await user.click(screen.getByRole('button', { name: /create task/i }))

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith(`/api/${mockUserId}/tasks`, {
        title: 'Task Title',
        description: 'Task Description',
      })
      expect(mockOnSuccess).toHaveBeenCalled()
    })
  })

  it('displays validation error for empty title', async () => {
    const user = userEvent.setup()

    render(<TaskForm userId={mockUserId} onSuccess={mockOnSuccess} />)

    // Try to submit without entering a title
    await user.click(screen.getByRole('button', { name: /create task/i }))

    await waitFor(() => {
      expect(screen.getByText(/required/i)).toBeInTheDocument()
    })

    // API should not be called
    expect(apiClient.post).not.toHaveBeenCalled()
  })

  it('displays error message on API failure', async () => {
    const user = userEvent.setup()
    ;(apiClient.post as jest.Mock).mockRejectedValue({
      response: {
        data: {
          detail: 'Server error occurred',
        },
      },
    })

    render(<TaskForm userId={mockUserId} onSuccess={mockOnSuccess} />)

    await user.type(screen.getByLabelText(/title/i), 'Test Task')
    await user.click(screen.getByRole('button', { name: /create task/i }))

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument()
    })

    expect(mockOnSuccess).not.toHaveBeenCalled()
  })

  it('clears form after successful submission', async () => {
    const user = userEvent.setup()
    ;(apiClient.post as jest.Mock).mockResolvedValue({
      data: {
        id: 1,
        user_id: mockUserId,
        title: 'New Task',
        description: null,
        completed: false,
        created_at: '2026-02-08T10:00:00Z',
        updated_at: '2026-02-08T10:00:00Z',
      },
    })

    render(<TaskForm userId={mockUserId} onSuccess={mockOnSuccess} />)

    const titleInput = screen.getByLabelText(/title/i) as HTMLInputElement

    await user.type(titleInput, 'New Task')
    await user.click(screen.getByRole('button', { name: /create task/i }))

    await waitFor(() => {
      expect(titleInput.value).toBe('')
    })
  })
})
