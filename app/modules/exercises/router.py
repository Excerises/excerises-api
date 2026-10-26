from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.shared.model import ApiResponse, api_response

from .schemas import ExerciseDetailResponse, ExerciseListResponse
from .service import get_exercise, list_exercises

router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.get("", response_model=ApiResponse[ExerciseListResponse])
async def public_list_exercises(
    cursor: str | None = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    if limit < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be greated than 1",
        )

    result = await list_exercises(db, cursor, limit)
    return api_response("exercises fetched", result)


@router.get("/{exercise_id}", response_model=ApiResponse[ExerciseDetailResponse])
async def public_get_exercise(exercise_id: str, db: AsyncSession = Depends(get_db)):
    exercise = await get_exercise(db, exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )
    return api_response("exercise fetched", exercise)
