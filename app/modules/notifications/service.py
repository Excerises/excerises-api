from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.schemas import Notification


async def get_notifications(db: AsyncSession, user_id: str):
    """Get all notifications for a user."""
    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
    )
    return result.scalars().all()


async def get_unread_notifications(db: AsyncSession, user_id: str):
    """Get unread notifications for a user."""
    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == user_id, Notification.readed_at == None)
        .order_by(Notification.created_at.desc())
    )
    return result.scalars().all()


async def get_unread_count(db: AsyncSession, user_id: str) -> int:
    """Get count of unread notifications for a user."""
    total_count = await db.scalar(
        select(func.count(Notification.id)).where(Notification.user_id == user_id)
    )
    return total_count or 0


async def mark_notification_read(db: AsyncSession, notification_id: int, user_id: str):
    """Mark a single notification as read."""
    result = await db.execute(
        select(Notification).where(
            Notification.id == notification_id, Notification.user_id == user_id
        )
    )
    notification = result.scalar_one_or_none()
    if not notification:
        return None
    notification.readed_at = datetime.now(timezone.utc)
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    return notification


async def mark_all_notifications_read(db: AsyncSession, user_id: str):
    """Mark all notifications as read for a user."""
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(Notification).where(
            Notification.user_id == user_id, Notification.readed_at == None
        )
    )
    notifications = result.scalars().all()
    for notification in notifications:
        notification.readed_at = now
        db.add(notification)
    await db.commit()
    return notifications


async def delete_notification(db: AsyncSession, notification_id: int, user_id: str):
    """Delete a single notification."""
    result = await db.execute(
        select(Notification).where(
            Notification.id == notification_id, Notification.user_id == user_id
        )
    )
    notification = result.scalar_one_or_none()
    if not notification:
        return None
    await db.delete(notification)
    await db.commit()
    return notification
