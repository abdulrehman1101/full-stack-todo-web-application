/**
 * API client for the todo application.
 * This module provides an API client that automatically attaches JWT tokens to requests.
 */

import { getAuth } from "better-auth/client";

// Initialize the auth client
const authClient = getAuth({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
  fetch: globalThis.fetch,
});

// Helper functions for token retrieval (mirroring useAuth.ts)
const TOKEN_STORAGE_KEY = 'better-auth-jwt-token';

// Retrieve token from storage
const getStoredToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(TOKEN_STORAGE_KEY);
  }
  return null;
};

// Create a base API client that can be extended for different endpoints
class ApiClient {
  private baseUrl: string;
  private authClient: any;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000/api";
    this.authClient = authClient;
  }

  // Generic request method that includes JWT token in headers
  async request(endpoint: string, options: RequestInit = {}) {
    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    // Get the current session to access the JWT token
    const session = await this.authClient.getSession();

    // Try to get token from session first, then fall back to stored token
    let token = null;
    if (session?.value?.session?.token) {
      token = session.value.session.token;
    } else {
      // Try to get token from localStorage if session is not available
      token = getStoredToken();
    }

    // If user is authenticated, add the JWT token to the headers
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const url = `${this.baseUrl}${endpoint}`;

    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Handle 401 responses for expired tokens
    if (response.status === 401) {
      // Clear stored auth data if token is rejected
      if (typeof window !== 'undefined') {
        localStorage.removeItem('better-auth-jwt-token');
        localStorage.removeItem('better-auth-user');
      }
      throw new Error(`Authentication failed: ${response.status} ${response.statusText}`);
    }

    // Handle 403 responses for unauthorized access to another user's data
    if (response.status === 403) {
      throw new Error(`Access forbidden: ${response.status} ${response.statusText}`);
    }

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // GET request method
  async get<T>(endpoint: string): Promise<T> {
    return this.request(endpoint, { method: "GET" });
  }

  // POST request method
  async post<T>(endpoint: string, data: any): Promise<T> {
    return this.request(endpoint, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  // PUT request method
  async put<T>(endpoint: string, data: any): Promise<T> {
    return this.request(endpoint, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  // DELETE request method
  async delete<T>(endpoint: string): Promise<T> {
    return this.request(endpoint, {
      method: "DELETE",
    });
  }
}

// Export a singleton instance of the API client
export const apiClient = new ApiClient();

// Export the auth client for direct use if needed
export { authClient };