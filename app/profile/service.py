from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.model import User
from app.users.profile_model import UserProfile


async def get_profile(db: AsyncSession, user_id: str) -> UserProfile | None:
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == user_id))
    return result.scalar_one_or_none()


async def create_profile(db: AsyncSession, user_id: str) -> UserProfile:
    profile = UserProfile(user_id=user_id)
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


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

    # Recalculate BMI if height or weight changed
    if profile.height and profile.weight:
        height_m = profile.height / 100
        profile.bmi = round(profile.weight / (height_m ** 2), 1)

    await db.commit()
    await db.refresh(profile)
    return profile
