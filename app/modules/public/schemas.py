from pydantic import BaseModel, Field

from app.database.schemas import UserProfileGender
from app.modules.exercises.schemas import (
    ExcerciseBodyPart,
    ExerciseCategory,
    ExerciseDifficulty,
    ExerciseEquipment,
    ExerciseResponse,
    ExerciseTarget,
)


class PublicCalculateFitnessRequest(BaseModel):
    age: int = Field(ge=1, le=120)
    gender: UserProfileGender
    height: float = Field(gt=0)
    weight: float = Field(gt=0)
    workout_freq_per_week: int = Field(ge=0, le=7)
    workout_duration_per_day: float = Field(ge=0)
    water_intake_daily: float = Field(gt=0)


class PublicCalculateFitnessResponse(BaseModel):
    level: str = Field(...)


class PublicRecommendExerciseRequest(BaseModel):
    body_part: ExcerciseBodyPart = Field(...)
    equipment: ExerciseEquipment = Field(...)
    target: ExerciseTarget = Field(...)
    difficulty: ExerciseDifficulty = Field(...)
    category: ExerciseCategory = Field(...)
    top_n: int = Field(default=5)


class PublicRecommendExerciseResponse(BaseModel):
    total: int = 0
    exercises: list[ExerciseResponse] = []
