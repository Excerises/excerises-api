from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.database.schemas import User
from app.modules.auth.dependencies import require_admin
from app.shared.model import ApiResponse, api_response

from .schemas import (
    DashboardStatResponse,
    PopularExerciseResponse,
    UserRegistrationsResponse,
)
from .service import get_dashboard_stat, get_popular_exercises, get_user_registrations

router = APIRouter(
    prefix="/admin/dashboard",
    tags=["Admin - Dashboard"],
    dependencies=[Depends(require_admin)],
)


@router.get("/stat", response_model=ApiResponse[DashboardStatResponse])
async def dashboard_stat(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    data = await get_dashboard_stat(db)
    return api_response("dashboard stat fetched", data)


@router.get(
    "/user-registrations", response_model=ApiResponse[UserRegistrationsResponse]
)
async def dashboard_user_registrations(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    data = await get_user_registrations(db)
    return api_response("user registrations fetched", data)


@router.get(
    "/popular-exercises",
    response_model=ApiResponse[list[PopularExerciseResponse]],
)
async def dashboard_popular_exercises(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    data = await get_popular_exercises(db)
    return api_response("popular exercises fetched", data)
