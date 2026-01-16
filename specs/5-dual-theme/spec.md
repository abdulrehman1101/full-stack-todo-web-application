# Dual Theme System Specification

## Overview

Implement a dual-theme system that allows users to switch between Light Mode (current design) and Dark Mode (legacy Midnight Cyber-Pro theme). The system will leverage next-themes with Tailwind's dark mode strategy to provide a seamless user experience with proper hydration handling.

## Theme Definitions

### Light Mode (Active Design)
- Background: White (#FFFFFF)
- Accents: Deep Blue (#051df5)
- Typography: Slate

### Dark Mode (Legacy Midnight Cyber-Pro)
- Background: Midnight Blue (#020617)
- Accents: Indigo (#6366f1)
- Glows: Cyan (#22d3ee)

## Technical Strategy

### Theme Management
- Integrate `next-themes` library for theme switching
- Configure Tailwind with `darkMode: 'class'` strategy
- Implement proper hydration mismatch prevention using mounted state checks
- Store user theme preference in localStorage

### Color Refactoring
- Replace hardcoded colors with dynamic Tailwind classes
- Use `dark:` variant for all theme-dependent styling
- Example: `bg-white` becomes `bg-white dark:bg-[#020617]`
- Example: `text-gray-900` becomes `text-gray-900 dark:text-white`

### Component Updates Required

#### Layout Components
- **Global Background Transitions**: Update root layout backgrounds to transition between themes
- **Dashboard Layout**: Modify background from white to midnight blue in dark mode

#### Navigation Components
- **Navbar & Sidebar**:
  - Light: White/Blue theme with deep blue accents
  - Dark: Midnight/Indigo-Cyan theme with glassmorphism effect
  - Maintain consistent styling patterns across both modes

#### Dashboard Components
- **Action Cards**:
  - Light: Solid Deep Blue cards (#051df5)
  - Dark: Translucent Midnight cards with Indigo borders and glassmorphism
  - Preserve shadow effects with theme-appropriate colors

#### Form Components
- **Inputs/Forms**:
  - Light: White backgrounds with Black borders
  - Dark: Translucent backgrounds with Blue-glow borders
  - Maintain proper contrast ratios in both themes

#### Settings Components
- **Theme Toggle Component**:
  - Implement proper hydration handling with mounted state check
  - Display appropriate icon for each theme (sun/moon icons)
  - Smooth transition between theme changes

#### Profile Components
- **Profile Cards**:
  - Light: Deep Blue backgrounds (#051df5) with blue shadows
  - Dark: Midnight Blue backgrounds (#020617) with indigo shadows
  - Maintain consistent card styling across both themes

#### Task Components
- **Task Cards**:
  - Light: White backgrounds with black text
  - Dark: Translucent backgrounds with appropriate text contrast
  - Preserve interactive states (hover, active, completed)

## User Scenarios

### Scenario 1: Theme Switching
- User navigates to settings page
- User clicks on theme toggle button
- System smoothly transitions between light and dark themes
- User preference is saved and persists across sessions

### Scenario 2: First-Time Visit
- User visits the application for the first time
- System detects user's preferred OS theme
- System defaults to user's preferred theme or falls back to light mode
- User can manually override the default in settings

### Scenario 3: Theme Persistence
- User sets theme preference
- User closes browser and returns later
- System remembers user's theme preference
- Application loads with previously selected theme

## Functional Requirements

### FR-001: Theme Storage
- The system SHALL store user theme preference in localStorage
- The system SHALL persist theme preference across browser sessions
- The system SHALL respect user's OS-level theme preference as default

### FR-002: Theme Switching
- The system SHALL provide a toggle mechanism to switch between light and dark themes
- The system SHALL apply theme changes immediately upon selection
- The system SHALL maintain all interactive states during theme transitions

### FR-003: Visual Consistency
- All components SHALL render appropriately in both light and dark themes
- Text contrast ratios SHALL meet WCAG accessibility standards in both themes
- Interactive elements SHALL maintain consistent hover, focus, and active states across themes

### FR-004: Hydration Handling
- The system SHALL prevent hydration mismatch errors during theme switching
- The ThemeToggle component SHALL use mounted state check before rendering
- The system SHALL handle server-side rendering appropriately for theme context

### FR-005: Performance
- Theme switching SHALL occur with minimal performance impact
- The system SHALL cache theme-related computations where appropriate
- CSS bundle size SHALL not increase significantly with dual-theme implementation

## Success Criteria

### Quantitative Measures
- Theme switching completes within 100ms after user interaction
- All components maintain acceptable contrast ratios (4.5:1 for normal text, 3:1 for large text)
- Zero hydration mismatch errors reported in console during theme switching
- Less than 5KB increase in CSS bundle size after implementation

### Qualitative Measures
- Users can seamlessly switch between themes without jarring visual transitions
- All interactive elements maintain visual feedback consistency across themes
- Theme preference persists reliably across sessions and browser restarts
- Application maintains professional appearance in both light and dark modes

## Key Entities

### Theme Context
- Current theme state (light/dark/system)
- Theme change event handlers
- Theme persistence mechanisms

### Theme Toggle Component
- User interface element for theme switching
- Hydration-safe rendering logic
- Visual indicators for current theme

### Theme Configuration
- Tailwind CSS dark mode configuration
- Theme color mappings
- Component-specific theme variants

## Constraints and Assumptions

### Assumptions
- Users have JavaScript enabled for theme switching functionality
- Modern browsers support CSS variables and Tailwind's dark mode
- Existing components can be refactored to support dual themes without major rewrites
- Color contrast ratios can be maintained in both themes without compromising design

### Constraints
- Implementation must not break existing functionality in light mode
- Theme switching must be accessible to users with disabilities
- Performance impact must be minimal
- Solution must work across all supported browsers

## Dependencies

- `next-themes` library for theme management
- Tailwind CSS configured with dark mode support
- Existing component structure that supports Tailwind class variants