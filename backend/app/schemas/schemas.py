"""
Pydantic schemas for all API request/response contracts.
Covers Auth, Users, Carbon, AI, Recommendations, Gamification, Eco Twin, Analytics.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


# ══════════════════════════════════════════════════════════════════
#  AUTH SCHEMAS
# ══════════════════════════════════════════════════════════════════

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=2, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class GoogleOAuthRequest(BaseModel):
    code: str
    redirect_uri: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ══════════════════════════════════════════════════════════════════
#  USER SCHEMAS
# ══════════════════════════════════════════════════════════════════

class UserProfile(BaseModel):
    id: UUID
    email: str
    full_name: str
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str
    country: Optional[str] = None
    city: Optional[str] = None
    bio: Optional[str] = None
    household_size: int = 1
    total_points: int = 0
    level: int = 1
    current_streak: int = 0
    longest_streak: int = 0
    carbon_saved_kg: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    country: Optional[str] = None
    city: Optional[str] = None
    bio: Optional[str] = None
    household_size: Optional[int] = Field(None, ge=1, le=20)
    avatar_url: Optional[str] = None


# ══════════════════════════════════════════════════════════════════
#  CARBON SCHEMAS
# ══════════════════════════════════════════════════════════════════

class TransportationInput(BaseModel):
    vehicle_type: str = "car_petrol"  # car_petrol, car_diesel, car_hybrid, ev, none
    km_per_month: float = 0
    public_transport_km: float = 0
    flights_short_haul: int = 0  # per year
    flights_long_haul: int = 0  # per year
    bicycle_walking_pct: float = 0


class EnergyInput(BaseModel):
    electricity_kwh_per_month: float = 300
    renewable_percentage: float = 0
    natural_gas: bool = False
    heating_type: str = "electric"  # electric, gas, oil, heat_pump
    ac_usage_hours: float = 0
    household_size: int = 1


class FoodInput(BaseModel):
    diet_type: str = "mixed"  # vegan, vegetarian, pescatarian, mixed, heavy_meat
    dairy_consumption: str = "moderate"  # none, low, moderate, high
    food_waste_pct: float = 10
    local_produce_pct: float = 30


class ShoppingInput(BaseModel):
    clothing_items_per_month: int = 2
    electronics_per_year: int = 2
    online_deliveries_per_month: int = 4
    second_hand_pct: float = 10


class WasteInput(BaseModel):
    recycling_frequency: str = "sometimes"  # never, sometimes, often, always
    composting: bool = False
    plastic_usage: str = "moderate"  # low, moderate, high
    reusable_water_bottle: bool = False


class CarbonCalculateRequest(BaseModel):
    transportation: TransportationInput
    energy: EnergyInput
    food: FoodInput
    shopping: ShoppingInput
    waste: WasteInput


class CategoryBreakdown(BaseModel):
    category: str
    monthly_kg: float
    percentage: float
    details: Dict[str, Any] = {}


class CarbonScoreResponse(BaseModel):
    id: UUID
    monthly_kg: float
    annual_tons: float
    daily_kg: float
    grade: str
    grade_color: str
    breakdown: List[CategoryBreakdown]
    comparisons: Dict[str, float]
    insights: List[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class CarbonHistoryItem(BaseModel):
    id: UUID
    monthly_kg: float
    annual_tons: float
    grade: str
    created_at: datetime

    model_config = {"from_attributes": True}


class CarbonTrendsResponse(BaseModel):
    current_month: float
    previous_month: float
    change_pct: float
    trend: str  # improving, stable, worsening
    history: List[CarbonHistoryItem]


# ══════════════════════════════════════════════════════════════════
#  AI CHAT SCHEMAS
# ══════════════════════════════════════════════════════════════════

class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[UUID] = None


class ChatMessageResponse(BaseModel):
    conversation_id: UUID
    message_id: UUID
    content: str
    intent: Optional[str] = None
    agent_used: Optional[str] = None
    suggestions: List[str] = []
    created_at: datetime


class ConversationResponse(BaseModel):
    id: UUID
    title: Optional[str] = None
    message_count: int
    last_intent: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    intent: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ══════════════════════════════════════════════════════════════════
#  RECOMMENDATION SCHEMAS
# ══════════════════════════════════════════════════════════════════

class RecommendationResponse(BaseModel):
    id: UUID
    title: str
    description: str
    detailed_steps: List[Dict] = []
    category: str
    difficulty: str
    priority_score: int
    estimated_co2_savings_kg: float
    estimated_cost_savings: float
    estimated_time_weeks: int
    impact_level: str
    status: str
    confidence_score: float
    created_at: datetime

    model_config = {"from_attributes": True}


class RecommendationActionRequest(BaseModel):
    action_type: str  # accepted, rejected, started, completed, paused
    notes: Optional[str] = None
    progress_percentage: Optional[int] = Field(None, ge=0, le=100)


# ══════════════════════════════════════════════════════════════════
#  GAMIFICATION SCHEMAS
# ══════════════════════════════════════════════════════════════════

class PointsResponse(BaseModel):
    points: int
    level: int
    level_progress: int
    next_level_points: int
    total_points_earned: int
    badges_unlocked: int
    challenges_completed: int
    current_streak: int
    longest_streak: int


class BadgeResponse(BaseModel):
    id: UUID
    name: str
    display_name: str
    description: str
    icon_url: Optional[str] = None
    category: str
    rarity: str
    points_awarded: int
    unlocked: bool = False
    unlocked_at: Optional[datetime] = None
    progress: int = 0


class ChallengeResponse(BaseModel):
    id: UUID
    name: str
    display_name: str
    description: str
    category: str
    challenge_type: str
    difficulty: str
    duration_days: int
    points_reward: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    participant_count: int
    user_status: Optional[str] = None
    user_progress: Optional[Dict] = None


class LeaderboardEntry(BaseModel):
    rank: int
    user: Dict[str, Any]
    score: float
    percentile: Optional[float] = None


class LeaderboardResponse(BaseModel):
    leaderboard_type: str
    period: str
    metric: str
    current_user_rank: Optional[int] = None
    rankings: List[LeaderboardEntry]
    total_participants: int


# ══════════════════════════════════════════════════════════════════
#  ECO TWIN SCHEMAS
# ══════════════════════════════════════════════════════════════════

class ScenarioChange(BaseModel):
    category: str
    change_type: str
    from_value: Optional[str] = Field(None, alias="from")
    to_value: Optional[str] = Field(None, alias="to")
    details: Optional[Dict] = None

    model_config = {"populate_by_name": True}


class SimulationRequest(BaseModel):
    scenario_name: str = Field(..., min_length=1, max_length=100)
    changes: List[ScenarioChange]


class SimulationResponse(BaseModel):
    simulation_id: UUID
    scenario_name: str
    baseline: Dict[str, float]
    simulated: Dict[str, float]
    impact: Dict[str, float]
    financial: Dict[str, float]
    feasibility: Dict[str, Any]
    created_at: datetime


class PrebuiltScenario(BaseModel):
    id: str
    name: str
    description: str
    expected_reduction_pct: float
    difficulty: str
    estimated_cost: str


# ══════════════════════════════════════════════════════════════════
#  ANALYTICS SCHEMAS
# ══════════════════════════════════════════════════════════════════

class DashboardAnalytics(BaseModel):
    period: str
    carbon_metrics: Dict[str, Any]
    engagement: Dict[str, Any]
    achievements: Dict[str, Any]
    impact: Dict[str, Any]


class AnalyticsBreakdown(BaseModel):
    period: str
    categories: List[Dict[str, Any]]
    total_current: float
    total_previous: float


class PredictionResponse(BaseModel):
    timeframe: str
    predictions: List[Dict[str, Any]]
    trend: str
    projected_reduction_pct: float
    confidence_score: float
    assumptions: List[str]


# ══════════════════════════════════════════════════════════════════
#  LEARNING SCHEMAS
# ══════════════════════════════════════════════════════════════════

class LearningContentResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    description: Optional[str] = None
    category: str
    difficulty: str
    content_type: str
    thumbnail_url: Optional[str] = None
    estimated_read_time: Optional[int] = None
    view_count: int = 0
    like_count: int = 0
    tags: List[str] = []
    is_featured: bool = False

    model_config = {"from_attributes": True}


class LearningContentDetailResponse(LearningContentResponse):
    content: str
    related_content: List[Dict] = []


class QuizResponse(BaseModel):
    id: UUID
    title: str
    category: str
    difficulty: str
    question_count: int
    total_points: int
    passing_score: Optional[int] = None
    average_score: Optional[float] = None
    attempt_count: int = 0

    model_config = {"from_attributes": True}


class QuizAttemptRequest(BaseModel):
    answers: List[Dict[str, str]]
    time_taken_seconds: Optional[int] = None


class QuizAttemptResponse(BaseModel):
    attempt_id: UUID
    score: int
    total_possible: int
    percentage: float
    passed: bool
    correct_answers: int
    wrong_answers: int
    points_earned: int
    results: List[Dict]


# ══════════════════════════════════════════════════════════════════
#  SHARED / PAGINATION
# ══════════════════════════════════════════════════════════════════

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class PaginatedResponse(BaseModel):
    data: List[Any]
    pagination: Dict[str, int]
