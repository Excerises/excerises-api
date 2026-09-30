from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import require_admin
from app.database.connection import get_db
from app.database.schemas import User
from app.shared.model import ApiResponse, api_response

from app.modules.session.schemas import SessionResponse

from .schemas import (
    AdminUserAuthUpdateRequest,
    AdminUserCreateRequest,
    AdminUserDetailResponse,
    AdminUserProfileUpdateRequest,
    AdminUserResponse,
)
from .service import (
    create_user,
    delete_user,
    get_user_session,
    get_user_with_profile,
    list_user_sessions,
    list_users,
    update_user_password,
    update_user_profile,
)

router = APIRouter(
    prefix="/admin/users",
    tags=["Admin - User"],
    dependencies=[Depends(require_admin)],
)


@router.get("", response_model=ApiResponse[list[AdminUserResponse]])
async def admin_list_users(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    users = await list_users(db)
    return api_response("users fetched", users)


@router.post(
    "",
    response_model=ApiResponse[AdminUserResponse],
    status_code=status.HTTP_201_CREATED,
)
async def admin_create_user(
    body: AdminUserCreateRequest,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    try:
        user = await create_user(
            db, body.name, str(body.email), body.password, body.role
        )
        return api_response("user created", user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=ApiResponse[AdminUserDetailResponse])
async def admin_get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    user = await get_user_with_profile(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return api_response("user fetched", user)


@router.put("/{user_id}/auth", response_model=ApiResponse[AdminUserResponse])
async def admin_update_user_auth(
    user_id: str,
    body: AdminUserAuthUpdateRequest,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    user = await update_user_password(db, user_id, body.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return api_response("auth user updated", user)


@router.put("/{user_id}/profile", response_model=ApiResponse[AdminUserDetailResponse])
async def admin_update_user_profile(
    user_id: str,
    body: AdminUserProfileUpdateRequest,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    data = body.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update"
        )
    profile = await update_user_profile(db, user_id, data)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user = await get_user_with_profile(db, user_id)
    return api_response("user detail fetched", user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    ok = await delete_user(db, user_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return api_response("user deleted")


@router.get("/{user_id}/sessions", response_model=ApiResponse[list[SessionResponse]])
async def admin_list_user_sessions(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    user = await get_user_with_profile(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    sessions = await list_user_sessions(db, user_id)
    return api_response("sessions fetched", sessions)


@router.get(
    "/{user_id}/sessions/{session_id}", response_model=ApiResponse[SessionResponse]
)
async def admin_get_user_session(
    user_id: str,
    session_id: str,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    user = await get_user_with_profile(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    session = await get_user_session(db, user_id, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )
    return api_response("session fetched", session)
