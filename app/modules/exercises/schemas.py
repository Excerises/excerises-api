from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ExerciseResponse(BaseModel):
    id: str
    name: str
    description: str | None
    body_part: str | None
    equipment: str | None
    target: str | None
    secondary_muscles: list[Any] | None
    instructions: list[Any] | None
    difficulty: str | None
    category: str | None
    created_at: datetime | None
    updated_at: datetime | None

    model_config = {"from_attributes": True}


class ExerciseDetailResponse(ExerciseResponse):
    pass


class ExerciseImportRequest(BaseModel):
    file: str = Field(..., description="Base64 encoded file content (xlsx or csv)")
    file_type: str = Field(..., description="'xlsx' or 'csv'")


class ImportResponse(BaseModel):
    success: bool
    message: str
    imported_count: int
    skipped_count: int


class ExerciseListResponse(BaseModel):
    data: list[ExerciseResponse]
    next_cursor: str | None
    has_more: bool
    limit: int
