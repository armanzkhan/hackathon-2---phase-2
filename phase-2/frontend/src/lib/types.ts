/**
 * TypeScript interfaces for the Todo application.
 */

// User types
export interface User {
  id: string
  email: string
  created_at: string
  updated_at: string
}

// Task types
export interface Task {
  id: number
  user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}

export interface TaskCreateRequest {
  title: string
  description?: string
}

export interface TaskUpdateRequest {
  title?: string
  description?: string
  completed?: boolean
}

// Authentication types
export interface AuthResponse {
  user_id: string
  email: string
  token: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface SignupRequest {
  email: string
  password: string
}

// Error types
export interface ErrorResponse {
  detail: string
  field_errors?: Record<string, string>
}

export interface ValidationError {
  field: string
  message: string
}
