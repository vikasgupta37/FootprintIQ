"""
Centralized Application Constants.
Stores emission factors, points logic, and other magic numbers to avoid DRY violations.
"""

# ── Gamification Constants ───────────────────────────────────────

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

# ── Carbon Emission Factors ──────────────────────────────────────
# Source: IPCC AR6, EPA, Carbon Footprint Ltd.

VEHICLE_EMISSION_FACTORS = {
    "car_petrol": 0.171,       # kg CO2e per km
    "car_diesel": 0.168,
    "car_hybrid": 0.092,
    "ev": 0.053,
    "motorcycle": 0.103,
    "none": 0.0,
}

PUBLIC_TRANSPORT_FACTOR = 0.089  # kg CO2e per km (average bus/metro)

FLIGHT_EMISSIONS = {
    "short_haul": 255,   # kg CO2e per flight (avg domestic round-trip)
    "long_haul": 1240,   # kg CO2e per flight (avg international round-trip)
}

ELECTRICITY_FACTOR = 0.309  # kg CO2e per kWh (US average grid)

HEATING_FACTORS = {
    "electric": 0.309,
    "gas": 0.184,
    "oil": 0.245,
    "heat_pump": 0.100,
}

DIET_FACTORS = {
    "vegan": 1.5,           # tons CO2e per year
    "vegetarian": 1.7,
    "pescatarian": 1.9,
    "mixed": 2.5,
    "heavy_meat": 3.3,
}

DAIRY_MULTIPLIERS = {
    "none": 0.0,
    "low": 0.8,
    "moderate": 1.0,
    "high": 1.3,
}

# Average kg CO2e per item
SHOPPING_FACTORS = {
    "clothing_item": 25.0,
    "electronics_item": 200.0,
    "online_delivery": 3.5,
}

RECYCLING_REDUCTION = {
    "never": 0.0,
    "sometimes": 0.15,
    "often": 0.30,
    "always": 0.45,
}

# Grade thresholds (monthly kg CO2e)
GRADE_THRESHOLDS = [
    (200,  "EXCELLENT", "#10B981"),  # green
    (350,  "GOOD",      "#34D399"),
    (500,  "MODERATE",  "#FBBF24"),  # amber
    (700,  "HIGH",      "#F97316"),  # orange
    (9999, "CRITICAL",  "#EF4444"),  # red
]

# Comparisons (monthly kg)
COMPARISON_AVERAGES = {
    "us_average": 1370,    # ~16.4 tons/year
    "eu_average": 567,     # ~6.8 tons/year
    "global_average": 400, # ~4.8 tons/year
    "target_2c": 183,      # ~2.2 tons/year (Paris Agreement)
    "india_average": 158,  # ~1.9 tons/year
}
