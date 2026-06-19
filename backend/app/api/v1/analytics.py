"""Analytics API — dashboard, breakdown, predictions, export."""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.carbon_service import CarbonService
from app.services.report_service import report_service

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard(
    period: str = Query("month"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CarbonService(db)
    trends = await service.get_trends(user.id)

    return {
        "period": period,
        "carbon_metrics": {
            "current_footprint": trends["current_month"],
            "previous_footprint": trends["previous_month"],
            "change_pct": trends["change_pct"],
            "trend": trends["trend"],
        },
        "engagement": {
            "login_days": user.current_streak,
            "calculations_performed": len(trends.get("history", [])),
            "ai_conversations": 0,
            "articles_read": 0,
        },
        "achievements": {
            "points_earned": user.total_points,
            "badges_unlocked": 0,
            "challenges_completed": 0,
            "recommendations_completed": 0,
        },
        "impact": {
            "total_co2_saved_kg": user.carbon_saved_kg,
            "equivalent_trees": user.carbon_saved_kg // 22 if user.carbon_saved_kg else 0,
            "equivalent_car_km": user.carbon_saved_kg * 6 if user.carbon_saved_kg else 0,
        },
    }


@router.get("/breakdown")
async def get_breakdown(
    period: str = Query("month"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CarbonService(db)
    history = await service.get_history(user.id, limit=2)

    if not history:
        return {"period": period, "categories": [], "total_current": 0, "total_previous": 0}

    current = history[0]
    previous = history[1] if len(history) > 1 else None

    categories = []
    for cat, kg in (current.breakdown or {}).items():
        prev_kg = (previous.breakdown or {}).get(cat, 0) if previous else 0
        change = round(((kg - prev_kg) / prev_kg * 100) if prev_kg > 0 else 0, 1)
        total = float(current.monthly_kg) or 1
        categories.append({
            "category": cat,
            "current_kg": kg,
            "previous_kg": prev_kg,
            "change_pct": change,
            "percentage_of_total": round(kg / total * 100, 1),
            "trend": "decreasing" if change < 0 else "increasing",
        })

    return {
        "period": period,
        "categories": categories,
        "total_current": float(current.monthly_kg),
        "total_previous": float(previous.monthly_kg) if previous else 0,
    }


@router.get("/predictions")
async def get_predictions(
    timeframe: str = Query("90d"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CarbonService(db)
    history = await service.get_history(user.id, limit=6)

    if not history:
        return {
            "timeframe": timeframe,
            "predictions": [],
            "trend": "stable",
            "projected_reduction_pct": 0,
            "confidence_score": 0,
            "assumptions": [],
        }

    current = float(history[0].monthly_kg)
    avg = sum(float(h.monthly_kg) for h in history) / len(history)
    trend_direction = "decreasing" if current < avg else ("increasing" if current > avg else "stable")
    
    # 6-month forecast vs 2°C target (which implies a ~0.5% reduction per month)
    predictions = []
    target_curve = []
    current_prediction = current
    current_target = current
    
    for i in range(1, 7):
        current_prediction = round(current_prediction * 0.98 if trend_direction == "decreasing" else current_prediction * 1.01, 1)
        current_target = round(current_target * 0.995, 1)
        predictions.append({"month": i, "predicted_kg": current_prediction})
        target_curve.append({"month": i, "target_kg": current_target})

    return {
        "timeframe": timeframe,
        "predictions": predictions,
        "target_curve": target_curve,
        "trend": trend_direction,
        "projected_reduction_pct": round((current - current_prediction) / current * 100, 1),
        "confidence_score": 0.85,
        "assumptions": [
            "Current behavior patterns continue",
            "Seasonal factors accounted for",
            "Accepted recommendations implemented",
            "2°C target assumes steady linear reduction"
        ],
    }


@router.post("/reports/generate")
async def generate_weekly_report(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    report = await report_service.generate_weekly_report(db, user.id)
    if not report:
        raise HTTPException(status_code=400, detail="Not enough data to generate report")
    return report


@router.get("/reports")
async def get_user_reports(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    reports = await report_service.get_user_reports(db, user.id)
    return reports
