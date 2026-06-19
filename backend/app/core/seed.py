import asyncio
from datetime import date, datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.models.gamification import Badge, Challenge
from app.models.extras import LearningContent, Quiz

# ── Seed Data ──────────────────────────────────────────────────────

BADGES = [
    {
        "name": "first_calculation",
        "display_name": "Carbon Curious",
        "description": "Complete your first carbon footprint calculation",
        "category": "engagement",
        "rarity": "common",
        "icon_url": "/badges/curious.svg",
        "criteria": {"action": "complete_calculation", "count": 1},
        "points_awarded": 50,
    },
    {
        "name": "week_streak",
        "display_name": "7-Day Streak",
        "description": "Log in to FootprintIQ for 7 consecutive days",
        "category": "engagement",
        "rarity": "common",
        "icon_url": "/badges/streak7.svg",
        "criteria": {"action": "login_streak", "days": 7},
        "points_awarded": 100,
    },
    {
        "name": "co2_reducer_10",
        "display_name": "Carbon Cutter",
        "description": "Reduce your projected carbon footprint by 10%",
        "category": "carbon_reduction",
        "rarity": "rare",
        "icon_url": "/badges/reducer_10.svg",
        "criteria": {"action": "reduction", "percentage": 10},
        "points_awarded": 250,
    },
    {
        "name": "co2_reducer_30",
        "display_name": "Eco Champion",
        "description": "Reduce your projected carbon footprint by 30%",
        "category": "carbon_reduction",
        "rarity": "epic",
        "icon_url": "/badges/champion.svg",
        "criteria": {"action": "reduction", "percentage": 30},
        "points_awarded": 500,
    },
    {
        "name": "quiz_master",
        "display_name": "Eco Scholar",
        "description": "Score 100% on 3 interactive quizzes",
        "category": "learning",
        "rarity": "rare",
        "icon_url": "/badges/scholar.svg",
        "criteria": {"action": "perfect_quizzes", "count": 3},
        "points_awarded": 200,
    },
    {
        "name": "commute_hero",
        "display_name": "Transit Hero",
        "description": "Log 5 green commuting actions in weekly challenges",
        "category": "social",
        "rarity": "rare",
        "icon_url": "/badges/transit_hero.svg",
        "criteria": {"action": "green_commutes", "count": 5},
        "points_awarded": 150,
    }
]

CHALLENGES = [
    {
        "name": "green_commute_week",
        "display_name": "Green Commute Week",
        "description": "Walk, bike, or use public transport for all your work/school trips for 5 days.",
        "category": "transportation",
        "challenge_type": "weekly",
        "duration_days": 7,
        "requirements": {"transport_type": ["public", "bicycle", "walking"], "min_trips": 5},
        "points_reward": 300,
    },
    {
        "name": "meatless_week",
        "display_name": "Meatless Week",
        "description": "Eat a completely plant-based (vegan or vegetarian) diet for a whole week to reduce emissions.",
        "category": "food",
        "challenge_type": "weekly",
        "duration_days": 7,
        "requirements": {"diet": ["vegan", "vegetarian"], "days": 7},
        "points_reward": 400,
    },
    {
        "name": "power_down_week",
        "display_name": "Power Down Challenge",
        "description": "Reduce your home electricity usage by switching off standby appliances and adjusting your thermostat.",
        "category": "energy",
        "challenge_type": "weekly",
        "duration_days": 7,
        "requirements": {"adjust_thermostat": True, "unplug_standby": True},
        "points_reward": 250,
    },
    {
        "name": "zero_waste_day",
        "display_name": "Zero Waste Day",
        "description": "Avoid all single-use plastics and compost all organic waste for a full 24 hours.",
        "category": "waste",
        "challenge_type": "daily",
        "duration_days": 1,
        "requirements": {"single_use_plastics": 0, "compost_all_food": True},
        "points_reward": 100,
    }
]

ARTICLES = [
    {
        "title": "Diet and Climate: The Hidden Impact of Food",
        "slug": "diet-and-climate-hidden-impact-of-food",
        "description": "Learn how shifting to a plant-based diet can dramatically reduce your global footprint.",
        "category": "food",
        "difficulty": "beginner",
        "content_type": "article",
        "estimated_read_time": 5,
        "is_published": True,
        "content": """# Diet and Climate: The Hidden Impact of Food

Did you know that **food production accounts for about 26% of global greenhouse gas emissions**? That's more than a quarter of the world's carbon footprint linked directly to what we put on our plates.

## The Carbon Intensity of Food
Not all foods are created equal. Animal-based products consistently have a higher environmental impact than plant-based alternatives:
*   **Beef:** 60kg CO2e per kg of product.
*   **Cheese:** 24kg CO2e per kg.
*   **Poultry:** 10kg CO2e per kg.
*   **Wheat / Peas:** Less than 1.5kg CO2e per kg.

## Why Animal Products Have Higher Footprints
1.  **Enteric Fermentation:** Ruminants like cows and sheep produce methane, a greenhouse gas up to 36 times more potent than CO2.
2.  **Land Use:** Grazing land and feed crops require vast areas, leading to deforestation.
3.  **Feed Conversion:** It takes up to 25kg of plant feed to produce just 1kg of beef.

## Actionable Steps for Reductions
*   **Try Meatless Mondays:** Skipping meat just one day a week reduces your food footprint by ~15%.
*   **Embrace Plant Proteins:** Swap beef for lentils, beans, or chickpeas.
*   **Minimize Waste:** About 30% of all food produced is wasted, generating methane in landfills. Plan meals and compost leftovers!

🌱 **Every small shift on your plate makes a huge difference for our planet.**
""",
    },
    {
        "title": "Decarbonizing Your Home Energy Use",
        "slug": "decarbonizing-your-home-energy-use",
        "description": "Top strategies to optimize heating, cooling, and lighting emissions in your household.",
        "category": "energy",
        "difficulty": "intermediate",
        "content_type": "article",
        "estimated_read_time": 6,
        "is_published": True,
        "content": """# Decarbonizing Your Home Energy Use

Household heating, cooling, and electricity are the largest contributors to personal carbon emissions in many countries. Optimizing your home energy footprint can save both greenhouse gases and money on utility bills.

## Heating and Cooling: The Big Culprits
Heating and air conditioning make up over **50% of the average home's energy consumption**.
*   **Adjust the Thermostat:** Setting your thermostat 7-10°F lower in winter (or higher in summer) for 8 hours a day can reduce bills by 10%.
*   **Upgrade to Heat Pumps:** Modern electric heat pumps are up to 3-4 times more efficient than traditional gas or oil boilers because they transfer heat rather than generating it.

## Lighting and Electronics
*   **LED Transition:** Replacing incandescent bulbs with LEDs reduces lighting energy by 75-80% and bulbs last 25 times longer.
*   **Combat Vampire Power:** Standby power on unused electronics (TVs, chargers, computers) accounts for up to 10% of household electricity use. Use smart power strips to cut power completely.

## Sourcing Renewable Power
If available, switch your electricity plan to **100% green power** through your utility or install solar panels. A residential solar installation can prevent over 3-4 tons of CO2 emissions annually.
""",
    }
]

