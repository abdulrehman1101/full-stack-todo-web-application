"""
FastAPI Main Application for Todo Backend

This file defines the main FastAPI application with authentication middleware
and API routes for the todo application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .v1.endpoints.users import router as users_router
from .v1.endpoints.auth import router as auth_router
from .v1.endpoints.tasks import router as tasks_router
from ..config.settings import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app instance
app = FastAPI(
    title="Todo API",
    description="API for the Todo Application with Authentication",
    version="1.0.0",
)

# Add security headers via middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)

    # Add security headers to all responses
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data: https://fastapi.tiangolo.com; connect-src 'self' https://cdn.jsdelivr.net; frame-ancestors 'none'"

    return response

origins = [
    "http://localhost:3000",
    "https://abdulrehman2-todowebapp-backend.hf.space",
    "https://your-vercel-app-url.vercel.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include API routes
app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(tasks_router, prefix="/api/v1", tags=["tasks"])

@app.get("/")
@limiter.limit("100/minute")  # Rate limit for root endpoint
def read_root(request):
    """Root endpoint for the API."""
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
@limiter.limit("200/minute")  # Rate limit for health endpoint
def health_check(request):
    """Health check endpoint."""
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )