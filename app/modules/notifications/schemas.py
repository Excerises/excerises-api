from pydantic import BaseModel


class NotificationReadResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: str | None
    readed_at: str | None
    created_at: str

    model_config = {"from_attributes": True}


class NotificationMarkReadRequest(BaseModel):
    notification_id: int


class NotificationMarkAllReadRequest(BaseModel):
    pass