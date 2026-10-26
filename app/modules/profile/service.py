from datetime import date, timedelta

from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.schemas import Session, SessionExercise, User
from app.database.schemas import UserProfile
from app.modules.auth.service import hash_password
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


async def update_profile_auth(db: AsyncSession, user_id: str, data: dict) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise ValueError("User not found")

    if data.get("email") is not None:
        existing = await db.execute(
            select(User).where(User.email == data["email"], User.id != user_id)
        )
        if existing.scalar_one_or_none():
            raise ValueError("Email already taken")
        user.email = data["email"]

    if data.get("name") is not None:
        user.name = data["name"]

    if data.get("password") is not None:
        user.hashed_password = hash_password(data["password"])

    await db.commit()
    await db.refresh(user)
    return user


async def get_progress(db: AsyncSession, user_id: str) -> dict:
    rows = (
        await db.execute(
            select(Session.created_at, Session.duration).where(
                Session.user_id == user_id
            )
        )
    ).all()

    workouts = (
        await db.execute(
            select(func.count(distinct(SessionExercise.exercise_id)))
            .join(Session, Session.id == SessionExercise.session_id)
            .where(Session.user_id == user_id)
        )
    ).scalar_one()

    seconds = sum(duration or 0 for _, duration in rows)
    trained_dates = {created_at.date() for created_at, _ in rows}

    streaks = 0
    day = date.today()
    if day not in trained_dates:
        day -= timedelta(days=1)
    while day in trained_dates:
        streaks += 1
        day -= timedelta(days=1)

    today = date.today()
    monday = today - timedelta(days=today.weekday())
    weekly_durations = [0] * 7
    for created_at, duration in rows:
        offset = (created_at.date() - monday).days
        if 0 <= offset < 7:
            weekly_durations[offset] += duration or 0

    return {
        "streaks": streaks,
        "workouts": workouts,
        "minutes": seconds / 60,
        "weeklyDurations": weekly_durations,
    }
