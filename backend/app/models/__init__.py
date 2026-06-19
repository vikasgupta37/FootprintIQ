from app.core.database import Base
from app.models.user import User
from app.models.carbon import CarbonFootprint, CarbonCategory
from app.models.conversation import Conversation, Message
from app.models.gamification import Badge, UserAchievement, Challenge, UserChallenge, Leaderboard
from app.models.recommendation import Recommendation, RecommendationAction
from app.models.extras import (
    EcoTwinState,
    EcoTwinSimulation,
    LearningContent,
    Quiz,
    QuizAttempt,
    UserAnalytics,
    SustainabilityReport,
    AuditLog,
)

__all__ = [
    "Base",
    "User",
    "CarbonFootprint",
    "CarbonCategory",
    "Conversation",
    "Message",
    "Badge",
    "UserAchievement",
    "Challenge",
    "UserChallenge",
    "Leaderboard",
    "Recommendation",
    "RecommendationAction",
    "EcoTwinState",
    "EcoTwinSimulation",
    "LearningContent",
    "Quiz",
    "QuizAttempt",
    "UserAnalytics",
    "SustainabilityReport",
    "AuditLog",
]
