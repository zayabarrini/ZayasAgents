from fastapi import FastAPI, Depends
import logging
from contextlib import asynccontextmanager

from .api.routes import router as payment_router
from .api.middleware import setup_middleware
from .core.payment_processor import InternationalPaymentProcessor
from .services.rate_limiter import RateLimiter
from .utils.logger import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    logging.info("International Payment System starting up...")

    # Initialize services
    app.state.payment_processor = InternationalPaymentProcessor()
    app.state.rate_limiter = RateLimiter()

    yield

    # Shutdown
    logging.info("International Payment System shutting down...")


def create_application() -> FastAPI:
    """Create and configure FastAPI application"""

    app = FastAPI(
        title="International Payment System",
        description="Secure multi-currency international payment processing with AI agents",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Include routers
    app.include_router(payment_router)

    # Setup middleware
    setup_middleware(app, app.state.rate_limiter)

    return app


app = create_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Disable in production
        log_level="info",
    )
