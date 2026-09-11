from datetime import datetime

from pydantic import BaseModel, Field


class SessionExerciseCreateRequest(BaseModel):
    exercise_id: str = Field(min_length=1)
    repetition: int | None = Field(default=None, ge=0)
    duration: int | None = Field(default=None, ge=0)


class SessionCreateRequest(BaseModel):
    duration: int = Field(default=0, ge=0)
    feedback: str | None = None
    exercises: list[SessionExerciseCreateRequest] = Field(min_length=1)


class SessionExerciseBriefResponse(BaseModel):
    id: str
    name: str
    body_part: str | None = None
    equipment: str | None = None
    target: str | None = None
    difficulty: str | None = None
    category: str | None = None

    model_config = {"from_attributes": True}


class SessionExerciseResponse(BaseModel):
    id: int
    exercise_id: str
    repetition: int | None = None
    duration: int | None = None
    exercise: SessionExerciseBriefResponse | None = None

    model_config = {"from_attributes": True}


class SessionResponse(BaseModel):
    id: str
    duration: int
    feedback: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    exercises: list[SessionExerciseResponse] = []

    model_config = {"from_attributes": True}
