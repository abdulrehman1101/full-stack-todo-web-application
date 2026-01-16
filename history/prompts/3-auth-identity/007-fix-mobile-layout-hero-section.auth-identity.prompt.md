---
id: "007"
title: "Fix Mobile Layout in Hero Section"
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
  - "mobile"
  - "landing"
  - "hero"
  - "responsive"
files:
  - "frontend/src/components/landing/HeroSection.tsx"
tests: []
spec: "specs/3-auth-identity/spec.md"
ticket: null
adr: null
pr: null
---

# Fix Mobile Layout in Hero Section

## PROMPT_TEXT

The landing page looks great, but I need to fix the mobile layout in HeroSection.tsx as shown in 188.PNG.

Task 1: Re-order Elements for Mobile

In the 2-column grid, use Tailwind's order classes to swap the elements on mobile.

Image Container: Add order-first lg:order-last. This ensures the image is at the top on mobile but stays on the right on desktop.

Text Container: Add order-last lg:order-first. This puts the text below the image on mobile but keeps it on the left on desktop.

Task 2: Mobile Text Alignment

Ensure that on mobile (sm: or default), the heading, subtitle, and 'Get Started' button are Centered (text-center items-center).

On desktop (lg:), they should remain Left-aligned (lg:text-left lg:items-start).

Task 3: Spacing Polish

Add a gap between the image and text for mobile view: gap-10 lg:gap-16.

Make sure the image doesn't touch the navbar on mobile by adding some top padding (pt-10).

Goal: On a phone, the user should see the Hero Image first, then the text and button below it. On a laptop, the text should stay on the left and the image on the right.

## RESPONSE_TEXT

Successfully implemented all requested mobile layout changes:

Task 1: Re-ordered elements for mobile:
- Added order-first lg:order-last to image container
- Added order-last lg:order-first to text container
- On mobile: image appears first, text below
- On desktop: text remains on left, image on right

Task 2: Updated mobile text alignment:
- Added text-center and items-center for mobile
- Added lg:text-left lg:items-start for desktop
- Text and button are centered on mobile, left-aligned on desktop

Task 3: Applied spacing polish:
- Changed gap to gap-10 lg:gap-16 for mobile/desktop
- Added pt-10 to prevent image touching navbar on mobile
- Maintained proper spacing and padding for all devices

The mobile layout now shows the hero image first, followed by text and button, while preserving desktop layout.

## EVALUATION

All requested changes have been successfully implemented:
- Mobile elements reordered with Tailwind order classes
- Text alignment centered on mobile, left on desktop
- Proper spacing with gap-10 lg:gap-16
- Top padding added to prevent navbar overlap
- Responsive design maintained for all screen sizes