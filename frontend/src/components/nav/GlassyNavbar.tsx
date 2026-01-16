'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { UserCircle, Menu, X, LogOut, LayoutDashboard, Settings } from 'lucide-react';
import { useState, useEffect } from 'react';
import { useAuth } from '@/src/contexts/AuthContext';
import { useTheme } from 'next-themes';
import { usePathname } from 'next/navigation';
import ThemeToggle from '@/src/components/common/ThemeToggle';

const GlassyNavbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [mounted, setMounted] = useState(false);
  const { user, isAuthenticated, logout } = useAuth();
  const { theme, setTheme } = useTheme();
  const pathname = usePathname();

  // Set mounted to true on client-side
  useEffect(() => {
    setMounted(true);
  }, []);

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-slate-200 bg-white/80 dark:bg-[#020617]/80 backdrop-blur-md">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center"
            >
              <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-blue-600 to-cyan-400"></div>
              <span className="ml-2 text-xl font-bold text-blue-600 dark:text-indigo-400 glow-text">CyberTodo</span>
            </motion.div>
          </Link>

          {/* Desktop Navigation - Empty for unauthenticated users */}
          <div className="hidden items-center space-x-8 md:flex">
            {isAuthenticated ? (
              <>
                {/* Authenticated user doesn't need additional nav links here */}
              </>
            ) : (
              <>
                {/* Unauthenticated user - no center navigation links */}
              </>
            )}
          </div>

          {/* Auth-dependent Buttons */}
          <div className="hidden items-center space-x-4 md:flex">
            {isAuthenticated ? (
              <>
                <ThemeToggle />
                <Link
                  href="/dashboard/profile"
                  className="w-10 h-10 rounded-full bg-blue-500/20 dark:bg-indigo-500/20 flex items-center justify-center hover:bg-blue-500/30 dark:hover:bg-indigo-500/30 transition-colors border border-slate-200 dark:border-slate-700"
                  title="Profile"
                >
                  <UserCircle className="text-blue-600 dark:text-indigo-400 hover:text-blue-700 dark:hover:text-indigo-300" size={24} />
                </Link>
              </>
            ) : (
              <>
                <ThemeToggle />
                <Link
                  href="/login"
                  className="rounded-lg bg-blue-50 dark:bg-indigo-900/20 px-4 py-2 text-[#051df5] dark:text-indigo-300 border border-blue-200 dark:border-indigo-500/50 hover:bg-[#051df5] dark:hover:bg-indigo-500 hover:text-white hover:shadow-[0_0_20px_rgba(5,29,245,0.4)] dark:shadow-[0_0_20px_rgba(99,102,241,0.4)] hover:scale-105 transition-all duration-300"
                >
                  Login
                </Link>
                <Link
                  href="/register"
                  className="rounded-lg bg-blue-50 dark:bg-indigo-900/20 px-6 py-2 text-[#051df5] dark:text-indigo-300 border border-blue-200 dark:border-indigo-500/50 hover:bg-[#051df5] dark:hover:bg-indigo-500 hover:text-white hover:shadow-[0_0_20px_rgba(5,29,245,0.4)] dark:shadow-[0_0_20px_rgba(99,102,241,0.4)] hover:scale-105 transition-all duration-300"
                >
                  Register
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button - Show User Avatar for Authenticated Users */}
          {isAuthenticated ? (
            <button
              className="rounded-lg p-2 text-slate-700 hover:text-blue-600 md:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              title="Menu"
            >
              {mounted ? (
                <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center border border-slate-200">
                  <UserCircle className="text-blue-600 hover:text-blue-700" size={24} />
                </div>
              ) : (
                <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center border border-slate-200" />
              )}
            </button>
          ) : (
            <button
              className="rounded-lg p-2 text-slate-700 dark:text-slate-200 hover:text-blue-600 dark:hover:text-indigo-400 md:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          )}
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 pb-4 md:hidden"
          >
            <div className="bg-white/80 dark:bg-[#020617]/80 backdrop-blur-md rounded-xl p-4 border border-slate-200 dark:border-slate-700 shadow-lg dark:shadow-lg dark:shadow-indigo-500/20">
              {/* User Header with Glowing Border */}
              {isAuthenticated && (
                <div className="border border-blue-500/50 dark:border-indigo-500/50 rounded-lg p-3 mb-4 bg-blue-50 dark:bg-indigo-900/20">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center border border-slate-200">
                      <UserCircle className="text-blue-600" size={24} />
                    </div>
                    <div>
                      <p className="font-medium text-slate-900 dark:text-slate-200">{user?.name || user?.username || (user?.email ? user.email.split('@')[0] : 'User')}</p>
                      <p className="text-sm text-slate-600 dark:text-slate-400">{user?.email || 'Email'}</p>
                    </div>
                  </div>
                </div>
              )}

              <div className="flex flex-col space-y-3">
                {isAuthenticated ? (
                  <>
                    {/* Navigation Links */}
                    <Link
                      href="/dashboard"
                      className={`flex items-center gap-3 p-3 rounded-lg transition-all duration-300 border border-slate-200 dark:border-slate-700 ${
                        pathname === '/dashboard'
                          ? 'bg-blue-50 dark:bg-indigo-900/30 border border-blue-500 dark:border-indigo-500 text-blue-600 dark:text-indigo-300'
                          : 'hover:bg-slate-100 dark:hover:bg-slate-700 hover:text-blue-600 dark:hover:text-indigo-400 text-slate-700 dark:text-slate-200'
                      }`}
                      onClick={() => setIsMenuOpen(false)}
                    >
                      <LayoutDashboard size={18} className="text-blue-600 dark:text-indigo-400" />
                      <span>Dashboard</span>
                    </Link>

                    <Link
                      href="/dashboard/profile"
                      className={`flex items-center gap-3 p-3 rounded-lg transition-all duration-300 border border-slate-200 dark:border-slate-700 ${
                        pathname === '/dashboard/profile'
                          ? 'bg-blue-50 dark:bg-indigo-900/30 border border-blue-500 dark:border-indigo-500 text-blue-600 dark:text-indigo-300'
                          : 'hover:bg-slate-100 dark:hover:bg-slate-700 hover:text-blue-600 dark:hover:text-indigo-400 text-slate-700 dark:text-slate-200'
                      }`}
                      onClick={() => setIsMenuOpen(false)}
                    >
                      <UserCircle size={18} className="text-blue-600 dark:text-indigo-400" />
                      <span>Profile</span>
                    </Link>

                    <Link
                      href="/dashboard/settings"
                      className={`flex items-center gap-3 p-3 rounded-lg transition-all duration-300 border border-slate-200 dark:border-slate-700 ${
                        pathname === '/dashboard/settings'
                          ? 'bg-blue-50 dark:bg-indigo-900/30 border border-blue-500 dark:border-indigo-500 text-blue-600 dark:text-indigo-300'
                          : 'hover:bg-slate-100 dark:hover:bg-slate-700 hover:text-blue-600 dark:hover:text-indigo-400 text-slate-700 dark:text-slate-200'
                      }`}
                      onClick={() => setIsMenuOpen(false)}
                    >
                      <Settings size={18} className="text-blue-600 dark:text-indigo-400" />
                      <span>Settings</span>
                    </Link>

                    {/* Theme Toggle */}
                    <div className="flex items-center gap-3 p-3 text-slate-700 dark:text-slate-200 text-left">
                      <ThemeToggle />
                      <span>Theme</span>
                    </div>

                    {/* Logout Button */}
                    <button
                      onClick={() => {
                        logout();
                        setIsMenuOpen(false);
                      }}
                      className="flex items-center gap-3 p-3 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/30 hover:text-red-600 dark:hover:text-red-400 transition-transform duration-300 scale-100 hover:scale-105 text-red-600 dark:text-red-400 text-left mt-2 border border-slate-200 dark:border-slate-700"
                    >
                      <LogOut size={18} />
                      <span>Logout</span>
                    </button>
                  </>
                ) : (
                  <>
                    <div className="flex items-center gap-3 p-3 text-slate-700 dark:text-slate-200 text-left">
                      <ThemeToggle />
                      <span>Theme</span>
                    </div>
                    <div className="flex flex-col space-y-3 pt-4">
                      <Link
                        href="/login"
                        className="rounded-lg bg-blue-50 dark:bg-indigo-900/20 px-4 py-2 text-[#051df5] dark:text-indigo-300 border border-blue-200 dark:border-indigo-500/50 hover:bg-[#051df5] dark:hover:bg-indigo-500 hover:text-white hover:shadow-[0_0_20px_rgba(5,29,245,0.4)] dark:shadow-[0_0_20px_rgba(99,102,241,0.4)] hover:scale-105 transition-all duration-300 text-center"
                        onClick={() => setIsMenuOpen(false)}
                      >
                        Login
                      </Link>
                      <Link
                        href="/register"
                        className="rounded-lg bg-blue-50 dark:bg-indigo-900/20 px-6 py-2 text-[#051df5] dark:text-indigo-300 border border-blue-200 dark:border-indigo-500/50 hover:bg-[#051df5] dark:hover:bg-indigo-500 hover:text-white hover:shadow-[0_0_20px_rgba(5,29,245,0.4)] dark:shadow-[0_0_20px_rgba(99,102,241,0.4)] hover:scale-105 transition-all duration-300 text-center"
                        onClick={() => setIsMenuOpen(false)}
                      >
                        Register
                      </Link>
                    </div>
                  </>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </nav>
  );
};

export default GlassyNavbar;