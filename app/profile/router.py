import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user_id
from app.database.connection import get_db

from .schemas import (
    CalculateFitnessLevelRequest,
    CalculateFitnessLevelResponse,
    ProfileResponse,
    ProfileUpdateRequest,
)
from .service import calculate_fitness_level, get_profile, update_profile

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("", response_model=ProfileResponse)
async def get_my_profile(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    user = await get_profile(db, str(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.patch("", response_model=ProfileResponse)
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
    return user


@router.post("/calculate-fitness", response_model=CalculateFitnessLevelResponse)
async def calculate_my_fitness_level(
    body: CalculateFitnessLevelRequest | None = None,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    data = body.model_dump(exclude_unset=True) if body else {}
    level = await calculate_fitness_level(db, str(user_id), data)
    return {"level": level}
