---
id: "004"
title: "Fix Hero Section Clean Split Layout"
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

# Fix Hero Section Clean Split Layout

## PROMPT_TEXT

The previous implementation was wrong. The image should NOT be the background of the whole section. I want a clean split layout.

Task 1: Remove Background Image

Remove bg-[url('/hero-bg.png')], bg-cover, and bg-center from the main section container.

Set the main section background to pure White (bg-white).

Task 2: Implement Split Layout (Grid)

Use a 2-column grid: grid grid-cols-1 lg:grid-cols-2.

Left Column (Image): Place the image /hero-bg.png here. Use an <img> tag with object-contain or object-cover so it's clearly visible ONLY on the left side.

Right Column (Text): Move the Heading, Subtitle, and 'Get Started' button here.

Task 3: Alignment & Spacing

Right Column: Center the content vertically using flex flex-col justify-center.

Text Alignment: Align all text to the Left within this right column (items-start text-left).

Ensure there is enough gap (gap-12) between the image and the text.

Height should remain min-h-[80vh] to min-h-screen.

Goal: When I open the page, I should see the Image on the left half and the Text/Buttons on the right half, with a clean white background.

## RESPONSE_TEXT

Successfully implemented the clean split layout for the Hero Section:

- Removed background image classes from main section container
- Set main section background to pure white (bg-white)
- Added gap-12 between columns for proper spacing
- Implemented 2-column grid layout (grid grid-cols-1 lg:grid-cols-2)
- Added img tag in left column with object-contain for proper image display
- Kept text content in right column with flex flex-col justify-center items-start alignment
- Maintained animations and button styling while reorganizing layout

The hero section now features a clean split layout with image on the left and text/buttons on the right, with a pure white background.

## EVALUATION

All requested changes have been successfully implemented:
- Background image removed from section container
- Pure white background applied
- Clean split layout with image on left and text on right
- Proper spacing with gap-12
- Vertical centering and left alignment maintained
- Responsive design preserved