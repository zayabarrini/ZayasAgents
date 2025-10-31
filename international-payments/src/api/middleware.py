from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging
from typing import Callable


class SecurityHeadersMiddleware:
    def __init__(self):
        self.logger = logging.getLogger("SecurityHeadersMiddleware")

    async def __call__(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        response.headers["Content-Security-Policy"] = "default-src 'self'"

        return response


class LoggingMiddleware:
    def __init__(self):
        self.logger = logging.getLogger("APILogger")

    async def __call__(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        # Log request
        self.logger.info(f"Incoming request: {request.method} {request.url}")

        response = await call_next(request)

        # Log response
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        self.logger.info(
            f"Completed request: {request.method} {request.url} "
            f"Status: {response.status_code} Duration: {process_time:.2f}s"
        )

        return response


class RateLimitMiddleware:
    def __init__(self, rate_limiter):
        self.rate_limiter = rate_limiter
        self.logger = logging.getLogger("RateLimitMiddleware")

    async def __call__(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "0.0.0.0"

        try:
            # Check rate limit for all requests
            self.rate_limiter.check_limit(client_ip, "api_request")
        except Exception as e:
            self.logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            from fastapi import HTTPException

            raise HTTPException(
                status_code=429, detail="Rate limit exceeded. Please try again later."
            )

        response = await call_next(request)
        return response


def setup_middleware(app, rate_limiter):
    """Setup all middleware for the FastAPI application"""

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://yourdomain.com"],  # Configure appropriately
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )

    # Trusted hosts middleware
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=["yourdomain.com", "api.yourdomain.com"]
    )

    # Custom middleware
    security_middleware = SecurityHeadersMiddleware()
    logging_middleware = LoggingMiddleware()
    rate_limit_middleware = RateLimitMiddleware(rate_limiter)

    app.middleware("http")(security_middleware)
    app.middleware("http")(logging_middleware)
    app.middleware("http")(rate_limit_middleware)
