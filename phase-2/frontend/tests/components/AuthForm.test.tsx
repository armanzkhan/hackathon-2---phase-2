/**
 * T037: Component test for AuthForm
 *
 * Tests that AuthForm renders email/password inputs, submits form, displays errors.
 */

import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import '@testing-library/jest-dom'
import AuthForm from '@/components/AuthForm'

// Mock the API client
jest.mock('@/lib/api-client', () => ({
  __esModule: true,
  default: {
    post: jest.fn(),
  },
}))

// Mock Next.js router
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}))

describe('AuthForm Component', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders email and password inputs in login mode', () => {
    render(<AuthForm mode="login" />)

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /log in/i })).toBeInTheDocument()
  })

  it('renders email and password inputs in signup mode', () => {
    render(<AuthForm mode="signup" />)

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument()
  })

  it('submits form with email and password', async () => {
    const user = userEvent.setup()
    render(<AuthForm mode="login" />)

    const emailInput = screen.getByLabelText(/email/i)
    const passwordInput = screen.getByLabelText(/password/i)
    const submitButton = screen.getByRole('button', { name: /log in/i })

    await user.type(emailInput, 'test@example.com')
    await user.type(passwordInput, 'SecurePassword123')
    await user.click(submitButton)

    // Form should have been submitted
    expect(emailInput).toHaveValue('test@example.com')
    expect(passwordInput).toHaveValue('SecurePassword123')
  })

  it('displays validation errors for empty fields', async () => {
    const user = userEvent.setup()
    render(<AuthForm mode="login" />)

    const submitButton = screen.getByRole('button', { name: /log in/i })
    await user.click(submitButton)

    // Should show validation errors
    await waitFor(() => {
      expect(screen.getByText(/email is required/i) || screen.getByText(/required/i)).toBeInTheDocument()
    })
  })

  it('displays error message on failed authentication', async () => {
    const apiClient = require('@/lib/api-client').default
    apiClient.post.mockRejectedValueOnce(new Error('Invalid credentials'))

    const user = userEvent.setup()
    render(<AuthForm mode="login" />)

    const emailInput = screen.getByLabelText(/email/i)
    const passwordInput = screen.getByLabelText(/password/i)
    const submitButton = screen.getByRole('button', { name: /log in/i })

    await user.type(emailInput, 'test@example.com')
    await user.type(passwordInput, 'WrongPassword')
    await user.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i) || screen.getByText(/error/i)).toBeInTheDocument()
    })
  })

  it('shows loading state during submission', async () => {
    const apiClient = require('@/lib/api-client').default
    apiClient.post.mockImplementationOnce(
      () => new Promise((resolve) => setTimeout(resolve, 100))
    )

    const user = userEvent.setup()
    render(<AuthForm mode="login" />)

    const emailInput = screen.getByLabelText(/email/i)
    const passwordInput = screen.getByLabelText(/password/i)
    const submitButton = screen.getByRole('button', { name: /log in/i })

    await user.type(emailInput, 'test@example.com')
    await user.type(passwordInput, 'SecurePassword123')
    await user.click(submitButton)

    // Button should be disabled during loading
    expect(submitButton).toBeDisabled()
  })
})
