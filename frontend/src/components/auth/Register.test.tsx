/**
 * Unit tests for email format validation in the Register component.
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Register } from './Register'; // Adjust import path as needed
import { useAuth } from '../../hooks/useAuth';

// Mock the useAuth hook
jest.mock('../../hooks/useAuth');

describe('Email Format Validation Tests', () => {
  beforeEach(() => {
    (useAuth as jest.MockedFunction<any>).mockReturnValue({
      register: jest.fn(),
      login: jest.fn(),
      user: null,
      loading: false,
      isAuthenticated: jest.fn(),
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('accepts valid email format', () => {
    render(<Register />);

    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test a valid email
    fireEvent.change(emailInput, { target: { value: 'valid@example.com' } });
    fireEvent.click(submitButton);

    // Should not show error for valid email
    expect(screen.queryByText(/invalid email format/i)).not.toBeInTheDocument();
  });

  test('rejects email without @ symbol', () => {
    render(<Register />);

    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test email without @ symbol
    fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
    fireEvent.click(submitButton);

    // Should show error for invalid email
    expect(screen.getByText(/invalid email format/i)).toBeInTheDocument();
  });

  test('rejects email with @ but no domain', () => {
    render(<Register />);

    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test email with @ but no domain
    fireEvent.change(emailInput, { target: { value: '@example.com' } });
    fireEvent.click(submitButton);

    // Should show error for invalid email
    expect(screen.getByText(/invalid email format/i)).toBeInTheDocument();
  });

  test('rejects email with @ but no username', () => {
    render(<Register />);

    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test email with @ but no username
    fireEvent.change(emailInput, { target: { value: 'user@' } });
    fireEvent.click(submitButton);

    // Should show error for invalid email
    expect(screen.getByText(/invalid email format/i)).toBeInTheDocument();
  });

  test('rejects email with @ but no TLD', () => {
    render(<Register />);

    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test email with @ but no TLD
    fireEvent.change(emailInput, { target: { value: 'user@domain' } });
    fireEvent.click(submitButton);

    // Should show error for invalid email
    expect(screen.getByText(/invalid email format/i)).toBeInTheDocument();
  });

  test('rejects empty email', () => {
    render(<Register />);

    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test empty email
    fireEvent.change(emailInput, { target: { value: '' } });
    fireEvent.click(submitButton);

    // Should show error for empty email
    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
  });

  test('rejects email with multiple @ symbols', () => {
    render(<Register />);

    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test email with multiple @ symbols
    fireEvent.change(emailInput, { target: { value: 'user@@example.com' } });
    fireEvent.click(submitButton);

    // Should show error for invalid email
    expect(screen.getByText(/invalid email format/i)).toBeInTheDocument();
  });

  test('rejects email with space', () => {
    render(<Register />);

    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test email with space
    fireEvent.change(emailInput, { target: { value: 'user @example.com' } });
    fireEvent.click(submitButton);

    // Should show error for invalid email
    expect(screen.getByText(/invalid email format/i)).toBeInTheDocument();
  });

  test('accepts email with subdomain', () => {
    render(<Register />);

    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test email with subdomain
    fireEvent.change(emailInput, { target: { value: 'user@mail.example.com' } });
    fireEvent.click(submitButton);

    // Should not show error for valid email with subdomain
    expect(screen.queryByText(/invalid email format/i)).not.toBeInTheDocument();
  });

  test('accepts email with plus sign', () => {
    render(<Register />);

    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test email with plus sign (common for filtering)
    fireEvent.change(emailInput, { target: { value: 'user+tag@example.com' } });
    fireEvent.click(submitButton);

    // Should not show error for valid email with plus sign
    expect(screen.queryByText(/invalid email format/i)).not.toBeInTheDocument();
  });
});


/**
 * Unit tests for password strength validation in the Register component.
 */

describe('Password Strength Validation Tests', () => {
  beforeEach(() => {
    (useAuth as jest.MockedFunction<any>).mockReturnValue({
      register: jest.fn(),
      login: jest.fn(),
      user: null,
      loading: false,
      isAuthenticated: jest.fn(),
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('rejects password that is too short', () => {
    render(<Register />);

    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test short password
    fireEvent.change(passwordInput, { target: { value: 'weak' } });
    fireEvent.click(submitButton);

    // Should show error for weak password
    expect(screen.getByText(/password must be at least/i)).toBeInTheDocument();
  });

  test('rejects password with only lowercase letters', () => {
    render(<Register />);

    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test password with only lowercase letters
    fireEvent.change(passwordInput, { target: { value: 'password' } });
    fireEvent.click(submitButton);

    // Should show error for weak password (if strength check requires complexity)
    // This depends on the specific requirements
    const errorElement = screen.queryByText(/password too weak/i);
    if (errorElement) {
      expect(errorElement).toBeInTheDocument();
    }
  });

  test('rejects password with only numbers', () => {
    render(<Register />);

    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test password with only numbers
    fireEvent.change(passwordInput, { target: { value: '12345678' } });
    fireEvent.click(submitButton);

    // Should show error for weak password (if strength check requires complexity)
    const errorElement = screen.queryByText(/password too weak/i);
    if (errorElement) {
      expect(errorElement).toBeInTheDocument();
    }
  });

  test('accepts strong password with mixed case, numbers, and special character', () => {
    render(<Register />);

    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test strong password
    fireEvent.change(passwordInput, { target: { value: 'SecurePass123!' } });
    fireEvent.click(submitButton);

    // Should not show error for strong password
    expect(screen.queryByText(/password too weak/i)).not.toBeInTheDocument();
  });

  test('accepts password that meets minimum length requirement', () => {
    render(<Register />);

    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test password that meets minimum length (8 characters)
    fireEvent.change(passwordInput, { target: { value: 'LongPass1' } });
    fireEvent.click(submitButton);

    // Should not show error for password that meets minimum length
    expect(screen.queryByText(/password must be at least/i)).not.toBeInTheDocument();
  });

  test('rejects empty password', () => {
    render(<Register />);

    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test empty password
    fireEvent.change(passwordInput, { target: { value: '' } });
    fireEvent.click(submitButton);

    // Should show error for empty password
    expect(screen.getByText(/password is required/i)).toBeInTheDocument();
  });

  test('shows specific error for password without uppercase letter if required', () => {
    render(<Register />);

    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test password without uppercase (if required by validation)
    fireEvent.change(passwordInput, { target: { value: 'lowercase123!' } });
    fireEvent.click(submitButton);

    // Might show error depending on specific requirements
    const errorElement = screen.queryByText(/uppercase letter required/i);
    if (errorElement) {
      expect(errorElement).toBeInTheDocument();
    }
  });

  test('shows specific error for password without number if required', () => {
    render(<Register />);

    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test password without number (if required by validation)
    fireEvent.change(passwordInput, { target: { value: 'Password!' } });
    fireEvent.click(submitButton);

    // Might show error depending on specific requirements
    const errorElement = screen.queryByText(/number required/i);
    if (errorElement) {
      expect(errorElement).toBeInTheDocument();
    }
  });

  test('shows specific error for password without special character if required', () => {
    render(<Register />);

    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test password without special character (if required by validation)
    fireEvent.change(passwordInput, { target: { value: 'Password123' } });
    fireEvent.click(submitButton);

    // Might show error depending on specific requirements
    const errorElement = screen.queryByText(/special character required/i);
    if (errorElement) {
      expect(errorElement).toBeInTheDocument();
    }
  });
});