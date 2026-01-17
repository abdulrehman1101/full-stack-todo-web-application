'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import apiClient from '@/src/lib/api-client';
import { useRouter } from 'next/navigation';

interface User {
  id: string;
  email: string;
  name?: string;
  username?: string;
  created_at: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  updateUser: (updatedUser: User) => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Initialize auth state
    const initializeAuth = async () => {
      setLoading(true);
      try {
        const token = localStorage.getItem('token');
        if (token) {
          // Attempt to fetch user data using the token
          const userData = await fetchUserWithRetry();
          if (userData) {
            setUser(userData);
          } else {
            // If token is invalid, remove it
            localStorage.removeItem('token');
          }
        }
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const fetchUser = async (): Promise<User | null> => {
    try {
      const response = await apiClient.get('/me'); // GET /api/v1/me endpoint
      return response.data;
    } catch (error) {
      return null;
    }
  };

  const fetchUserWithRetry = async (): Promise<User | null> => {
    try {
      const response = await apiClient.get('/me'); // GET /api/v1/me endpoint
      return response.data;
    } catch (error: any) {
      // If the request fails with 401, try again after a small delay
      if (error?.response?.status === 401) {
        await new Promise(resolve => setTimeout(resolve, 100)); // 100ms delay
        try {
          const response = await apiClient.get('/me');
          return response.data;
        } catch (retryError: any) {
          return null;
        }
      }
      return null;
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await apiClient.post('/auth/login', { email, password });

      // Extract token from response
      const { access_token, user: userData } = response.data;

      // Store token in localStorage using the correct key
      localStorage.setItem('token', access_token);

      // Manually set the default header for immediate API calls
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

      // Set user in context and wait for the state update to propagate
      return new Promise<void>((resolve, reject) => {
        try {
          setUser(userData);

          // Use a slightly longer delay to ensure state propagation to all consumers
          setTimeout(() => {
            // Use window.location.href for a clean redirect that forces a full page refresh
            // This ensures the new auth state is picked up properly
            window.location.href = '/dashboard';
            resolve();
          }, 100);
        } catch (error) {
          reject(error);
        }
      });
    } catch (error: any) {
      if (error.response) {
        throw new Error(error.response.data.detail || 'Login failed');
      } else {
        throw new Error('Network error occurred during login');
      }
    }
  };

  const register = async (email: string, password: string) => {
    try {
      const response = await apiClient.post('/auth/register', { email, password });

      // Extract token from response
      const { access_token, user: userData } = response.data;

      // Store token in localStorage using the correct key
      localStorage.setItem('token', access_token);

      // Manually set the default header for immediate API calls
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

      // Set user in context and wait for the state update to propagate
      return new Promise<void>((resolve, reject) => {
        try {
          setUser(userData);

          // Use a slightly longer delay to ensure state propagation to all consumers
          setTimeout(() => {
            // Use window.location.href for a clean redirect that forces a full page refresh
            // This ensures the new auth state is picked up properly
            window.location.href = '/dashboard';
            resolve();
          }, 100);
        } catch (error) {
          reject(error);
        }
      });
    } catch (error: any) {
      if (error.response) {
        throw new Error(error.response.data.detail || 'Registration failed');
      } else {
        throw new Error('Network error occurred during registration');
      }
    }
  };

  const logout = () => {
    // Remove token from localStorage
    localStorage.removeItem('token');

    // Clear the default authorization header
    delete apiClient.defaults.headers.common['Authorization'];

    // Clear user from context
    setUser(null);

    // Redirect to login
    router.push('/login');
    router.refresh(); // Refresh to update UI
  };

  const updateUser = (updatedUser: User) => {
    setUser(updatedUser);
  };

  const isAuthenticated = !!user;

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    updateUser,
    isAuthenticated,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};