'use client';

import { useAuth } from '@/src/contexts/AuthContext';

const ProfileSettings = () => {
  const { user } = useAuth();

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-white dark:text-slate-200">Profile Settings</h1>

      <div className="glass p-6 rounded-xl">
        <div className="mb-6">
          <h2 className="text-lg font-semibold text-white dark:text-slate-200 mb-4">Account Information</h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 dark:text-slate-300 mb-1">Name</label>
              <p className="text-white dark:text-slate-200 bg-black/20 dark:bg-slate-900/50 p-3 rounded-lg">{user?.name || 'Not provided'}</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 dark:text-slate-300 mb-1">Email</label>
              <p className="text-white dark:text-slate-200 bg-black/20 dark:bg-slate-900/50 p-3 rounded-lg">{user?.email || 'Not provided'}</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 dark:text-slate-300 mb-1">User ID</label>
              <p className="text-white dark:text-slate-200 bg-black/20 dark:bg-slate-900/50 p-3 rounded-lg">{user?.id || 'Not provided'}</p>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-700 dark:border-slate-700 pt-6">
          <h2 className="text-lg font-semibold text-white dark:text-slate-200 mb-4">Security</h2>
          <div className="space-y-4">
            <button className="w-full md:w-auto glass px-4 py-2 rounded-lg text-white dark:text-slate-200 hover:bg-white/10 dark:hover:bg-slate-700/50 transition-colors">
              Change Password
            </button>
            <button className="w-full md:w-auto glass px-4 py-2 rounded-lg text-white dark:text-slate-200 hover:bg-white/10 dark:hover:bg-slate-700/50 transition-colors">
              Manage Two-Factor Authentication
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileSettings;