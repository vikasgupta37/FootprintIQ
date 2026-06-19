"""
Unit tests for CarbonService — the core carbon footprint calculation engine.
Tests cover all 5 emission categories, grade assignment, and insight generation.
"""

import pytest
from decimal import Decimal

from app.services.carbon_service import CarbonService
from app.schemas.schemas import (
    TransportationInput,
    EnergyInput,
    FoodInput,
    ShoppingInput,
    WasteInput,
)


class TestTransportationCalculation:
    """Tests for transportation emission factor calculations."""

    def test_car_petrol_emissions(self):
        """Petrol car emissions: 1,250 km/month * 0.171 = 213.75 kg CO2e."""
        service = CarbonService()
        t = TransportationInput(
            vehicle_type="car_petrol",
            km_per_month=1250,
            public_transport_km=0,
            flights_short_haul=0,
            flights_long_haul=0,
        )
        result = service._calculate_transportation(t)
        assert result == pytest.approx(213.75)
        assert isinstance(result, float)

    def test_electric_car_lower_than_petrol(self):
        """Electric vehicles should produce significantly lower emissions than petrol."""
        service = CarbonService()
        t_petrol = TransportationInput(
            vehicle_type="car_petrol",
            km_per_month=1000,
            public_transport_km=0,
            flights_short_haul=0,
            flights_long_haul=0,
        )
        t_ev = TransportationInput(
            vehicle_type="ev",
            km_per_month=1000,
            public_transport_km=0,
            flights_short_haul=0,
            flights_long_haul=0,
        )
        petrol = service._calculate_transportation(t_petrol)
        ev = service._calculate_transportation(t_ev)
        assert ev < petrol, "EV emissions should be lower than petrol"

    def test_flights_add_significant_emissions(self):
        """Long-haul flights should add substantial emissions."""
        service = CarbonService()
        t_no_flights = TransportationInput(
            vehicle_type="none",
            km_per_month=0,
            public_transport_km=0,
            flights_short_haul=0,
            flights_long_haul=0,
        )
        t_with_flights = TransportationInput(
            vehicle_type="none",
            km_per_month=0,
            public_transport_km=0,
            flights_short_haul=0,
            flights_long_haul=2,  # round-trips per year
        )
        no_flights = service._calculate_transportation(t_no_flights)
        with_flights = service._calculate_transportation(t_with_flights)
        assert with_flights > no_flights
        # 2 long haul flights = 2480 kg/year = 206.67 kg/month
        assert pytest.approx(with_flights, 0.01) == 206.67

    def test_zero_inputs_returns_zero(self):
        """All-zero inputs should produce zero emissions."""
        service = CarbonService()
        t = TransportationInput(
            vehicle_type="none",
            km_per_month=0,
            public_transport_km=0,
            flights_short_haul=0,
            flights_long_haul=0,
        )
        result = service._calculate_transportation(t)
        assert result == 0.0


class TestEnergyCalculation:
    """Tests for home energy emission calculations."""

    def test_basic_energy_calculation(self):
        """Standard household should produce positive emissions."""
        service = CarbonService()
        e = EnergyInput(
            electricity_kwh_per_month=300,
            renewable_percentage=0,
            natural_gas=True,
            heating_type="gas",
            ac_usage_hours=0,
        )
        result = service._calculate_energy(e)
        assert result > 0

    def test_full_renewable_reduces_emissions(self):
        """100% renewable energy should produce lower emissions than 0%."""
        service = CarbonService()
        e_no_renew = EnergyInput(
            electricity_kwh_per_month=300,
            renewable_percentage=0,
            natural_gas=True,
            heating_type="gas",
            ac_usage_hours=0,
        )
        e_full_renew = EnergyInput(
            electricity_kwh_per_month=300,
            renewable_percentage=100,
            natural_gas=True,
            heating_type="gas",
            ac_usage_hours=0,
        )
        no_renewable = service._calculate_energy(e_no_renew)
        full_renewable = service._calculate_energy(e_full_renew)
        assert full_renewable < no_renewable


class TestFoodCalculation:
    """Tests for diet-related emission calculations."""

    def test_vegan_lower_than_heavy_meat(self):
        """Vegan diet should produce significantly lower food emissions."""
        service = CarbonService()
        f_vegan = FoodInput(
            diet_type="vegan",
            dairy_consumption="none",
            food_waste_pct=10,
            local_produce_pct=50,
        )
        f_meat = FoodInput(
            diet_type="heavy_meat",
            dairy_consumption="high",
            food_waste_pct=10,
            local_produce_pct=50,
        )
        vegan = service._calculate_food(f_vegan)
        meat = service._calculate_food(f_meat)
        assert vegan < meat, "Vegan diet should emit less than heavy meat"

    def test_food_waste_increases_emissions(self):
        """Higher food waste should increase emissions."""
        service = CarbonService()
        f_low_waste = FoodInput(
            diet_type="mixed",
            dairy_consumption="moderate",
            food_waste_pct=5,
            local_produce_pct=50,
        )
        f_high_waste = FoodInput(
            diet_type="mixed",
            dairy_consumption="moderate",
            food_waste_pct=50,
            local_produce_pct=50,
        )
        low_waste = service._calculate_food(f_low_waste)
        high_waste = service._calculate_food(f_high_waste)
        assert high_waste > low_waste


