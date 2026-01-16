'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTheme } from 'next-themes';
import { usePathname } from 'next/navigation';
import {
  Menu,
  X,
  LayoutDashboard,
  User,
  Settings,
  LogOut,
  Moon,
  Sun
} from 'lucide-react';
import { useAuth } from '@/src/contexts/AuthContext';

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(true);
  const [isMobile, setIsMobile] = useState(false);
  const { theme, setTheme } = useTheme();
  const { user, logout } = useAuth();
  const pathname = usePathname();

  // Check screen size for responsive design
  useEffect(() => {
    const checkScreenSize = () => {
      setIsMobile(window.innerWidth < 768);
      if (window.innerWidth < 768) {
        setIsOpen(false);
      } else {
        setIsOpen(true);
      }
    };

    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);

    return () => window.removeEventListener('resize', checkScreenSize);
  }, []);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  // Close sidebar on mobile when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (isMobile && isOpen && !(event.target as Element).closest('.sidebar')) {
        setIsOpen(false);
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, [isMobile, isOpen]);

  return (
    <>
      {/* Mobile Overlay */}
      {isMobile && isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Hamburger Button for Mobile */}
      {isMobile && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            toggleSidebar();
          }}
          className="fixed top-4 left-4 z-50 p-2 rounded-lg bg-white/80 dark:bg-[#020617]/80 backdrop-blur-md text-slate-900 dark:text-slate-200 lg:hidden border border-slate-200 dark:border-slate-700"
          aria-label={isOpen ? "Close menu" : "Open menu"}
        >
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      )}

      {/* Sidebar */}
      <motion.aside
        className={`sidebar fixed top-0 left-0 h-full z-50 flex flex-col bg-white dark:bg-[#020617] text-slate-900 dark:text-slate-200 border-r border-slate-200 dark:border-slate-700 transition-all duration-300 ${
          isMobile ? 'w-full max-w-64' : ''
        }`}
        initial={{ x: isMobile ? '-100%' : 0 }}
        animate={{
          x: isOpen ? 0 : (isMobile ? '-100%' : `-${isOpen ? 0 : 240}px`)
        }}
        exit={{ x: isMobile ? '-100%' : 0 }}
        transition={{ type: 'spring', damping: 20 }}
      >
        <div className="bg-white/80 dark:bg-[#020617]/80 backdrop-blur-md flex-1 p-4 flex flex-col">
          {/* Toggle Button for Desktop */}
          {!isMobile && (
            <div className="flex justify-end mb-6">
              <button
                onClick={toggleSidebar}
                className="p-2 rounded-lg bg-white/80 dark:bg-[#020617]/80 backdrop-blur-md text-slate-900 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors border border-slate-200 dark:border-slate-700"
                aria-label={isOpen ? "Collapse sidebar" : "Expand sidebar"}
              >
                {isOpen ? <X size={20} /> : <Menu size={20} />}
              </button>
            </div>
          )}

          {/* User Profile Section */}
          <div className="mb-8">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-full bg-indigo-500/20 dark:bg-indigo-500/20 flex items-center justify-center">
                <User className="text-indigo-500 dark:text-indigo-400" size={20} />
              </div>
              {isOpen && (
                <div>
                  <p className="font-medium text-slate-900 dark:text-slate-200">{user?.name || user?.username || (user?.email ? user.email.split('@')[0] : 'User')}</p>
                  <p className="text-sm text-gray-400 dark:text-slate-400">{user?.email || 'Email'}</p>
                </div>
              )}
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="flex-1">
            <ul className="space-y-2">
              <li>
                <a
                  href="/dashboard"
                  className={`flex items-center gap-3 p-3 rounded-lg bg-white/80 dark:bg-[#020617]/80 backdrop-blur-md transition-all duration-300 border border-slate-200 dark:border-slate-700 ${
                    pathname === '/dashboard'
                      ? 'bg-blue-50 dark:bg-indigo-900/30 border border-blue-500 dark:border-indigo-500 text-blue-600 dark:text-indigo-300'
                      : 'hover:bg-slate-100 dark:hover:bg-slate-700 hover:text-blue-600 dark:hover:text-indigo-400 border-l-4 border-transparent hover:border-blue-500 dark:hover:border-indigo-500'
                  }`}
                >
                  <LayoutDashboard className="text-blue-600 dark:text-indigo-400" size={20} />
                  {isOpen && <span className="text-slate-900 dark:text-slate-200">Dashboard</span>}
                </a>
              </li>
              <li>
                <a
                  href="/dashboard/profile"
                  className={`flex items-center gap-3 p-3 rounded-lg bg-white/80 dark:bg-[#020617]/80 backdrop-blur-md transition-all duration-300 border border-slate-200 dark:border-slate-700 ${
                    pathname === '/dashboard/profile'
                      ? 'bg-blue-50 dark:bg-indigo-900/30 border border-blue-500 dark:border-indigo-500 text-blue-600 dark:text-indigo-300'
                      : 'hover:bg-slate-100 dark:hover:bg-slate-700 hover:text-blue-600 dark:hover:text-indigo-400 border-l-4 border-transparent hover:border-blue-500 dark:hover:border-indigo-500'
                  }`}
                >
                  <User className="text-blue-600 dark:text-indigo-400" size={20} />
                  {isOpen && <span className="text-slate-900 dark:text-slate-200">Profile</span>}
                </a>
              </li>
              <li>
                <a
                  href="/dashboard/settings"
                  className={`flex items-center gap-3 p-3 rounded-lg bg-white/80 dark:bg-[#020617]/80 backdrop-blur-md transition-all duration-300 border border-slate-200 dark:border-slate-700 ${
                    pathname === '/dashboard/settings'
                      ? 'bg-blue-50 dark:bg-indigo-900/30 border border-blue-500 dark:border-indigo-500 text-blue-600 dark:text-indigo-300'
                      : 'hover:bg-slate-100 dark:hover:bg-slate-700 hover:text-blue-600 dark:hover:text-indigo-400 border-l-4 border-transparent hover:border-blue-500 dark:hover:border-indigo-500'
                  }`}
                >
                  <Settings className="text-blue-600 dark:text-indigo-400" size={20} />
                  {isOpen && <span className="text-slate-900 dark:text-slate-200">Settings</span>}
                </a>
              </li>
            </ul>
          </nav>

          {/* Bottom Section */}
          <div className="mt-auto space-y-2">
            <button
              onClick={logout}
              className="w-full flex items-center gap-3 p-3 rounded-lg bg-white/80 dark:bg-[#020617]/80 backdrop-blur-md hover:bg-red-50 dark:hover:bg-red-900/30 hover:text-red-600 dark:hover:text-red-400 transition-transform duration-300 hover:scale-105 text-red-600 dark:text-red-400 border border-slate-200 dark:border-slate-700"
            >
              <LogOut size={20} className="text-red-600 dark:text-red-400" />
              {isOpen && <span className="text-slate-900 dark:text-slate-200">Logout</span>}
            </button>
          </div>
        </div>
      </motion.aside>
    </>
  );
};

export default Sidebar;