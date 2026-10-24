from datetime import datetime

from pydantic import BaseModel


class NotificationReadResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: str | None
    readed_at: datetime | None
    created_at: datetime | None

    model_config = {"from_attributes": True}


class NotificationMarkReadRequest(BaseModel):
    notification_id: int


class NotificationMarkAllReadRequest(BaseModel):
    pass
