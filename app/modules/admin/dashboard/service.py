from datetime import datetime

from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.schemas import Exercise, Session, SessionExercise, User


async def get_dashboard_stat(db: AsyncSession) -> dict:
    total_users = (await db.execute(select(func.count(User.id)))).scalar() or 0
    total_exercise = (await db.execute(select(func.count(Exercise.id)))).scalar() or 0
    total_body_parts = (
        await db.execute(
            select(func.count(distinct(Exercise.body_part))).where(
                Exercise.body_part.isnot(None)
            )
        )
    ).scalar() or 0

    levels = ["beginner", "intermediate", "advanced"]
    dataset = []
    for level in levels:
        count = (
            await db.execute(
                select(func.count(Exercise.id)).where(Exercise.difficulty == level)
            )
        ).scalar() or 0
        dataset.append(count)

    return {
        "total_users": total_users,
        "total_exercise": total_exercise,
        "total_body_parts": total_body_parts,
        "exercise_level_distribution": {
            "labels": levels,
            "dataset": dataset,
        },
    }


async def get_user_registrations(db: AsyncSession) -> dict:
    now = datetime.now()
    year = now.year

    dataset = []
    for month in range(1, 13):
        count = (
            await db.execute(
                select(func.count(User.id)).where(
                    func.year(User.created_at) == year,
                    func.month(User.created_at) == month,
                )
            )
        ).scalar() or 0
        dataset.append(count)

    result = await db.execute(
        select(User).order_by(User.created_at.desc()).limit(5)
    )
    recent_users = list(result.scalars().all())

    return {
        "dataset": dataset,
        "recent_users": recent_users,
    }


async def get_popular_exercises(db: AsyncSession) -> list[dict]:
    total_users_with_sessions = (
        await db.execute(
            select(func.count(distinct(Session.user_id)))
        )
    ).scalar() or 0

    if total_users_with_sessions == 0:
        return []

    # count distinct users per exercise
    stmt = (
        select(
            Exercise,
            func.count(distinct(Session.user_id)).label("user_count"),
        )
        .join(SessionExercise, SessionExercise.exercise_id == Exercise.id)
        .join(Session, Session.id == SessionExercise.session_id)
        .group_by(Exercise.id)
        .order_by(func.count(distinct(Session.user_id)).desc())
        .limit(5)
    )

    result = await db.execute(stmt)
    rows = result.all()

    exercises = []
    for exercise, user_count in rows:
        exercises.append(
            {
                "id": exercise.id,
                "name": exercise.name,
                "description": exercise.description,
                "body_part": exercise.body_part,
                "equipment": exercise.equipment,
                "target": exercise.target,
                "secondary_muscles": exercise.secondary_muscles,
                "instructions": exercise.instructions,
                "difficulty": exercise.difficulty,
                "category": exercise.category,
                "created_at": exercise.created_at,
                "updated_at": exercise.updated_at,
                "usage_percentage": round(
                    (user_count / total_users_with_sessions) * 100, 2
                ),
            }
        )

    return exercises
