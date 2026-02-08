/**
 * T038: E2E test for signup flow
 *
 * Tests complete user signup flow: navigate to signup → fill form → submit → redirected to tasks page.
 */

import { test, expect } from '@playwright/test'

test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Start from home page
    await page.goto('http://localhost:3000')
  })

  test('user can sign up with valid credentials', async ({ page }) => {
    // Navigate to signup page
    await page.goto('http://localhost:3000/signup')

    // Fill in signup form
    await page.fill('input[type="email"]', `testuser${Date.now()}@example.com`)
    await page.fill('input[type="password"]', 'SecurePassword123')

    // Submit form
    await page.click('button[type="submit"]')

    // Should redirect to tasks page after successful signup
    await expect(page).toHaveURL(/\/tasks/)

    // Should see tasks page content
    await expect(page.locator('h1, h2')).toContainText(/tasks|todo/i)
  })

  test('user can log in with existing credentials', async ({ page }) => {
    // First, create a user via signup
    await page.goto('http://localhost:3000/signup')
    const email = `logintest${Date.now()}@example.com`
    await page.fill('input[type="email"]', email)
    await page.fill('input[type="password"]', 'SecurePassword123')
    await page.click('button[type="submit"]')

    // Wait for redirect to tasks
    await expect(page).toHaveURL(/\/tasks/)

    // Logout (simulate)
    await page.evaluate(() => localStorage.clear())

    // Navigate to login page
    await page.goto('http://localhost:3000/login')

    // Fill in login form with same credentials
    await page.fill('input[type="email"]', email)
    await page.fill('input[type="password"]', 'SecurePassword123')

    // Submit form
    await page.click('button[type="submit"]')

    // Should redirect to tasks page after successful login
    await expect(page).toHaveURL(/\/tasks/)
  })

  test('shows error for invalid credentials', async ({ page }) => {
    // Navigate to login page
    await page.goto('http://localhost:3000/login')

    // Try to login with invalid credentials
    await page.fill('input[type="email"]', 'nonexistent@example.com')
    await page.fill('input[type="password"]', 'WrongPassword123')
    await page.click('button[type="submit"]')

    // Should show error message
    await expect(page.locator('text=/error|invalid/i')).toBeVisible()

    // Should stay on login page
    await expect(page).toHaveURL(/\/login/)
  })

  test('protected routes redirect to login when not authenticated', async ({ page }) => {
    // Clear any existing auth
    await page.evaluate(() => localStorage.clear())

    // Try to access protected route
    await page.goto('http://localhost:3000/tasks')

    // Should redirect to login
    await expect(page).toHaveURL(/\/login/)
  })

  test('authenticated users cannot access login page', async ({ page }) => {
    // First, authenticate
    await page.goto('http://localhost:3000/signup')
    await page.fill('input[type="email"]', `authtest${Date.now()}@example.com`)
    await page.fill('input[type="password"]', 'SecurePassword123')
    await page.click('button[type="submit"]')

    // Wait for redirect
    await expect(page).toHaveURL(/\/tasks/)

    // Try to access login page
    await page.goto('http://localhost:3000/login')

    // Should redirect back to tasks
    await expect(page).toHaveURL(/\/tasks/)
  })
})
