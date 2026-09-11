from datetime import datetime

from pydantic import BaseModel, Field


class NewsCreatedByResponse(BaseModel):
    id: str
    name: str

    model_config = {"from_attributes": True}


class NewsResponse(BaseModel):
    id: str
    title: str
    description: str
    content: str
    viewed_count: int
    created_at: datetime | None = None
    created_by: NewsCreatedByResponse

    model_config = {"from_attributes": True}


class NewsCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    content: str = Field(min_length=1)


class NewsUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1)
    content: str | None = Field(default=None, min_length=1)
