import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import get_current_user_id
from app.database.connection import get_db
from app.shared.model import ApiResponse, api_response

from .schemas import (
    CalculateFitnessLevelResponse,
    ProfileResponse,
    ProfileUpdateRequest,
)
from .service import get_profile, update_profile
from app.shared.utils.fitness import calculate_fitness_level

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("", response_model=ApiResponse[ProfileResponse])
async def get_my_profile(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    user = await get_profile(db, str(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return api_response("get profile successful", user)


@router.patch("", response_model=ApiResponse[ProfileResponse])
async def update_my_profile(
    body: ProfileUpdateRequest,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    data = body.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update"
        )
    profile = await update_profile(db, str(user_id), data)
    user = await get_profile(db, str(user_id))
    return api_response("update profile successful", user)


@router.post(
    "/calculate-fitness", response_model=ApiResponse[CalculateFitnessLevelResponse]
)
async def calculate_my_fitness_level(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    user = await get_profile(db, str(user_id))
    if not user or not user.profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complete your profile first",
        )

    profile = user.profile
    today = date.today()
    age = (
        today.year
        - profile.birth_date.year
        - ((today.month, today.day) < (profile.birth_date.month, profile.birth_date.day))
        if profile.birth_date
        else 25
    )

    level = calculate_fitness_level(
        age=age,
        height=profile.height or 0,
        weight=profile.weight or 0,
        bmi=profile.bmi or 0,
        workout_freq_per_week=profile.workout_freq_per_week or 0,
        workout_duration_per_day=profile.workout_duration_per_day or 0,
    )
    return api_response("fitness level calculated", {"level": level})
