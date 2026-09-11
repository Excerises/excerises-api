import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.schemas import Exercise, Session, SessionExercise

from .schemas import SessionExerciseCreateRequest


class ExerciseNotFoundError(Exception):
    """Raised when one or more exercise_id do not exist."""

    def __init__(self, missing_ids: list[str]) -> None:
        self.missing_ids = missing_ids
        super().__init__(f"Exercises not found: {', '.join(missing_ids)}")


def _session_options():
    """Eager-load exercises and their exercise detail."""
    return selectinload(Session.exercises).selectinload(SessionExercise.exercise)


async def create_session(
    db: AsyncSession,
    user_id: str,
    duration: int,
    feedback: str | None,
    exercises_data: list[SessionExerciseCreateRequest],
) -> Session:
    """Create training session with its exercises in one transaction."""
    exercise_ids = [item.exercise_id for item in exercises_data]
    result = await db.execute(select(Exercise.id).where(Exercise.id.in_(exercise_ids)))
    found_ids = set(result.scalars().all())
    missing_ids = [eid for eid in exercise_ids if eid not in found_ids]
    if missing_ids:
        raise ExerciseNotFoundError(missing_ids)

    session = Session(
        id=str(uuid.uuid4()),
        user_id=user_id,
        duration=duration,
        feedback=feedback,
    )
    db.add(session)
    await db.flush()

    for item in exercises_data:
        db.add(
            SessionExercise(
                session_id=session.id,
                exercise_id=item.exercise_id,
                repetition=item.repetition,
                duration=item.duration,
            )
        )
    await db.commit()

    result = await db.execute(
        select(Session).options(_session_options()).where(Session.id == session.id)
    )
    return result.scalar_one()


async def list_sessions(db: AsyncSession, user_id: str) -> list[Session]:
    """List training sessions owned by user, newest first."""
    result = await db.execute(
        select(Session)
        .options(_session_options())
        .where(Session.user_id == user_id)
        .order_by(Session.created_at.desc())
    )
    return list(result.scalars().all())


async def get_session(
    db: AsyncSession, session_id: str, user_id: str
) -> Session | None:
    """Get single training session owned by user. Returns None if not found."""
    result = await db.execute(
        select(Session)
        .options(_session_options())
        .where(Session.id == session_id, Session.user_id == user_id)
    )
    return result.scalar_one_or_none()
