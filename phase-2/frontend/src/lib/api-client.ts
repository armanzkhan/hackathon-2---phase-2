/**
 * API client with JWT interceptor.
 *
 * Axios instance that automatically attaches JWT token and handles auth errors.
 */

import axios, { AxiosError } from 'axios'
import { getAuthToken, logout } from './auth'
import type { ErrorResponse } from './types'

// Create axios instance
export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
})

// Request interceptor - attach JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = getAuthToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - handle auth errors
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error: AxiosError<ErrorResponse>) => {
    if (error.response?.status === 401) {
      // Unauthorized - token invalid or expired
      logout()
      return Promise.reject(new Error('Session expired. Please login again.'))
    }

    if (error.response?.status === 403) {
      // Forbidden - user doesn't have permission
      return Promise.reject(
        new Error(error.response.data?.detail || 'Access denied')
      )
    }

    // Other errors
    const errorMessage =
      error.response?.data?.detail || error.message || 'An error occurred'
    return Promise.reject(new Error(errorMessage))
  }
)

export default apiClient
