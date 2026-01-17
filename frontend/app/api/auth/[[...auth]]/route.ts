import { auth } from "@/src/lib/auth"; // Adjust the import path as needed
import { toNextJsHandler } from "better-auth/next-js";

// This API route handles all Better Auth requests
export const { GET, POST } = toNextJsHandler(auth);