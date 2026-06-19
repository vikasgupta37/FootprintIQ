"""
Unit tests for EcoTwinService — scenario simulation and change impact calculation.
"""

import pytest

from app.services.ecotwin_service import (
    CHANGE_IMPACTS,
    EcoTwinService,
    PREBUILT_SCENARIOS,
)


class TestPrebuiltScenarios:
    """Tests for prebuilt scenario configuration."""

    def test_scenarios_have_required_fields(self):
        """Each prebuilt scenario should have id, name, description, and reduction_pct."""
        required_keys = {"id", "name", "description", "expected_reduction_pct", "difficulty"}
        for key, scenario in PREBUILT_SCENARIOS.items():
            for field in required_keys:
                assert field in scenario, f"Scenario '{key}' missing field '{field}'"

    def test_reduction_percentages_are_valid(self):
        """Reduction percentages should be between 0 and 100."""
        for key, scenario in PREBUILT_SCENARIOS.items():
            pct = scenario["expected_reduction_pct"]
            assert 0 < pct <= 100, f"Scenario '{key}' has invalid reduction: {pct}%"

    def test_difficulty_is_valid_enum(self):
        """Difficulty should be easy, medium, or hard."""
        valid = {"easy", "medium", "hard"}
        for key, scenario in PREBUILT_SCENARIOS.items():
            assert scenario["difficulty"] in valid, (
                f"Scenario '{key}' has invalid difficulty: {scenario['difficulty']}"
            )

    def test_get_prebuilt_scenarios_returns_list(self):
        """Static method should return a list of scenario dicts."""
        result = EcoTwinService.get_prebuilt_scenarios()
        assert isinstance(result, list)
        assert len(result) == len(PREBUILT_SCENARIOS)

    def test_sustainable_living_has_highest_combined_reduction(self):
        """Sustainable living package should have reduction >= 40%."""
        scenario = PREBUILT_SCENARIOS["sustainable_living"]
        assert scenario["expected_reduction_pct"] >= 40


class TestChangeImpacts:
    """Tests for change impact factor configuration."""

    def test_all_impacts_are_positive_fractions(self):
        """All impact factors should be between 0 and 1."""
        for category, changes in CHANGE_IMPACTS.items():
            for change, factor in changes.items():
                assert 0 < factor <= 1, (
                    f"Impact factor for {category}/{change} = {factor} is out of range"
                )

    def test_ev_higher_reduction_than_hybrid(self):
        """EV should have a higher reduction factor than hybrid."""
        ev = CHANGE_IMPACTS["replace_vehicle"]["car_petrol_to_ev"]
        hybrid = CHANGE_IMPACTS["replace_vehicle"]["car_petrol_to_hybrid"]
        assert ev > hybrid, "EV reduction should be greater than hybrid"

    def test_green_provider_higher_than_solar(self):
        """Green provider should have higher reduction than solar panels."""
        green = CHANGE_IMPACTS["add_renewable"]["green_provider"]
        solar = CHANGE_IMPACTS["add_renewable"]["solar_panels"]
        assert green > solar

    def test_vegan_higher_reduction_than_vegetarian(self):
        """Vegan diet change should have higher impact than vegetarian."""
        vegan = CHANGE_IMPACTS["change_diet"]["mixed_to_vegan"]
        veg = CHANGE_IMPACTS["change_diet"]["mixed_to_vegetarian"]
        assert vegan > veg


class TestChangeImpactCalculation:
    """Tests for the _calculate_change_impact method."""

    def test_known_change_type_returns_values(self):
        """Known change types should return non-zero reduction factors."""
        service = EcoTwinService.__new__(EcoTwinService)

        class FakeChange:
            change_type = "replace_vehicle"
            category = "transportation"

        result = service._calculate_change_impact(FakeChange())
        assert result["reduction_factor"] > 0
        assert "upfront_cost" in result
        assert "annual_savings" in result

    def test_unknown_change_type_returns_default(self):
        """Unknown change types should return a small default factor."""
        service = EcoTwinService.__new__(EcoTwinService)

        class FakeChange:
            change_type = "unknown_action"
            category = "other"

        result = service._calculate_change_impact(FakeChange())
        assert result["reduction_factor"] == 0.1
        assert result["upfront_cost"] == 0
        assert result["annual_savings"] == 0
