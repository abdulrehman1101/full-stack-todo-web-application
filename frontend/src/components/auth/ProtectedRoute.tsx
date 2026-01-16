/**
 * ProtectedRoute component for the todo application.
 * This component wraps protected pages and redirects unauthenticated users back to /login.
 */

import React, { ReactNode, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/src/contexts/AuthContext';
import { Loader2 } from 'lucide-react';

interface ProtectedRouteProps {
  children: ReactNode;
  fallback?: ReactNode; // Optional fallback component while checking auth status
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, fallback = (
  <div className="flex items-center justify-center min-h-screen bg-[#020617]">
    <Loader2 className="h-8 w-8 animate-spin text-indigo-500" />
  </div>
) }) => {
  const { user, loading } = useAuth();
  const router = useRouter();

  // Redirect to login if user is not authenticated and loading is complete
  useEffect(() => {
    if (!user && !loading) {
      router.replace('/login');
    }
  }, [user, loading, router]);

  // Show loading while checking auth status
  if (loading) {
    return fallback;
  }

  // If user is not authenticated and not loading, show nothing while redirecting
  if (!user && !loading) {
    return null;
  }

  // Render children if user is authenticated
  return <>{children}</>;
};

export default ProtectedRoute;