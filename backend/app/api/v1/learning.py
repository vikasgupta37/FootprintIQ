"""Learning Content API — articles and quizzes."""

from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.exceptions import NotFoundException
from app.models.extras import LearningContent, Quiz
from app.models.user import User
from app.schemas.schemas import LearningContentResponse, QuizResponse

router = APIRouter()


@router.get("/content", response_model=list[LearningContentResponse])
async def get_learning_content(
    category: str = Query(None),
    difficulty: str = Query(None),
    content_type: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(LearningContent).where(LearningContent.is_published == True)
    if category:
        query = query.where(LearningContent.category == category)
    if difficulty:
        query = query.where(LearningContent.difficulty == difficulty)
    if content_type:
        query = query.where(LearningContent.content_type == content_type)
    query = query.limit(50)

    result = await db.execute(query)
    return [LearningContentResponse.model_validate(c) for c in result.scalars().all()]


@router.get("/content/{content_id}")
async def get_content_detail(content_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LearningContent).where(LearningContent.id == content_id))
    content = result.scalar_one_or_none()
    if not content:
        raise NotFoundException("Content", str(content_id))

    content.view_count += 1
    await db.flush()

    return {
        "id": content.id,
        "title": content.title,
        "content": content.content,
        "category": content.category,
        "difficulty": content.difficulty,
        "estimated_read_time": content.estimated_read_time,
        "tags": content.tags or [],
        "view_count": content.view_count,
        "like_count": content.like_count,
    }


@router.get("/quizzes")
async def get_quizzes(
    category: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Quiz).where(Quiz.is_published == True)
    if category:
        query = query.where(Quiz.category == category)

    result = await db.execute(query)
    quizzes = result.scalars().all()
    return {
        "quizzes": [
            {
                "id": q.id,
                "title": q.title,
                "category": q.category,
                "difficulty": q.difficulty,
                "question_count": len(q.questions) if q.questions else 0,
                "total_points": q.total_points,
                "passing_score": q.passing_score,
                "attempt_count": q.attempt_count,
            }
            for q in quizzes
        ]
    }
