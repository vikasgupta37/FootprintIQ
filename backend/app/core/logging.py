"""
Structured logging configuration for the application.
"""

import logging
import sys
from typing import Optional

from app.core.config import settings


def setup_logging(level: Optional[str] = None) -> logging.Logger:
    """Configure application-wide logging."""
    log_level = getattr(logging, (level or settings.LOG_LEVEL).upper(), logging.INFO)

    # Root logger
    logging.basicConfig(
        level=log_level,
        format=settings.LOG_FORMAT,
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Application logger
    logger = logging.getLogger("footprintiq")
    logger.setLevel(log_level)

    # Suppress noisy libraries
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    return logger


logger = setup_logging()
