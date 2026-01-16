import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Clean Enterprise Light theme
        'midnight-bg': '#FFFFFF',    // White background
        'cyber-accent': '#051df5',   // Deep Blue accent
        'cyber-glow': '#22d3ee',     // Cyan glow (unchanged)

        // Legacy Midnight Cyber-Pro Dark theme
        'midnight-bg-dark': '#020617',    // Midnight Blue background
        'cyber-accent-dark': '#6366f1',   // Indigo accent
        'cyber-glow-dark': '#22d3ee',     // Cyan glow
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
};
export default config;