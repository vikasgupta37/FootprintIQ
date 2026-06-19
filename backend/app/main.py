"""
FootprintIQ — FastAPI Application Entry Point.
AI-Powered Carbon Footprint Awareness Platform.
"""

import uuid as _uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.cache import cache
from app.core.config import settings
from app.core.database import init_db
from app.core.exceptions import AppException, app_exception_handler, generic_exception_handler
from app.core.logging import logger
from app.api.v1 import api_router


# ── Security Headers Middleware ──────────────────────────────────

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Inject standard security headers into every response."""

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )
        if settings.ENVIRONMENT != "development":
            response.headers["Strict-Transport-Security"] = (
                "max-age=63072000; includeSubDomains; preload"
            )
        return response


# ── Request‑ID Middleware ────────────────────────────────────────

class RequestIdMiddleware(BaseHTTPMiddleware):
    """Attach a unique request ID to each request/response for tracing."""

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(_uuid.uuid4()))
        request.state.request_id = request_id
        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


# ── Lifespan ─────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown lifecycle."""
    logger.info("Starting %s v%s", settings.PROJECT_NAME, settings.VERSION)

    # Connect Redis
    try:
        await cache.connect()
        logger.info("Redis connected")
    except Exception as e:
        logger.warning("Redis connection failed: %s — running without cache", e)

    # Initialize database (dev only)
    if settings.ENVIRONMENT == "development":
        from app import models  # noqa: F401
        try:
            await init_db()
            logger.info("Database tables initialized")
            try:
                from app.core.seed import seed_db
                from app.core.database import AsyncSessionLocal
                async with AsyncSessionLocal() as session:
                    await seed_db(session)
                logger.info("Database seeded successfully")
            except Exception as e:
                logger.warning("Database seeding failed: %s", e)
        except Exception as db_err:
            logger.warning(
                "Database connection failed: %s — running without active database connection",
                db_err,
            )

    yield

    # Shutdown
    await cache.disconnect()
    logger.info("Application shutdown complete")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Carbon Footprint Awareness Platform",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── Middleware (outermost first) ─────────────────────────────────

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Accept",
        "X-Request-ID",
    ],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# ── Exception Handlers ───────────────────────────────────────────

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# ── Routes ───────────────────────────────────────────────────────

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/")
async def root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
    }
