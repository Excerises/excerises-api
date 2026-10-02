from fastapi import APIRouter

from app.modules.exercises.service import recommend_exercise
from app.shared.model import ApiResponse, api_response
from app.shared.utils.fitness import calculate_fitness_level

from .schemas import (
    PublicCalculateFitnessRequest,
    PublicCalculateFitnessResponse,
    PublicRecommendExerciseRequest,
    PublicRecommendExerciseResponse,
)

router = APIRouter(tags=["Public"])


@router.post(
    "/calculate-fitness",
    response_model=ApiResponse[PublicCalculateFitnessResponse],
    summary="Calculate Fitness Level",
)
async def public_calculate_fitness(body: PublicCalculateFitnessRequest):
    level = calculate_fitness_level(
        gender=body.gender,
        age=body.age,
        height=body.height,
        weight=body.weight,
        workout_freq_per_week=body.workout_freq_per_week,
        workout_duration_per_day=body.workout_duration_per_day,
        water_intake_daily=body.water_intake_daily,
    )
    return api_response("fitness level calculated", {"level": level})


@router.post(
    "/recommend-exercise",
    response_model=ApiResponse[PublicRecommendExerciseResponse],
    summary="Recommend Exercises",
)
async def public_recommend_exercise(body: PublicRecommendExerciseRequest):
    exercises = await recommend_exercise(
        body_part=body.body_part,
        equipment=body.equipment,
        target=body.target,
        difficulty=body.difficulty,
        category=body.category,
        top_n=body.top_n,
    )

    return api_response(
        "exercise recommendation fetched",
        {
            "total": len(exercises),
            "exercises": exercises,
        },
    )
