from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ExerciseLevelDistribution(BaseModel):
    labels: list[str]
    dataset: list[int]


class DashboardStatResponse(BaseModel):
    total_users: int
    total_exercises: int
    total_body_parts: int
    exercise_level_distribution: ExerciseLevelDistribution


class UserRegistrationsResponse(BaseModel):
    dataset: list[int]
    recent_users: list["RecentUserResponse"]


class RecentUserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class PopularExerciseResponse(BaseModel):
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
    usage_percentage: float

    model_config = {"from_attributes": True}
