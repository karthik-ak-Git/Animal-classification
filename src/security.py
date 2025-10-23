"""Security middleware for API rate limiting and authentication"""
import time
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


# API Key authentication
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Store valid API keys (in production, use database or environment variables)
VALID_API_KEYS = {
    "dev-key-12345": {"name": "Development", "rate_limit": 1000},
    "prod-key-67890": {"name": "Production", "rate_limit": 100},
}


async def get_api_key(api_key: str = Security(api_key_header)) -> Optional[str]:
    """Validate API key"""
    if api_key in VALID_API_KEYS:
        return api_key
    return None


def require_api_key(api_key: str = Security(api_key_header)):
    """Require valid API key for protected endpoints"""
    if not api_key or api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return api_key


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""

    def __init__(self, app, calls: int = 100, period: int = 60):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            calls: Maximum number of calls allowed
            period: Time period in seconds
        """
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        """Process each request"""
        # Get client identifier (IP address)
        client_ip = request.client.host

        # Clean old requests
        now = time.time()
        self.requests[client_ip] = [
            req_time
            for req_time in self.requests[client_ip]
            if now - req_time < self.period
        ]

        # Check rate limit
        if len(self.requests[client_ip]) >= self.calls:
            return HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Max {self.calls} requests per {self.period} seconds.",
            )

        # Add current request
        self.requests[client_ip].append(now)

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.calls)
        response.headers["X-RateLimit-Remaining"] = str(
            self.calls - len(self.requests[client_ip])
        )
        response.headers["X-RateLimit-Reset"] = str(int(now + self.period))

        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers[
            "Strict-Transport-Security"
        ] = "max-age=31536000; includeSubDomains"

        # Content Security Policy - allow CDNs, inline styles, and data URIs for frontend
        # Note: 'unsafe-inline' is needed for inline event handlers and styles
        # Consider refactoring to remove inline handlers for better security
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
            "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
            "img-src 'self' data: blob:; "
            "connect-src 'self'"
        )

        return response


def validate_file_upload(
    file_size: int,
    file_type: str,
    max_size: int = 10 * 1024 * 1024,
    allowed_types: list = None,
) -> bool:
    """
    Validate uploaded files

    Args:
        file_size: Size of file in bytes
        file_type: MIME type of file
        max_size: Maximum allowed file size
        allowed_types: List of allowed MIME types

    Returns:
        bool: True if valid, raises HTTPException if invalid
    """
    if allowed_types is None:
        allowed_types = ["image/jpeg", "image/png", "image/jpg"]

    # Check file size
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {max_size / (1024*1024)}MB",
        )

    # Check file type
    if file_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type not supported. Allowed types: {', '.join(allowed_types)}",
        )

    return True


def sanitize_filename(filename: str) -> str:
    """Sanitize uploaded filename to prevent directory traversal"""
    import re
    import os

    # Remove directory components
    filename = os.path.basename(filename)

    # Remove special characters except dots, dashes, underscores
    filename = re.sub(r"[^\w\s.-]", "", filename)

    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:250] + ext

    return filename