QUIZZES = [
    {
        "title": "Climate Science & Sustainability Basics",
        "description": "Test your knowledge of core sustainability terms, GHG protocols, and climate concepts.",
        "category": "sustainability_science",
        "difficulty": "beginner",
        "total_points": 100,
        "points_reward": 50,
        "is_published": True,
        "questions": [
            {
                "id": "q1",
                "text": "What percentage of global greenhouse gas emissions does food production account for?",
                "options": ["5%", "12%", "26%", "45%"],
                "answer": "26%",
            },
            {
                "id": "q2",
                "text": "Which greenhouse gas is primarily produced by decomposing organic waste in landfills?",
                "options": ["Carbon Dioxide", "Methane", "Nitrous Oxide", "Water Vapor"],
                "answer": "Methane",
            },
            {
                "id": "q3",
                "text": "What type of emissions are indirect emissions from the generation of purchased electricity?",
                "options": ["Scope 1", "Scope 2", "Scope 3", "Scope 4"],
                "answer": "Scope 2",
            }
        ]
    },
    {
        "title": "Transportation & Eco-Travel",
        "description": "Do you know which transport options emit the least carbon? Find out now!",
        "category": "transportation",
        "difficulty": "beginner",
        "total_points": 100,
        "points_reward": 50,
        "is_published": True,
        "questions": [
            {
                "id": "t1",
                "text": "Per passenger-kilometer, which of these travel modes emits the most CO2 on average?",
                "options": ["Domestic Flight", "Electric Train", "Shared Electric Vehicle", "Diesel Bus"],
                "answer": "Domestic Flight",
            },
            {
                "id": "t2",
                "text": "What is the typical reduction in commuting emissions if you switch from driving alone to public transit?",
                "options": ["10-20%", "30-45%", "up to 70%", "95%"],
                "answer": "up to 70%",
            }
        ]
    }
]

# ── Seeder Logic ───────────────────────────────────────────────────

async def seed_db(db: AsyncSession):
    """Seed the database with badges, challenges, articles, and quizzes."""
    print("Seeding database...")

    # 1. Seed Badges
    badge_map = {}
    for badge_data in BADGES:
        stmt = select(Badge).where(Badge.name == badge_data["name"])
        res = await db.execute(stmt)
        existing = res.scalar_one_or_none()
        if not existing:
            badge = Badge(**badge_data)
            db.add(badge)
            await db.flush()
            badge_map[badge.name] = badge.id
            print(f"Created badge: {badge.display_name}")
        else:
            badge_map[existing.name] = existing.id

    # 2. Seed Challenges
    for challenge_data in CHALLENGES:
        stmt = select(Challenge).where(Challenge.name == challenge_data["name"])
        res = await db.execute(stmt)
        existing = res.scalar_one_or_none()
        if not existing:
            # Optionally link to a badge if required
            if challenge_data["name"] == "green_commute_week" and "commute_hero" in badge_map:
                challenge_data["badge_reward_id"] = badge_map["commute_hero"]
            elif challenge_data["name"] == "meatless_week" and "quiz_master" in badge_map:
                pass  # no badge reward for this challenge yet

            challenge = Challenge(**challenge_data)
            db.add(challenge)
            print(f"Created challenge: {challenge.display_name}")

    # 3. Seed Articles (LearningContent)
    for article_data in ARTICLES:
        stmt = select(LearningContent).where(LearningContent.slug == article_data["slug"])
        res = await db.execute(stmt)
        existing = res.scalar_one_or_none()
        if not existing:
            article = LearningContent(**article_data)
            db.add(article)
            print(f"Created article: {article.title}")

    # 4. Seed Quizzes
    for quiz_data in QUIZZES:
        stmt = select(Quiz).where(Quiz.title == quiz_data["title"])
        res = await db.execute(stmt)
        existing = res.scalar_one_or_none()
        if not existing:
            quiz = Quiz(**quiz_data)
            db.add(quiz)
            print(f"Created quiz: {quiz.title}")

    await db.commit()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    async def main():
        async with AsyncSessionLocal() as session:
            await seed_db(session)

    asyncio.run(main())
