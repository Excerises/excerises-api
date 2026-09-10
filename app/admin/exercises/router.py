from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import require_admin
from app.database.connection import get_db
from app.exercises.schemas import (
    ExerciseImportRequest,
    ExerciseListResponse,
    ImportResponse,
)
from app.exercises.service import import_exercise, list_exercises
from app.users.model import User

router = APIRouter(
    prefix="/admin/exercises",
    tags=["Admin - Exercise"],
    dependencies=[Depends(require_admin)],
)


@router.post("/import", response_model=ImportResponse)
async def admin_import_exercise(
    body: ExerciseImportRequest,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """
    Import exercises from Excel or CSV file
    - file: Base64 encoded file content
    - file_type: 'xlsx' or 'csv'
    """
    result = await import_exercise(db, body.file, body.file_type)
    return result


@router.get("", response_model=ExerciseListResponse)
async def admin_list_exercises(
    cursor: str | None = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """
    List exercises with cursor pagination
    - cursor: Name to start from (for pagination)
    - limit: Number of items per page (default: 20)
    - Returns: data, next_cursor, has_more
    """
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100",
        )

    result = await list_exercises(db, cursor, limit)
    return result
