"""
V1 API Router — aggregates all endpoint modules.
"""

from fastapi import APIRouter

from app.api.v1 import auth, carbon, ai, recommendations, gamification, ecotwin, analytics, learning, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(carbon.router, prefix="/carbon", tags=["Carbon"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
api_router.include_router(gamification.router, prefix="/gamification", tags=["Gamification"])
api_router.include_router(ecotwin.router, prefix="/eco-twin", tags=["Eco Twin"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(learning.router, prefix="/learning", tags=["Learning"])
