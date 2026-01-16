---
id: "003"
title: "Redesign Hero Section with Background Image and Grid Layout"
stage: "red"
date: "2026-01-16"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "3-auth-identity"
branch: "3-auth-identity"
user: "user"
command: "/sp.implement"
labels:
  - "ui"
  - "landing"
  - "hero"
  - "design"
files:
  - "frontend/src/components/landing/HeroSection.tsx"
tests: []
spec: "specs/3-auth-identity/spec.md"
ticket: null
adr: null
pr: null
---

# Redesign Hero Section with Background Image and Grid Layout

## PROMPT_TEXT

I need to completely redesign the Hero Section on the landing page (frontend/src/components/landing/HeroSection.tsx).

Current State: Text and button are centered with a plain background. Desired State: Full-height section with a background image, and content pushed to the right side.

Task 1: Container Structure & Height

Update the main section container to have full screen height: min-h-screen (or at least min-h-[90vh]).

Change the internal layout to a 2-column grid on large screens: grid grid-cols-1 lg:grid-cols-2.

Add appropriate padding: px-6 lg:px-20 py-20.

Task 2: Background Image Implementation

Apply the background image located at /hero-bg.png (inside the public folder) to the main hero section container.

Use Tailwind arbitrary values for the background image: bg-[url('/hero-bg.png')] bg-cover bg-center bg-no-repeat.

Ensure the text remains readable against the image (you might need a subtle overlay gradient like bg-gradient-to-r from-white/90 to-white/50 depending on the image contrast). Let's try without an overlay first, but keep it in mind if text is hard to read.

Task 3: Content Alignment (Right Side)

Create an empty <div> for the left column (col-span-1) on large screens so the image shows through.

Place the existing Heading (<h1>), Subtitle (<p>), and "Get Started" button inside the right column <div>.

Align the content within this right column. On desktop (lg:), align items to the start (left-aligned text within the right block) and justify center vertically: flex flex-col justify-center items-start lg:pl-12.

Goal: The hero section should be tall, feature the hero-bg.png image across the entire background, and have the main text and button positioned prominently on the right half of the screen.

## RESPONSE_TEXT

Successfully redesigned the Hero Section with all requested features:

- Updated main section container to have full screen height (min-h-screen lg:min-h-[90vh])
- Implemented 2-column grid layout (grid grid-cols-1 lg:grid-cols-2) with appropriate padding
- Added background image using bg-[url('/hero-bg.png')] bg-cover bg-center bg-no-repeat
- Created empty left column (col-span-1) to show background image
- Positioned content in right column with flex flex-col justify-center items-start alignment
- Removed centering classes (mx-auto) to achieve left-aligned text
- Maintained animations and button styling while reorganizing layout

The hero section now features a full-height background image with content positioned prominently on the right half of the screen.

## EVALUATION

All requested changes have been successfully implemented:
- Full-height section with proper grid layout
- Background image applied correctly
- Content aligned to right side on large screens
- Left column empty to showcase background
- Text and button properly positioned and styled
- Responsive design maintained