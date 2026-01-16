import { auth } from "@/src/lib/auth"; // Adjust the import path as needed
import { handleAuth } from "better-auth/frameworks/next-js";

// This API route handles all Better Auth requests
export const { GET, POST } = handleAuth(auth);