import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import async_session_maker
from app.models.gamification import Badge, Challenge

async def seed_gamification():
    async with async_session_maker() as session:
        # Check if already seeded
        result = await session.execute(select(Badge))
        if result.scalars().first():
            print("Gamification data already seeded.")
            return

        print("Seeding Gamification data...")
        
        # ── Badges ───────────────────────────────────────────────
        badges = [
            Badge(
                name="first_step",
                display_name="First Step",
                description="Calculate your carbon footprint for the first time.",
                category="engagement",
                rarity="common",
                points_awarded=50,
                icon_url="/badges/first_step.png"
            ),
            Badge(
                name="public_transit_hero",
                display_name="Public Transit Hero",
                description="Log 10 public transit trips.",
                category="carbon_reduction",
                rarity="uncommon",
                points_awarded=150,
                icon_url="/badges/transit.png"
            ),
            Badge(
                name="meatless_week",
                display_name="Plant Based Week",
                description="Complete the meatless week challenge.",
                category="carbon_reduction",
                rarity="rare",
                points_awarded=300,
                icon_url="/badges/plant.png"
            ),
            Badge(
                name="eco_twin_master",
                display_name="Eco Twin Master",
                description="Simulate 5 different lifestyle changes in Eco Twin.",
                category="learning",
                rarity="epic",
                points_awarded=500,
                icon_url="/badges/eco_twin.png"
            )
        ]
        session.add_all(badges)
        
        # ── Challenges ───────────────────────────────────────────
        challenges = [
            Challenge(
                name="meatless_week_challenge",
                display_name="Meatless Week Challenge",
                description="Go completely meat-free for 7 days to dramatically reduce your food footprint.",
                category="food",
                challenge_type="weekly",
                difficulty="hard",
                duration_days=7,
                points_reward=300
            ),
            Challenge(
                name="energy_vampire_hunt",
                display_name="Energy Vampire Hunt",
                description="Unplug all unused electronics for a week.",
                category="energy",
                challenge_type="weekly",
                difficulty="medium",
                duration_days=7,
                points_reward=150
            ),
            Challenge(
                name="public_transit_commute",
                display_name="Transit Commuter",
                description="Take public transit to work or school 3 times this week.",
                category="transportation",
                challenge_type="weekly",
                difficulty="medium",
                duration_days=7,
                points_reward=200
            )
        ]
        session.add_all(challenges)
        
        await session.commit()
        print("Gamification data seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed_gamification())
