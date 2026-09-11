import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.modules.auth.dependencies import get_current_user_id

from .schemas import SessionCreateRequest, SessionResponse
from .service import ExerciseNotFoundError, create_session, get_session, list_sessions

router = APIRouter(prefix="/session", tags=["Session"])


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_my_session(
    body: SessionCreateRequest,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await create_session(
            db, str(user_id), body.duration, body.feedback, body.exercises
        )
    except ExerciseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercises not found: {', '.join(e.missing_ids)}",
        )


@router.get("", response_model=list[SessionResponse])
async def list_my_sessions(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await list_sessions(db, str(user_id))


@router.get("/{session_id}", response_model=SessionResponse)
async def get_my_session(
    session_id: str,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    session = await get_session(db, session_id, str(user_id))
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )
    return session
