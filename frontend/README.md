# Todo Application Frontend - Authentication & Identity

This is a [Next.js](https://nextjs.org) project with integrated authentication using Better Auth and JWT tokens, bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Authentication Setup

This application implements secure authentication with Better Auth and JWT tokens, integrated with the backend API for comprehensive security. Follow these steps to set up authentication:

1. **Configure environment variables**: Copy `.env.local.example` to `.env.local` and set your environment variables:
   ```bash
   # API Configuration
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

   # Better Auth Configuration
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
   BETTER_AUTH_URL=http://localhost:3000
   ```

2. **Production Environment**: For production deployments, copy `.env.production` and configure:
   ```bash
   # Production API Configuration
   NEXT_PUBLIC_API_BASE_URL=https://your-api-domain.com

   # Production Better Auth Configuration
   NEXT_PUBLIC_BETTER_AUTH_URL=https://your-domain.com
   BETTER_AUTH_URL=https://your-domain.com
   ```

3. **Set up Better Auth**: The authentication system is configured in `src/lib/auth.ts` with JWT plugin enabled.

4. **Authentication Components**: The application includes:
   - Login component: `src/components/auth/Login.tsx`
   - Register component: `src/components/auth/Register.tsx`
   - Protected Route component: `src/components/auth/ProtectedRoute.tsx`
   - Authentication hook: `src/hooks/useAuth.ts`

5. **Test authentication flow**:
   - Register a new account using the registration form
   - Login with your credentials
   - Access protected routes that require authentication
   - Verify JWT tokens are stored securely and used for API calls

6. **API Client Integration**: The API client in `src/services/api-client.ts` automatically attaches JWT tokens to requests and includes security headers.

7. **Security Features**:
   - Secure token storage in browser
   - Automatic token refresh and expiration handling
   - Protected route validation
   - Secure communication with backend API
   - CSRF protection through Better Auth

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
