from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import require_admin
from app.database.connection import get_db
from app.users.model import User

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
    get_user_with_profile,
    list_users,
    update_user_password,
    update_user_profile,
)

router = APIRouter(
    prefix="/admin/users",
    tags=["Admin - User"],
    dependencies=[Depends(require_admin)],
)


@router.get("", response_model=list[AdminUserResponse])
async def admin_list_users(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    return await list_users(db)


@router.post("", response_model=AdminUserResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_user(
    body: AdminUserCreateRequest,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    try:
        return await create_user(
            db, body.name, str(body.email), body.password, body.role
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=AdminUserDetailResponse)
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
    return user


@router.put("/{user_id}/auth", response_model=AdminUserResponse)
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
    return user


@router.put("/{user_id}/profile", response_model=AdminUserDetailResponse)
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
    return user


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
    return None
