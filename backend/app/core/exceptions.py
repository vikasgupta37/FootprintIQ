"""
Global exception handling and custom error classes.
Provides consistent error response format across all API endpoints.
"""

from typing import Any, Dict, List, Optional

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


# ── Error Response Schema ────────────────────────────────────────

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: Optional[List[ErrorDetail]] = None
    request_id: Optional[str] = None


# ── Custom Exceptions ────────────────────────────────────────────

class AppException(HTTPException):
    """Base application exception with structured error response."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[List[Dict]] = None,
    ):
        self.code = code
        self.error_message = message
        self.details = details
        super().__init__(status_code=status_code, detail=message)


class NotFoundException(AppException):
    def __init__(self, resource: str = "Resource", resource_id: str = ""):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="NOT_FOUND",
            message=f"{resource} not found" + (f": {resource_id}" if resource_id else ""),
        )


class AuthenticationException(AppException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTHENTICATION_ERROR",
            message=message,
        )


class AuthorizationException(AppException):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="AUTHORIZATION_ERROR",
            message=message,
        )


class ValidationException(AppException):
    def __init__(self, message: str = "Validation error", details: Optional[List[Dict]] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="VALIDATION_ERROR",
            message=message,
            details=details,
        )


class ConflictException(AppException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="CONFLICT",
            message=message,
        )


class RateLimitException(AppException):
    def __init__(self, retry_after: int = 3600):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            code="RATE_LIMIT_EXCEEDED",
            message=f"Rate limit exceeded. Retry after {retry_after} seconds.",
        )


class AIServiceException(AppException):
    def __init__(self, message: str = "AI service unavailable"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            code="AI_SERVICE_ERROR",
            message=message,
        )


# ── Exception Handlers ──────────────────────────────────────────

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle custom application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.error_message,
                "details": exc.details,
            }
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions — log the error for debugging."""
    import logging

    logger = logging.getLogger("footprintiq")
    request_id = getattr(getattr(request, "state", None), "request_id", "unknown")
    logger.exception(
        "Unhandled exception [request_id=%s] %s: %s",
        request_id,
        type(exc).__name__,
        exc,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
            }
        },
    )
