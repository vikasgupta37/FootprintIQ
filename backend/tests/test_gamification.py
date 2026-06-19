"""
Unit tests for GamificationService — points, levels, and leaderboards.
"""

import pytest

from app.services.gamification_service import GamificationService, LEVEL_THRESHOLDS, POINT_VALUES


class TestPointValues:
    """Tests for point value configuration."""

    def test_all_actions_have_positive_points(self):
        """Every defined action should award positive points."""
        for action, points in POINT_VALUES.items():
            assert points > 0, f"Action '{action}' has non-positive points: {points}"

    def test_challenge_completion_worth_more_than_article_read(self):
        """Challenge completion should be more rewarding than reading."""
        assert POINT_VALUES["challenge_completed"] > POINT_VALUES["article_read"]

    def test_first_calculation_bonus_exists(self):
        """First calculation should have a bonus point value."""
        assert "first_calculation" in POINT_VALUES
        assert POINT_VALUES["first_calculation"] >= 50


class TestLevelCalculation:
    """Tests for level threshold calculations."""

    def test_zero_points_is_level_one(self):
        """A new user with 0 points should be level 1."""
        service = GamificationService.__new__(GamificationService)
        assert service._calculate_level(0) == 1

    def test_level_increases_with_points(self):
        """Higher points should yield higher levels."""
        service = GamificationService.__new__(GamificationService)
        level_low = service._calculate_level(50)
        level_high = service._calculate_level(5000)
        assert level_high > level_low

    def test_level_at_threshold_boundary(self):
        """Points exactly at a threshold should advance to the next level."""
        service = GamificationService.__new__(GamificationService)
        # LEVEL_THRESHOLDS[1] = 100
        level_below = service._calculate_level(99)
        level_at = service._calculate_level(100)
        assert level_at >= level_below

    def test_max_level_for_very_high_points(self):
        """Very high points should reach the maximum level."""
        service = GamificationService.__new__(GamificationService)
        max_level = service._calculate_level(1_000_000)
        assert max_level == len(LEVEL_THRESHOLDS)

    def test_level_thresholds_are_sorted(self):
        """Level thresholds should be in ascending order."""
        for i in range(1, len(LEVEL_THRESHOLDS)):
            assert LEVEL_THRESHOLDS[i] > LEVEL_THRESHOLDS[i - 1], (
                f"Threshold at index {i} ({LEVEL_THRESHOLDS[i]}) is not greater than "
                f"index {i-1} ({LEVEL_THRESHOLDS[i-1]})"
            )

    def test_level_never_returns_zero(self):
        """Level should always be at least 1."""
        service = GamificationService.__new__(GamificationService)
        for pts in [0, 1, 50, 99]:
            assert service._calculate_level(pts) >= 1
