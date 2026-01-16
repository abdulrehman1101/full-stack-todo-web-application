'use client';

import { useState, useEffect } from 'react';
import { Bell, Shield, Palette, Mail, Smartphone } from 'lucide-react';
import DashboardLayout from '@/src/components/dashboard/DashboardLayout';
import { useTheme } from 'next-themes';

const SettingsPage = () => {
  const { theme, setTheme } = useTheme();
  const [notifications, setNotifications] = useState({
    email: true,
    push: false,
    sms: true,
  });

  const [appearance, setAppearance] = useState({
    theme: 'system', // Default to system theme
    accentColor: 'indigo',
    density: 'comfortable',
  });

  // Initialize appearance state from theme context and localStorage
  useEffect(() => {
    const savedAccentColor = localStorage.getItem('accent-color');
    const savedDensity = localStorage.getItem('ui-density');

    if (savedAccentColor) {
      setAppearance(prev => ({
        ...prev,
        accentColor: savedAccentColor
      }));
    }

    if (savedDensity) {
      setAppearance(prev => ({
        ...prev,
        density: savedDensity
      }));
    }
  }, []);

  // Update theme context when appearance theme changes
  useEffect(() => {
    setTheme(appearance.theme);
  }, [appearance.theme, setTheme]);

  const handleNotificationToggle = (type: keyof typeof notifications) => {
    setNotifications(prev => ({
      ...prev,
      [type]: !prev[type]
    }));
  };

  return (
    <DashboardLayout>
      <div className="p-6 max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-white dark:text-slate-200 mb-8 glow-text">Settings</h1>

        {/* Appearance Settings */}
        <div className="rounded-2xl p-8 border border-white/10 bg-[#051df5] dark:bg-[#020617]/50 dark:border-indigo-500/50 shadow-lg shadow-blue-500/20 dark:shadow-[0_0_15px_rgba(34,211,238,0.3)] mb-8">
          <div className="flex items-center gap-3 mb-6">
            <Palette className="text-cyan-400 dark:text-cyan-400" size={24} />
            <h2 className="text-2xl font-semibold text-white dark:text-slate-200">Appearance</h2>
          </div>

          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-white dark:text-slate-200 mb-3">Theme</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {[
                  { id: 'dark', label: 'Dark', desc: 'Dark theme' },
                  { id: 'light', label: 'Light', desc: 'Light theme' },
                  { id: 'system', label: 'System', desc: 'Match system preference' }
                ].map((themeOption) => (
                  <button
                    key={themeOption.id}
                    onClick={() => {
                      setTheme(themeOption.id);
                      setAppearance(prev => ({ ...prev, theme: themeOption.id }));
                    }}
                    className={`p-4 rounded-lg border transition-all ${
                      appearance.theme === themeOption.id
                        ? 'border-cyan-400 bg-cyan-400/10 dark:border-cyan-400 dark:bg-cyan-900/20'
                        : 'border-white/20 bg-white/10 hover:border-white/40 dark:border-slate-600/50 dark:bg-slate-900/20 dark:hover:border-slate-500/50'
                    }`}
                  >
                    <div className="font-medium text-white dark:text-slate-200">{themeOption.label}</div>
                    <div className="text-sm text-white/70 dark:text-slate-300/70 mt-1">{themeOption.desc}</div>
                  </button>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-lg font-medium text-white dark:text-slate-200 mb-3">Accent Color</h3>
              <div className="flex flex-wrap gap-3">
                {[
                  { id: 'indigo', label: 'Indigo', color: 'bg-indigo-500' },
                  { id: 'cyan', label: 'Cyan', color: 'bg-cyan-400' },
                  { id: 'purple', label: 'Purple', color: 'bg-purple-500' },
                  { id: 'emerald', label: 'Emerald', color: 'bg-emerald-500' },
                  { id: 'amber', label: 'Amber', color: 'bg-amber-500' }
                ].map((color) => (
                  <button
                    key={color.id}
                    onClick={() => {
                      const newAccentColor = color.id;
                      setAppearance(prev => ({ ...prev, accentColor: newAccentColor }));
                      localStorage.setItem('accent-color', newAccentColor);
                    }}
                    className={`w-10 h-10 rounded-full ${color.color} ${
                      appearance.accentColor === color.id ? 'ring-2 ring-offset-2 ring-white dark:ring-slate-200 ring-offset-[#051df5] dark:ring-offset-[#020617]' : 'ring-1 ring-white/30 dark:ring-slate-600/50'
                    }`}
                    title={color.label}
                  />
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-lg font-medium text-white dark:text-slate-200 mb-3">Density</h3>
              <div className="flex gap-4">
                {[
                  { id: 'compact', label: 'Compact', desc: 'More content per screen' },
                  { id: 'comfortable', label: 'Comfortable', desc: 'Balanced spacing' },
                  { id: 'spacious', label: 'Spacious', desc: 'More breathing room' }
                ].map((density) => (
                  <button
                    key={density.id}
                    onClick={() => {
                      const newDensity = density.id;
                      setAppearance(prev => ({ ...prev, density: newDensity }));
                      localStorage.setItem('ui-density', newDensity);
                    }}
                    className={`px-4 py-2 rounded-lg border transition-all ${
                      appearance.density === density.id
                        ? 'bg-white dark:bg-slate-800 text-black dark:text-slate-200 border border-black dark:border-slate-600'
                        : 'border-white/20 text-white dark:text-slate-200 hover:bg-white/10 dark:hover:bg-slate-700/50'
                    }`}
                  >
                    <div className="font-medium">{density.label}</div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Account Security */}
        <div className="rounded-2xl p-8 border border-white/10 bg-[#051df5] dark:bg-[#020617]/50 dark:border-indigo-500/50 shadow-lg shadow-blue-500/20 dark:shadow-[0_0_15px_rgba(34,211,238,0.3)] mb-8">
          <div className="flex items-center gap-3 mb-6">
            <Shield className="text-cyan-400 dark:text-cyan-400" size={24} />
            <h2 className="text-2xl font-semibold text-white dark:text-slate-200">Account Security</h2>
          </div>

          <div className="space-y-4">
            <div className="p-4 bg-white/10 dark:bg-slate-900/20 rounded-lg border border-white/20 dark:border-slate-600/50">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="font-medium text-white dark:text-slate-200">Change Password</h3>
                  <p className="text-sm text-white/70 dark:text-slate-300/70">Last changed 3 months ago</p>
                </div>
                <button className="px-4 py-2 bg-white dark:bg-slate-800 text-[#051df5] dark:text-slate-200 border border-blue-200 dark:border-slate-600 font-semibold rounded-lg hover:bg-[#051df5] dark:hover:bg-[#051df5] hover:text-white dark:hover:text-white hover:scale-105 hover:shadow-[0_0_20px_rgba(5,29,245,0.4)] transition-all duration-300">
                  Change
                </button>
              </div>
            </div>

            <div className="p-4 bg-white/10 dark:bg-slate-900/20 rounded-lg border border-white/20 dark:border-slate-600/50">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="font-medium text-white dark:text-slate-200">Two-Factor Authentication</h3>
                  <p className="text-sm text-white/70 dark:text-slate-300/70">Add an extra layer of security</p>
                </div>
                <button className="px-4 py-2 bg-white dark:bg-slate-800 text-[#051df5] dark:text-slate-200 border border-blue-200 dark:border-slate-600 font-semibold rounded-lg hover:bg-[#051df5] dark:hover:bg-[#051df5] hover:text-white dark:hover:text-white hover:scale-105 hover:shadow-[0_0_20px_rgba(5,29,245,0.4)] transition-all duration-300">
                  Enable
                </button>
              </div>
            </div>

            <div className="p-4 bg-white/10 dark:bg-slate-900/20 rounded-lg border border-white/20 dark:border-slate-600/50">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="font-medium text-white dark:text-slate-200">Active Sessions</h3>
                  <p className="text-sm text-white/70 dark:text-slate-300/70">Manage devices where you're signed in</p>
                </div>
                <button className="px-4 py-2 bg-white dark:bg-slate-800 text-black dark:text-slate-200 border border-black dark:border-slate-600 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 hover:scale-105 transition-all duration-300">
                  Review
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Notifications */}
        <div className="rounded-2xl p-8 border border-white/10 bg-[#051df5] dark:bg-[#020617]/50 dark:border-indigo-500/50 shadow-lg shadow-blue-500/20 dark:shadow-[0_0_15px_rgba(34,211,238,0.3)]">
          <div className="flex items-center gap-3 mb-6">
            <Bell className="text-cyan-400 dark:text-cyan-400" size={24} />
            <h2 className="text-2xl font-semibold text-white dark:text-slate-200">Notifications</h2>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-white/10 dark:bg-slate-900/20 rounded-lg border border-white/20 dark:border-slate-600/50">
              <div className="flex items-center gap-3">
                <Mail className="text-cyan-400 dark:text-cyan-400" size={20} />
                <div>
                  <h3 className="font-medium text-white dark:text-slate-200">Email Notifications</h3>
                  <p className="text-sm text-white/70 dark:text-slate-300/70">Receive updates via email</p>
                </div>
              </div>
              <button
                onClick={() => handleNotificationToggle('email')}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  notifications.email ? 'bg-cyan-400' : 'bg-gray-600 dark:bg-slate-600'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    notifications.email ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>

            <div className="flex items-center justify-between p-4 bg-white/10 dark:bg-slate-900/20 rounded-lg border border-white/20 dark:border-slate-600/50">
              <div className="flex items-center gap-3">
                <Bell className="text-cyan-400 dark:text-cyan-400" size={20} />
                <div>
                  <h3 className="font-medium text-white dark:text-slate-200">Push Notifications</h3>
                  <p className="text-sm text-white/70 dark:text-slate-300/70">Get instant updates on your device</p>
                </div>
              </div>
              <button
                onClick={() => handleNotificationToggle('push')}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  notifications.push ? 'bg-cyan-400' : 'bg-gray-600 dark:bg-slate-600'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    notifications.push ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>

            <div className="flex items-center justify-between p-4 bg-white/10 dark:bg-slate-900/20 rounded-lg border border-white/20 dark:border-slate-600/50">
              <div className="flex items-center gap-3">
                <Smartphone className="text-cyan-400 dark:text-cyan-400" size={20} />
                <div>
                  <h3 className="font-medium text-white dark:text-slate-200">SMS Notifications</h3>
                  <p className="text-sm text-white/70 dark:text-slate-300/70">Receive critical alerts via SMS</p>
                </div>
              </div>
              <button
                onClick={() => handleNotificationToggle('sms')}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  notifications.sms ? 'bg-cyan-400' : 'bg-gray-600 dark:bg-slate-600'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    notifications.sms ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default SettingsPage;