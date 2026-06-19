import json
from datetime import date, timedelta
from typing import List, Dict, Any, Optional
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc

from app.models.extras import SustainabilityReport
from app.models.carbon import CarbonFootprint
from app.services.ai_service import get_anthropic_client, SYSTEM_PROMPT
from app.core.config import settings

class ReportService:
    async def generate_weekly_report(self, db: AsyncSession, user_id: uuid.UUID) -> Optional[SustainabilityReport]:
        """
        Generates a weekly sustainability report for the user by aggregating recent data
        and using Claude to provide insights.
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=7)

        # 1. Gather recent footprint data
        stmt = select(CarbonFootprint).where(
            CarbonFootprint.user_id == user_id
        ).order_by(desc(CarbonFootprint.created_at)).limit(2)
        result = await db.execute(stmt)
        footprints = result.scalars().all()
        
        if not footprints:
            return None
            
        current_footprint = footprints[0]
        previous_footprint = footprints[1] if len(footprints) > 1 else None
        
        # 2. Gather AI input payload
        payload = {
            "time_period": f"{start_date} to {end_date}",
            "current_footprint_kg": float(current_footprint.monthly_kg),
            "previous_footprint_kg": float(previous_footprint.monthly_kg) if previous_footprint else None,
            "breakdown": current_footprint.breakdown,
            "ai_sustainability_score": current_footprint.ai_sustainability_score or 50,
            "grade": current_footprint.grade
        }

        # 3. Call AI to generate summary and insights
        client = get_anthropic_client()
        prompt = f"""
You are the FootprintIQ Sustainability Coach. Generate a weekly report based on the following user data:
{json.dumps(payload, indent=2)}

Return a JSON object with two keys:
- "summary_text": A 2-3 paragraph motivating summary of their week.
- "key_insights": A list of up to 3 objects, each with {{"text": "insight description", "metric": "quantifiable string like '-15kg'"}}.
"""
        response = await client.messages.create(
            model=settings.AI_MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        # Parse JSON from response
        try:
            content = response.content[0].text
            # Simple extraction assuming the model returns JSON
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                parsed = json.loads(json_str)
            else:
                parsed = {"summary_text": content, "key_insights": []}
        except Exception:
            parsed = {"summary_text": "Failed to parse AI insights.", "key_insights": []}

        # 4. Save report
        report = SustainabilityReport(
            user_id=user_id,
            report_type="weekly",
            period_start=start_date,
            period_end=end_date,
            summary_text=parsed.get("summary_text", ""),
            key_insights=parsed.get("key_insights", []),
            carbon_saved_kg=payload["previous_footprint_kg"] - payload["current_footprint_kg"] if payload["previous_footprint_kg"] else 0,
            ai_sustainability_score=payload["ai_sustainability_score"]
        )
        
        db.add(report)
        await db.flush()
        
        return report

    async def get_user_reports(self, db: AsyncSession, user_id: uuid.UUID) -> List[SustainabilityReport]:
        stmt = select(SustainabilityReport).where(
            SustainabilityReport.user_id == user_id
        ).order_by(desc(SustainabilityReport.created_at))
        result = await db.execute(stmt)
        return list(result.scalars().all())

report_service = ReportService()
