'use client';

import { ReactNode } from 'react';
import ProtectedRoute from '@/src/components/auth/ProtectedRoute';
import Sidebar from '@/src/components/sidebar/Sidebar';

interface DashboardLayoutProps {
  children: ReactNode;
}

const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  return (
    <ProtectedRoute>
      <div className="flex min-h-screen bg-white dark:bg-[#020617]">
        <Sidebar />
        <main className="flex-1 ml-0 md:ml-20 lg:ml-64 transition-all duration-300">
          <div className="p-4 md:p-6">
            {children}
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
};

export default DashboardLayout;