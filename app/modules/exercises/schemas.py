from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

ExcerciseBodyPart = Literal[
    "waist",
    "shoulders",
    "upper legs",
    "lower arms",
    "upper arms",
    "lower legs",
    "back",
    "chest",
    "neck",
    "cardio",
]

ExerciseEquipment = Literal[
    "assisted",
    "barbell",
    "rope",
    "body weight",
    "medicine ball",
    "cable",
    "leverage machine",
    "assisted (towel)",
    "stability ball",
    "dumbbell",
    "ez barbell",
    "kettlebell",
    "body weight (with resistance band)",
    "olympic barbell",
    "weighted",
    "bosu ball",
    "sled machine",
    "smith machine",
    "wheel roller",
    "trap bar",
    "band",
]

ExerciseTarget = Literal[
    "abs",
    "delts",
    "glutes",
    "quads",
    "forearms",
    "biceps",
    "calves",
    "triceps",
    "hamstrings",
    "upper back",
    "pectorals",
    "lats",
    "adductors",
    "traps",
    "serratus anterior",
    "levator scapulae",
    "spine",
    "cardiovascular system",
    "abductors",
]

ExerciseDifficulty = Literal["advanced", "intermediate", "beginner"]

ExerciseCategory = Literal[
    "strength",
    "cardio",
    "balance",
    "rehabilitation",
    "mobility",
    "plyometrics",
    "stretching",
]


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
    file_path: str = Field(..., description="Path of file content (xlsx or csv)")


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
