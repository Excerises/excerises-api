from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from app.modules.auth.dependencies import get_current_user_id
from app.modules.notifications.service import (
    delete_notification,
    get_notifications,
    get_unread_count,
    mark_all_notifications_read,
    mark_notification_read,
)
from app.shared.model import ApiResponse, api_response
from app.database.connection import get_db

from .schemas import NotificationReadResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=ApiResponse[List[NotificationReadResponse]])
async def list_notifications(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    notifications = await get_notifications(db, str(user_id))
    return api_response("notifications fetched", notifications)


@router.get(
    "/{notification_id}/read", response_model=ApiResponse[NotificationReadResponse]
)
async def mark_notification_read_fn(
    notification_id: int,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    notification = await mark_notification_read(db, notification_id, str(user_id))
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found"
        )
    return api_response("notification marked as read", notification)


@router.get("/read-all", response_model=ApiResponse[List[NotificationReadResponse]])
async def mark_all_notifications_read_fn(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    notifications = await mark_all_notifications_read(db, str(user_id))
    return api_response("all notifications marked as read", notifications)


@router.delete(
    "/{notification_id}", response_model=ApiResponse[NotificationReadResponse]
)
async def delete_notification_endpoint(
    notification_id: int,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    notification = await delete_notification(db, notification_id, str(user_id))
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found"
        )
    return api_response("notification deleted", notification)


@router.get("/unread-count", response_model=ApiResponse[int])
async def get_unread_count_endpoint(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    count = await get_unread_count(db, str(user_id))
    return api_response("unread count fetched", count)
