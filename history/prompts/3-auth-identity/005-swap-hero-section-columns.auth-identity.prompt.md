---
id: "005"
title: "Swap Hero Section Columns Layout"
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

# Swap Hero Section Columns Layout

## PROMPT_TEXT

The split layout is working, but I want to swap the positions of the content and adjust the height.

Task 1: Swap Columns

In HeroSection.tsx, swap the content within the 2-column grid.

Left Column: Move the Text content (Heading, Subtitle, and 'Get Started' button) here. Align text to the Left (items-start text-left).

Right Column: Move the Image (/hero-bg.png) here.

Task 2: Reduce Section Height

Change the main container height from min-h-screen to a more compact min-h-[75vh] or min-h-[80vh].

Ensure the vertical padding is adjusted to keep the content centered: py-12 lg:py-16.

Task 3: Visual Polish

Ensure the image on the right uses object-contain so it doesn't get cut off.

Maintain the clean white background and the blue/black text contrast we established.

Goal: The final result should show the Text on the left and the Image on the right, with a balanced height that doesn't take up the entire screen.

## RESPONSE_TEXT

Successfully swapped the Hero Section columns layout:

- Moved text content (heading, subtitle, and button) to the left column
- Moved the image (/hero-bg.png) to the right column
- Reduced section height from min-h-screen to min-h-[75vh] lg:min-h-[80vh]
- Adjusted vertical padding to py-12 lg:py-16 for better centering
- Maintained object-contain for image to prevent cutoff
- Preserved clean white background and text contrast
- Aligned text to the left with items-start

The hero section now shows text content on the left and image on the right with a more compact height.

## EVALUATION

All requested changes have been successfully implemented:
- Columns swapped with text on left and image on right
- Section height reduced to min-h-[75vh] lg:min-h-[80vh]
- Vertical padding adjusted to py-12 lg:py-16
- Image uses object-contain for proper display
- Text alignment maintained with items-start
- Clean white background preserved