/**
 * Authentication hook for the todo application.
 * This module provides authentication state management using React hooks.
 */

import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import { authClient } from '../services/api-client';
import { User } from 'better-auth/types';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: () => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Helper functions for token storage and management
const TOKEN_STORAGE_KEY = 'better-auth-jwt-token';
const USER_STORAGE_KEY = 'better-auth-user';

// Store token in localStorage (or use cookies for better security)
const storeToken = (token: string) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem(TOKEN_STORAGE_KEY, token);
  }
};

// Retrieve token from storage
const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(TOKEN_STORAGE_KEY);
  }
  return null;
};

// Store user data in localStorage
const storeUser = (user: User) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
  }
};

// Retrieve user data from storage
const getUser = (): User | null => {
  if (typeof window !== 'undefined') {
    const userData = localStorage.getItem(USER_STORAGE_KEY);
    return userData ? JSON.parse(userData) : null;
  }
  return null;
};

// Clear stored tokens and user data
const clearStoredAuth = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    localStorage.removeItem(USER_STORAGE_KEY);
  }
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Check session on initial load
  useEffect(() => {
    const checkSession = async () => {
      try {
        // First, try to restore from stored data
        const storedUser = getUser();
        if (storedUser) {
          setUser(storedUser);
        } else {
          // Otherwise, check with Better Auth
          const session = await authClient.getSession();
          if (session?.value?.user) {
            setUser(session.value.user);
            storeUser(session.value.user);
          }
        }
      } catch (error) {
        console.error('Error checking session:', error);
        // Clear stored auth if there's an error
        clearStoredAuth();
      } finally {
        setLoading(false);
      }
    };

    checkSession();

    // Set up session change listener
    const unsubscribe = authClient.subscribe((session) => {
      if (session?.value?.user) {
        setUser(session.value.user);
        storeUser(session.value.user);
        // Store the token if available
        if (session.value.session?.token) {
          storeToken(session.value.session.token);
        }
      } else {
        setUser(null);
        clearStoredAuth();
      }
    });

    return () => {
      unsubscribe();
    };
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await authClient.signIn.email({
        email,
        password,
        callbackURL: "/dashboard", // Redirect after login
      });

      if (response?.data?.user) {
        setUser(response.data.user);
        storeUser(response.data.user);
        // Store the token if available
        if (response.data.session?.token) {
          storeToken(response.data.session.token);
        }
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const register = async (email: string, password: string) => {
    try {
      const response = await authClient.signUp.email({
        email,
        password,
      });

      if (response?.data?.user) {
        setUser(response.data.user);
        storeUser(response.data.user);
        // Store the token if available
        if (response.data.session?.token) {
          storeToken(response.data.session.token);
        }
      }
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await authClient.signOut();
      setUser(null);
      clearStoredAuth();
    } catch (error) {
      console.error('Logout error:', error);
      // Still clear local storage even if backend logout fails
      setUser(null);
      clearStoredAuth();
      throw error;
    }
  };

  const isAuthenticated = (): boolean => {
    return user !== null;
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
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