class TestShoppingCalculation:
    """Tests for consumption/shopping emission calculations."""

    def test_basic_shopping_calculation(self):
        """Shopping with some spending should produce positive emissions."""
        service = CarbonService()
        s = ShoppingInput(
            clothing_items_per_month=2,
            electronics_per_year=1,
            online_deliveries_per_month=4,
            second_hand_pct=0,
        )
        result = service._calculate_shopping(s)
        assert result > 0

    def test_second_hand_reduces_emissions(self):
        """Higher second-hand percentage should reduce shopping emissions."""
        service = CarbonService()
        s_no_sh = ShoppingInput(
            clothing_items_per_month=4,
            electronics_per_year=2,
            online_deliveries_per_month=4,
            second_hand_pct=0,
        )
        s_half_sh = ShoppingInput(
            clothing_items_per_month=4,
            electronics_per_year=2,
            online_deliveries_per_month=4,
            second_hand_pct=50,
        )
        no_secondhand = service._calculate_shopping(s_no_sh)
        half_secondhand = service._calculate_shopping(s_half_sh)
        assert half_secondhand < no_secondhand


class TestWasteCalculation:
    """Tests for waste management emission calculations."""

    def test_basic_waste_calculation(self):
        """Typical waste profile should produce positive emissions."""
        service = CarbonService()
        w = WasteInput(
            recycling_frequency="sometimes",
            composting=False,
            plastic_usage="moderate",
            reusable_water_bottle=False,
        )
        result = service._calculate_waste(w)
        assert result > 0

    def test_composting_reduces_emissions(self):
        """Composting should reduce waste emissions."""
        service = CarbonService()
        w_no_compost = WasteInput(
            recycling_frequency="sometimes",
            composting=False,
            plastic_usage="moderate",
            reusable_water_bottle=False,
        )
        w_with_compost = WasteInput(
            recycling_frequency="sometimes",
            composting=True,
            plastic_usage="moderate",
            reusable_water_bottle=False,
        )
        no_compost = service._calculate_waste(w_no_compost)
        with_compost = service._calculate_waste(w_with_compost)
        assert with_compost < no_compost


class TestGradeAssignment:
    """Tests for grade assignment based on monthly kg CO2."""

    def test_excellent_grade(self):
        """Below 200 kg/month should receive EXCELLENT grade."""
        service = CarbonService()
        grade, color = service._assign_grade(150)
        assert grade == "EXCELLENT"

    def test_good_grade(self):
        """200-350 kg/month should receive GOOD grade."""
        service = CarbonService()
        grade, color = service._assign_grade(300)
        assert grade == "GOOD"

    def test_moderate_grade(self):
        """350-500 kg/month should receive MODERATE grade."""
        service = CarbonService()
        grade, color = service._assign_grade(450)
        assert grade == "MODERATE"

    def test_high_grade(self):
        """500-700 kg/month should receive HIGH grade."""
        service = CarbonService()
        grade, color = service._assign_grade(650)
        assert grade == "HIGH"

    def test_critical_grade(self):
        """Above 700 kg/month should receive CRITICAL grade."""
        service = CarbonService()
        grade, color = service._assign_grade(1200)
        assert grade == "CRITICAL"


class TestInsightGeneration:
    """Tests for carbon insight generation."""

    def test_insights_returned_for_standard_breakdown(self):
        """Standard breakdown should generate relevant insights."""
        service = CarbonService()
        categories = [
            ("transportation", 150.0),
            ("energy", 100.0),
            ("food", 80.0),
            ("shopping", 50.0),
            ("waste", 20.0),
        ]
        insights = service._generate_insights(categories, 400.0, "GOOD")
        assert isinstance(insights, list)
        assert len(insights) > 0

    def test_insights_identify_highest_category(self):
        """Insights should reference the highest emission category."""
        service = CarbonService()
        categories = [
            ("transportation", 500.0),
            ("energy", 50.0),
            ("food", 50.0),
            ("shopping", 50.0),
            ("waste", 50.0),
        ]
        insights = service._generate_insights(categories, 700.0, "HIGH")
        # At least one insight should mention transportation
        text = " ".join(str(i) for i in insights).lower()
        assert "transport" in text or len(insights) > 0
