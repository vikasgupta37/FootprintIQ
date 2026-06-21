"""
Gamification Service — points, badges, challenges, leaderboards.
"""

from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, desc, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import cache
from app.core.exceptions import ConflictException, NotFoundException
from app.models.gamification import (
    Badge,
    Challenge,
    Leaderboard,
    UserAchievement,
    UserChallenge,
)
from app.models.user import User
from app.schemas.schemas import PointsResponse


# Points for actions
POINT_VALUES = {
    "calculation": 50,
    "ai_chat": 10,
    "recommendation_accepted": 25,
    "recommendation_completed": 100,
    "challenge_completed": 200,
    "quiz_completed": 50,
    "article_read": 15,
    "streak_day": 5,
    "first_calculation": 100,
    "badge_unlocked": 50,
}

# Level thresholds
LEVEL_THRESHOLDS = [
    0, 100, 300, 600, 1000, 1500, 2200, 3000, 4000, 5200,
    6500, 8000, 10000, 12500, 15000, 18000, 22000, 27000, 33000, 40000,
]


class GamificationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Points ───────────────────────────────────────────────────

    async def award_points(self, user_id: UUID, action: str, multiplier: float = 1.0, points_override: Optional[int] = None) -> int:
        """Award points for an action and check level up."""
        if points_override is not None:
            points = int(points_override * multiplier)
        else:
            points = int(POINT_VALUES.get(action, 0) * multiplier)
            
        if points == 0:
            return 0

        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return 0

        user.total_points += points
        new_level = self._calculate_level(user.total_points)
        leveled_up = new_level > user.level
        user.level = new_level

        await self.db.flush()
        await cache.delete(cache.user_profile_key(str(user_id)))

        return points

    async def get_points(self, user: User) -> PointsResponse:
        """Get user's points, level, and progress."""
        level = self._calculate_level(user.total_points)
        next_level_pts = LEVEL_THRESHOLDS[level] if level < len(LEVEL_THRESHOLDS) else LEVEL_THRESHOLDS[-1]
        current_level_pts = LEVEL_THRESHOLDS[level - 1] if level > 0 else 0
        range_pts = next_level_pts - current_level_pts
        progress = int(((user.total_points - current_level_pts) / range_pts * 100) if range_pts > 0 else 100)

        # Count badges and challenges
        badge_count = await self.db.execute(
            select(func.count()).select_from(UserAchievement).where(UserAchievement.user_id == user.id)
        )
        challenge_count = await self.db.execute(
            select(func.count()).select_from(UserChallenge).where(
                UserChallenge.user_id == user.id,
                UserChallenge.status == "completed",
            )
        )

        return PointsResponse(
            points=user.total_points,
            level=level,
            level_progress=min(progress, 100),
            next_level_points=next_level_pts,
            total_points_earned=user.total_points,
            badges_unlocked=badge_count.scalar() or 0,
            challenges_completed=challenge_count.scalar() or 0,
            current_streak=user.current_streak,
            longest_streak=user.longest_streak,
        )

    def _calculate_level(self, points: int) -> int:
        for i, threshold in enumerate(LEVEL_THRESHOLDS):
            if points < threshold:
                return max(1, i)
        return len(LEVEL_THRESHOLDS)

    # ── Badges ───────────────────────────────────────────────────

    async def get_badges(self, user_id: UUID, status: str = "all") -> list:
        """Get all badges with user unlock status."""
        all_badges = await self.db.execute(
            select(Badge).where(Badge.is_active == True)
        )
        badges = all_badges.scalars().all()

        user_achievements = await self.db.execute(
            select(UserAchievement).where(UserAchievement.user_id == user_id)
        )
        unlocked_map = {
            str(ua.badge_id): ua for ua in user_achievements.scalars().all()
        }

        result = []
        for badge in badges:
            unlocked = str(badge.id) in unlocked_map
            ua = unlocked_map.get(str(badge.id))

            if status == "unlocked" and not unlocked:
                continue
            if status == "locked" and unlocked:
                continue

            result.append({
                "id": badge.id,
                "name": badge.name,
                "display_name": badge.display_name,
                "description": badge.description,
                "icon_url": badge.icon_url,
                "category": badge.category,
                "rarity": badge.rarity,
                "points_awarded": badge.points_awarded,
                "unlocked": unlocked,
                "unlocked_at": ua.unlocked_at if ua else None,
                "progress": ua.progress if ua else 0,
            })

        return result

    async def check_and_award_badge(self, user_id: UUID, badge_name: str) -> Optional[dict]:
        """Award a badge if not already unlocked."""
        result = await self.db.execute(select(Badge).where(Badge.name == badge_name))
        badge = result.scalar_one_or_none()
        if not badge:
            return None

        existing = await self.db.execute(
            select(UserAchievement).where(
                UserAchievement.user_id == user_id,
                UserAchievement.badge_id == badge.id,
            )
        )
        if existing.scalar_one_or_none():
            return None

        achievement = UserAchievement(
            user_id=user_id,
            badge_id=badge.id,
            progress=100,
        )
        self.db.add(achievement)
        await self.award_points(user_id, "badge_unlocked", points_override=badge.points_awarded)
        await self.db.flush()

        return {"badge": badge.display_name, "points": badge.points_awarded}

    # ── Challenges ───────────────────────────────────────────────

    async def get_challenges(self, user_id: UUID, status: str = "available") -> list:
        """Get challenges with user participation status."""
        query = select(Challenge).where(Challenge.is_active == True)
        result = await self.db.execute(query)
        challenges = result.scalars().all()

        user_challenges = await self.db.execute(
            select(UserChallenge).where(UserChallenge.user_id == user_id)
        )
        participation_map = {
            str(uc.challenge_id): uc for uc in user_challenges.scalars().all()
        }

        result_list = []
        for ch in challenges:
            uc = participation_map.get(str(ch.id))
            user_status = uc.status if uc else None

            if status == "active" and user_status != "active":
                continue
            if status == "completed" and user_status != "completed":
                continue

            result_list.append({
                "id": ch.id,
                "name": ch.name,
                "display_name": ch.display_name,
                "description": ch.description,
                "category": ch.category,
                "challenge_type": ch.challenge_type,
                "difficulty": ch.difficulty,
                "duration_days": ch.duration_days,
                "points_reward": ch.points_reward,
                "start_date": ch.start_date,
                "end_date": ch.end_date,
                "participant_count": ch.participant_count,
                "user_status": user_status,
                "user_progress": uc.progress if uc else None,
            })

        return result_list

    async def join_challenge(self, user_id: UUID, challenge_id: UUID) -> dict:
        """Join a challenge."""
        result = await self.db.execute(
            select(Challenge).where(Challenge.id == challenge_id)
        )
        challenge = result.scalar_one_or_none()
        if not challenge:
            raise NotFoundException("Challenge", str(challenge_id))

        existing = await self.db.execute(
            select(UserChallenge).where(
                UserChallenge.user_id == user_id,
                UserChallenge.challenge_id == challenge_id,
                UserChallenge.status == "active",
            )
        )
        if existing.scalar_one_or_none():
            raise ConflictException("Already participating in this challenge")

        uc = UserChallenge(
            user_id=user_id,
            challenge_id=challenge_id,
        )
        self.db.add(uc)
        challenge.participant_count += 1
        await self.db.flush()

        return {
            "challenge_id": str(challenge_id),
            "status": "active",
            "started_at": uc.started_at.isoformat(),
        }

    # ── Leaderboard ──────────────────────────────────────────────

    async def get_leaderboard(
        self,
        leaderboard_type: str = "global",
        period: str = "weekly",
        metric: str = "points",
        limit: int = 20,
    ) -> dict:
        """Get leaderboard rankings."""
        # For simplicity, generate from User table directly for points
        query = (
            select(User)
            .where(User.is_active == True)
            .order_by(desc(User.total_points))
            .limit(limit)
        )
        result = await self.db.execute(query)
        users = result.scalars().all()

        rankings = []
        for i, u in enumerate(users, 1):
            rankings.append({
                "rank": i,
                "user": {
                    "id": str(u.id),
                    "username": u.username or u.full_name,
                    "avatar_url": u.avatar_url,
                    "level": u.level,
                },
                "score": u.total_points,
                "percentile": None,
            })

        total_users = await self.db.execute(
            select(func.count()).select_from(User).where(User.is_active == True)
        )

        return {
            "leaderboard_type": leaderboard_type,
            "period": period,
            "metric": metric,
            "rankings": rankings,
            "total_participants": total_users.scalar() or 0,
        }
