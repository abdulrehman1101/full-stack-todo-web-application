# Dual Theme System Implementation Plan

## Overview
This plan outlines the step-by-step implementation of the dual-theme system to enable Dark Mode while preserving the current Light Mode. The implementation will follow the specifications defined in spec.md and ensure a seamless user experience with proper hydration handling.

## Phase 1: Foundation & Configuration

### Task 1: Install and Configure next-themes
- Install the `next-themes` package as a dependency
- Verify installation and compatibility with current Next.js version
- Document the package usage and configuration options

### Task 2: Update Tailwind Configuration
- Modify `tailwind.config.ts` to enable `darkMode: 'class'`
- Configure theme extensions to support both light and dark mode color schemes
- Test Tailwind compilation to ensure dark mode classes are processed correctly

### Task 3: Integrate ThemeProvider in Root Layout
- Update `app/layout.tsx` to wrap the application with `ThemeProvider`
- Configure ThemeProvider with default theme and storage options
- Verify ThemeProvider initialization and context propagation

## Phase 2: Global Style Refactoring

### Task 4: Refactor globals.css for Theme Support
- Define CSS variables for both light and dark color palettes
- Light palette: Background #FFFFFF, Accent #051df5
- Dark palette: Background #020617, Accent #6366f1, Glow #22d3ee
- Update global styles to use theme-appropriate colors with dark: variants

### Task 5: Update Base Layout Backgrounds
- Modify root layout backgrounds to transition between themes
- Apply `dark:bg-[#020617]` alongside existing light mode backgrounds
- Ensure smooth transitions and consistent appearance across both themes

## Phase 3: Component Refactoring Strategy

### Task 6: Navigation Components (Navbar & Sidebar)
- Refactor Navbar from White/Blue theme to support Midnight/Indigo-Cyan in dark mode
- Apply `dark:bg-[#020617] dark:text-white dark:border-indigo-500` classes
- Add glassmorphism effect in dark mode with `dark:bg-white/10` and `dark:backdrop-blur-lg`
- Update Sidebar with consistent dark mode styling

### Task 7: Dashboard Cards Refactoring
- Transform solid Deep Blue cards (#051df5) to translucent Midnight cards in dark mode
- Apply `dark:bg-[#020617]/20 dark:border-indigo-500/50` for dark mode
- Add glassmorphism effect with `dark:backdrop-blur-md` in dark mode
- Preserve shadow effects with theme-appropriate colors

### Task 8: Form Components (Inputs & Forms)
- Refactor white inputs with black borders to dark/translucent inputs with blue-glow borders in dark mode
- Apply `dark:bg-gray-800/50 dark:text-white dark:border-blue-500/30` for dark mode
- Add glow effects with `dark:shadow-[0_0_15px_rgba(34,211,238,0.3)]` for active states
- Maintain proper contrast ratios in both themes

### Task 9: Profile Components
- Update Profile cards from Deep Blue backgrounds to Midnight Blue in dark mode
- Apply `dark:bg-[#020617] dark:shadow-indigo-500/20` for dark mode
- Refactor display containers with `dark:bg-white/5 dark:border-white/20`
- Maintain consistent styling across both themes

### Task 10: Task Components
- Transform Task cards from white backgrounds to translucent dark backgrounds
- Apply `dark:bg-white/5 dark:text-white dark:border-white/20` for dark mode
- Update completed task styling with `dark:text-white/50` for better contrast
- Preserve hover and active states with theme-appropriate colors

### Task 11: Settings Components
- Refactor Settings cards from glassmorphism to deep blue in light mode, and to midnight in dark mode
- Apply `dark:bg-[#020617] dark:shadow-indigo-500/20` for dark mode
- Update panel backgrounds with `dark:bg-white/10 dark:border-white/20`
- Maintain button styling consistency across themes

## Phase 4: Logic & Persistence

### Task 12: Theme Toggle Component Implementation
- Create or update ThemeToggle component to handle theme switching
- Implement proper mounted state check to prevent hydration errors
- Add appropriate icons for light (sun) and dark (moon) modes
- Ensure toggle functionality works in both Navbar and Settings pages

### Task 13: Theme Persistence Logic
- Configure localStorage persistence for user theme preference
- Implement system theme detection as fallback
- Add theme change event listeners for system preference updates
- Verify theme preference survives browser refreshes and sessions

### Task 14: Hydration Error Prevention
- Implement mounted state check in ThemeToggle component
- Use `useState` to track mount status before rendering theme-sensitive elements
- Add proper error boundaries to catch any remaining hydration issues
- Test SSR and CSR consistency across both themes

## Phase 5: Testing & Validation

### Task 15: Cross-Component Theme Consistency
- Verify all components render appropriately in both themes
- Test theme transitions across all pages and components
- Validate color contrast ratios meet WCAG accessibility standards
- Ensure interactive states (hover, focus, active) work consistently

### Task 16: Performance Validation
- Measure theme switching performance (should complete within 100ms)
- Verify CSS bundle size increase is minimal (<5KB)
- Test memory usage during theme transitions
- Confirm no performance regressions in either theme

### Task 17: User Experience Validation
- Test theme persistence across sessions
- Verify theme preference respects user's OS-level settings
- Ensure smooth transitions without flickering or jarring changes
- Validate all interactive elements maintain visual feedback

## Dependencies & Prerequisites
- Next.js 16+ with App Router
- Tailwind CSS configured and working
- `next-themes` package (to be installed)
- Existing component structure supporting Tailwind class variants

## Risk Mitigation
- Maintain backward compatibility with existing light mode
- Use progressive enhancement approach for dark mode features
- Thorough testing on different browsers and devices
- Graceful degradation if JavaScript is disabled