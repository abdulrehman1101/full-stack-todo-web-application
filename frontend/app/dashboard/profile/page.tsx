'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/src/contexts/AuthContext';
import apiClient from '@/src/lib/api-client';
import DashboardLayout from '@/src/components/dashboard/DashboardLayout';

const ProfilePage = () => {
  const { user, loading, updateUser } = useAuth();
  const [name, setName] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    if (user) {
      setName(user.name || '');
      setUsername(user.username || '');
      setEmail(user.email || '');
    }
  }, [user]);

  const handleSave = async () => {
    setIsSaving(true);
    setSaveSuccess(false);

    try {
      // Update user profile via API
      const response = await apiClient.put('/me', {
        name,
        username,
        email,
      });

      // Update the auth context with new user data
      updateUser(response.data);

      setSaveSuccess(true);
      setIsEditing(false);
      setTimeout(() => setSaveSuccess(false), 3000); // Hide success message after 3 seconds
    } catch (error: any) {
      console.error('Failed to update profile:', error);
      if (error.response) {
        alert(`Failed to update profile: ${error.response.data.detail || 'Unknown error'}`);
      } else {
        alert('Failed to update profile. Please try again.');
      }
    } finally {
      setIsSaving(false);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center min-h-screen pb-20">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-400"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="p-6 max-w-3xl mx-auto pb-20">
        <h1 className="text-3xl font-bold text-white dark:text-slate-200 mb-8 glow-text">Profile Settings</h1>

        {saveSuccess && (
          <div className="mb-6 p-4 bg-green-500/20 dark:bg-green-900/30 border border-green-500/30 dark:border-green-500/50 rounded-lg text-green-300 dark:text-green-200">
            Profile updated successfully!
          </div>
        )}

        <div className="rounded-2xl p-8 border border-white/10 bg-[#051df5] dark:bg-[#020617]/50 dark:border-indigo-500/50 shadow-lg shadow-blue-500/20 dark:shadow-[0_0_15px_rgba(34,211,238,0.3)]">
          <div className="space-y-6">
            <div>
              <label className="block text-white dark:text-slate-200 text-sm font-medium mb-2">
                Name
              </label>
              {isEditing ? (
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  disabled={!isEditing}
                  className={`w-full px-4 py-3 rounded-lg ${
                    isEditing
                      ? 'bg-white dark:bg-slate-900/50 text-slate-950 dark:text-white border border-black dark:border-blue-500/50 placeholder:text-slate-400 dark:placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-500 focus:border-black dark:focus:border-blue-500'
                      : 'bg-transparent text-white dark:text-slate-200 border-none'
                  }`}
                />
              ) : (
                <div className="w-full px-4 py-2.5 rounded-lg bg-white/5 dark:bg-slate-900/30 border border-white/20 dark:border-slate-600/50 text-white dark:text-slate-200">
                  {name || 'Not provided'}
                </div>
              )}
            </div>

            <div>
              <label className="block text-white dark:text-slate-200 text-sm font-medium mb-2">
                Username
              </label>
              {isEditing ? (
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  disabled={!isEditing}
                  className={`w-full px-4 py-3 rounded-lg ${
                    isEditing
                      ? 'bg-white dark:bg-slate-900/50 text-slate-950 dark:text-white border border-black dark:border-blue-500/50 placeholder:text-slate-400 dark:placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-500 focus:border-black dark:focus:border-blue-500'
                      : 'bg-transparent text-white dark:text-slate-200 border-none'
                  }`}
                />
              ) : (
                <div className="w-full px-4 py-2.5 rounded-lg bg-white/5 dark:bg-slate-900/30 border border-white/20 dark:border-slate-600/50 text-white dark:text-slate-200">
                  {username || 'Not provided'}
                </div>
              )}
            </div>

            <div>
              <label className="block text-white dark:text-slate-200 text-sm font-medium mb-2">
                Email
              </label>
              {isEditing ? (
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={!isEditing}
                  className={`w-full px-4 py-3 rounded-lg ${
                    isEditing
                      ? 'bg-white dark:bg-slate-900/50 text-slate-950 dark:text-white border border-black dark:border-blue-500/50 placeholder:text-slate-400 dark:placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-500 focus:border-black dark:focus:border-blue-500'
                      : 'bg-transparent text-white dark:text-slate-200 border-none'
                  }`}
                />
              ) : (
                <div className="w-full px-4 py-2.5 rounded-lg bg-white/5 dark:bg-slate-900/30 border border-white/20 dark:border-slate-600/50 text-white dark:text-slate-200">
                  {email || 'Not provided'}
                </div>
              )}
            </div>

            <div className="pt-4 flex space-x-4">
              {!isEditing ? (
                <button
                  onClick={() => setIsEditing(true)}
                  className="px-6 py-3 bg-white dark:bg-slate-800 text-[#051df5] dark:text-slate-200 border border-blue-200 dark:border-slate-600 font-semibold rounded-lg hover:bg-[#051df5] dark:hover:bg-[#051df5] hover:text-white dark:hover:text-white hover:scale-105 hover:shadow-[0_0_20px_rgba(5,29,245,0.4)] transition-all duration-300"
                >
                  Edit Profile
                </button>
              ) : (
                <>
                  <button
                    onClick={handleSave}
                    disabled={isSaving}
                    className="px-6 py-3 bg-white dark:bg-slate-800 text-[#051df5] dark:text-slate-200 border border-blue-200 dark:border-slate-600 font-semibold rounded-lg hover:bg-[#051df5] dark:hover:bg-[#051df5] hover:text-white dark:hover:text-white hover:scale-105 hover:shadow-[0_0_20px_rgba(5,29,245,0.4)] transition-all duration-300 disabled:opacity-50"
                  >
                    {isSaving ? 'Saving...' : 'Save Changes'}
                  </button>
                  <button
                    onClick={() => {
                      setIsEditing(false);
                      // Reset to original values
                      setName(user?.name || '');
                      setUsername(user?.username || '');
                      setEmail(user?.email || '');
                    }}
                    className="px-6 py-3 bg-white dark:bg-slate-800 text-black dark:text-slate-200 border border-black dark:border-slate-600 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 hover:scale-105 transition-all duration-300"
                  >
                    Cancel
                  </button>
                </>
              )}
            </div>
          </div>

          <div className="mt-8 pt-8 border-t border-white/30 dark:border-slate-600/50">
            <h2 className="text-xl font-semibold text-white dark:text-slate-200 mb-4">Account Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-white/10 dark:bg-slate-900/20 rounded-lg border border-white/20 dark:border-slate-600/50">
                <p className="text-white/70 dark:text-slate-300 text-sm">Member Since</p>
                <p className="text-white dark:text-slate-200">
                  {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'Unknown'}
                </p>
              </div>
              <div className="p-4 bg-white/10 dark:bg-slate-900/20 rounded-lg border border-white/20 dark:border-slate-600/50">
                <p className="text-white/70 dark:text-slate-300 text-sm">User ID</p>
                <p className="text-white dark:text-slate-200">{user?.id}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default ProfilePage;