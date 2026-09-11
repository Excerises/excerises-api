"""Utility to insert Notification entities."""

from dataclasses import dataclass
from typing import NewType

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.schemas import Notification

UserId = NewType("UserId", str)


@dataclass(frozen=True, slots=True)
class NotificationPayload:
    """Single notification input. Parsed at boundary, trusted inside."""

    user_id: str
    title: str
    description: str

    def __post_init__(self) -> None:
        if not self.user_id.strip():
            raise InvalidNotificationPayloadError(
                field="user_id", reason="must not be empty"
            )
        if not self.title.strip():
            raise InvalidNotificationPayloadError(
                field="title", reason="must not be empty"
            )
        if not self.description.strip():
            raise InvalidNotificationPayloadError(
                field="description", reason="must not be empty"
            )


@dataclass(frozen=True, slots=True)
class InvalidNotificationPayloadError(ValueError):
    """Raised when NotificationPayload fields are empty."""

    field: str
    reason: str

    def __str__(self) -> str:
        return f"invalid notification payload: {self.field} {self.reason}"


@dataclass(frozen=True, slots=True)
class NotificationSendError(Exception):
    """Raised when DB insert fails. Carries user context for boundary handling."""

    user_id: str
    detail: str

    def __str__(self) -> str:
        return f"failed to send notification to user {self.user_id}: {self.detail}"


async def send_notification(
    db: AsyncSession, payload: NotificationPayload, *, commit: bool = True
) -> Notification:
    """Insert one Notification row.

    Set commit=False when caller owns the transaction (flush only).
    """
    notification = Notification(
        user_id=payload.user_id,
        title=payload.title,
        description=payload.description,
    )
    db.add(notification)
    try:
        if commit:
            await db.commit()
            await db.refresh(notification)
        else:
            await db.flush()
    except SQLAlchemyError as e:
        if commit:
            await db.rollback()
        raise NotificationSendError(user_id=payload.user_id, detail=str(e)) from e
    return notification


async def send_notifications(
    db: AsyncSession, payloads: list[NotificationPayload], *, commit: bool = True
) -> list[Notification]:
    """Insert many Notification rows in one round-trip."""
    notifications = [
        Notification(
            user_id=p.user_id,
            title=p.title,
            description=p.description,
        )
        for p in payloads
    ]
    if not notifications:
        return []
    db.add_all(notifications)
    try:
        if commit:
            await db.commit()
            for notification in notifications:
                await db.refresh(notification)
        else:
            await db.flush()
    except SQLAlchemyError as e:
        if commit:
            await db.rollback()
        raise NotificationSendError(user_id="bulk", detail=str(e)) from e
    return notifications
