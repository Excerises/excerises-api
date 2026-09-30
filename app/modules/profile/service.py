from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.schemas import User
from app.database.schemas import UserProfile
from app.shared.utils.fitness import (
    calculate_age,
    calculate_bmi,
    calculate_fitness_level,
)


async def get_profile(db: AsyncSession, user_id: str) -> User | None:
    result = await db.execute(
        select(User).options(selectinload(User.profile)).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def update_profile(db: AsyncSession, user_id: str, data: dict) -> UserProfile:
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == user_id))
    profile = result.scalar_one_or_none()
    if not profile:
        profile = UserProfile(user_id=user_id)
        db.add(profile)
        await db.flush()

    for key, value in data.items():
        if value is not None:
            setattr(profile, key, value)

    if profile.height and profile.weight:
        profile.bmi = calculate_bmi(profile.height, profile.weight)

    profile.fitness_level = calculate_fitness_level(
        gender=profile.gender,
        age=calculate_age(profile.birth_date),
        height=profile.height,
        weight=profile.weight,
        workout_freq_per_week=profile.workout_freq_per_week,
        workout_duration_per_day=profile.workout_duration_per_day,
        water_intake_daily=profile.water_intake_daily,
    )

    await db.commit()
    await db.refresh(profile)
    return profile
