from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from typing import Union

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Allow static files for documentation without strict CSP
        if request.url.path.startswith('/docs') or request.url.path.startswith('/redoc') or request.url.path.startswith('/openapi.json'):
            response: Response = await call_next(request)

            # Apply relaxed security headers for documentation endpoints
            response.headers.setdefault("X-Content-Type-Options", "nosniff")
            response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")  # Allow framing for Swagger UI
            response.headers.setdefault("X-XSS-Protection", "1; mode=block")
            response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")

            # More permissive CSP for documentation
            response.headers.setdefault(
                "Content-Security-Policy",
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
                "img-src 'self' data: blob: https://fastapi.tiangolo.com https://cdn.jsdelivr.net; "
                "font-src 'self' https://cdn.jsdelivr.net; "
                "connect-src 'self' https://cdn.jsdelivr.net; "
                "media-src 'self';"
            )

            response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
            response.headers.setdefault("X-Download-Options", "noopen")
            response.headers.setdefault("X-Permitted-Cross-Domain-Policies", "none")

            return response
        else:
            # Apply strict security headers for API endpoints
            response: Response = await call_next(request)

            # Prevent MIME-type sniffing
            response.headers.setdefault("X-Content-Type-Options", "nosniff")

            # Prevent page from loading in a frame to prevent clickjacking
            response.headers.setdefault("X-Frame-Options", "DENY")

            # Basic XSS protection
            response.headers.setdefault("X-XSS-Protection", "1; mode=block")

            # Strict transport security
            response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")

            # Content Security Policy - Allow CDN resources for Swagger UI
            response.headers.setdefault(
                "Content-Security-Policy",
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
                "img-src 'self' data: https://fastapi.tiangolo.com https://cdn.jsdelivr.net; "
                "font-src 'self' https://cdn.jsdelivr.net; "
                "connect-src 'self';"
            )

            # Referrer policy
            response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")

            # Prevent IE from opening downloads in the browser
            response.headers.setdefault("X-Download-Options", "noopen")

            # Disallow embedding in other sites
            response.headers.setdefault("X-Permitted-Cross-Domain-Policies", "none")

            return response