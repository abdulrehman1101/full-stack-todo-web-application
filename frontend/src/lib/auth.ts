/**
 * Better Auth configuration for the todo application.
 * This module configures Better Auth with JWT plugin for authentication.
 */

import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins/jwt";

// Initialize Better Auth with JWT plugin
export const auth = betterAuth({
  database: {
    provider: process.env.NODE_ENV === "production" ? "postgres" : "sqlite", // Use postgres in production, sqlite otherwise
    url: process.env.DATABASE_URL || "file:./dev.db",
  },
  secret: process.env.BETTER_AUTH_SECRET || "ZUu822SMcByw8CNnTkOBe4NO5ElvkcCP",
  plugins: [
    jwt(),
  ],
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // For MVP, we're not requiring email verification
  }
});