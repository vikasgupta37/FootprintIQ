"""
Dependency Injection providers for Services.
These functions allow FastAPI to inject service instances into route handlers,
improving testability and adherence to SOLID principles.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.carbon_service import CarbonService
from app.services.user_service import UserService
from app.services.gamification_service import GamificationService
from app.services.recommendation_service import RecommendationService
from app.services.ecotwin_service import EcoTwinService
from app.services.report_service import ReportService
from app.services.ai_service import AIService


def get_carbon_service(db: AsyncSession = Depends(get_db)) -> CarbonService:
    """Provide CarbonService instance."""
    return CarbonService(db)


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """Provide UserService instance."""
    return UserService(db)


def get_gamification_service(db: AsyncSession = Depends(get_db)) -> GamificationService:
    """Provide GamificationService instance."""
    return GamificationService(db)


def get_recommendation_service(db: AsyncSession = Depends(get_db)) -> RecommendationService:
    """Provide RecommendationService instance."""
    return RecommendationService(db)


def get_ecotwin_service(db: AsyncSession = Depends(get_db)) -> EcoTwinService:
    """Provide EcoTwinService instance."""
    return EcoTwinService(db)


def get_report_service(db: AsyncSession = Depends(get_db)) -> ReportService:
    """Provide ReportService instance."""
    return ReportService(db)


def get_ai_service(db: AsyncSession = Depends(get_db)) -> AIService:
    """Provide AIService instance."""
    return AIService(db)
