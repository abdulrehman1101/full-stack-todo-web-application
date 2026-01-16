/**
 * Better Auth configuration for the todo application.
 * This module configures Better Auth with JWT plugin for authentication.
 */

import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins/jwt";

// Initialize Better Auth with JWT plugin
const auth = betterAuth({
  database: {
    provider: "sqlite", // This will be updated when we connect to the real database
    url: process.env.DATABASE_URL || "file:./dev.db",
  },
  secret: process.env.NEXT_PUBLIC_BETTER_AUTH_SECRET || "ZUu822SMcByw8CNnTkOBe4NO5ElvkcCP",
  plugins: [
    jwt({
      secret: process.env.NEXT_PUBLIC_BETTER_AUTH_SECRET || "ZUu822SMcByw8CNnTkOBe4NO5ElvkcCP",
      expiresIn: "15m", // Token expires in 15 minutes
    }),
  ],
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // For MVP, we're not requiring email verification
  },
  account: {
    accountModel: {
      // Configuration for the account model
    }
  }
});

export default auth;