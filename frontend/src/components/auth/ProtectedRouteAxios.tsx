/**
 * ProtectedRoute component for the todo application using Axios-based auth.
 * This component wraps protected pages and redirects unauthenticated users to login.
 */

import React, { ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/src/contexts/AuthContext';

interface ProtectedRouteProps {
  children: ReactNode;
  fallback?: ReactNode; // Optional fallback component while checking auth status
}

const ProtectedRouteAxios: React.FC<ProtectedRouteProps> = ({ children, fallback = null }) => {
  const { user, loading } = useAuth();
  const router = useRouter();

  // Show fallback while checking auth status
  if (loading) {
    return fallback;
  }

  // Redirect to login if user is not authenticated
  if (!user) {
    // Use router.replace to avoid back button issues
    if (typeof window !== 'undefined') {
      router.replace('/login');
    }
    return null;
  }

  // Render children if user is authenticated
  return <>{children}</>;
};

export default ProtectedRouteAxios;