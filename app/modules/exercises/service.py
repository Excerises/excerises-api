import base64
import io
import json
import ast
import random
import tempfile
from typing import Any

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.ai import load_exercise_recommendation_model, _hub_download
from app.database.connection import async_session
from app.core.config import settings
from app.core.disk import s3_download
from app.database.schemas import Exercise
from app.modules.exercises.schemas import (
    ExcerciseBodyPart,
    ExerciseCategory,
    ExerciseDifficulty,
    ExerciseEquipment,
    ExerciseTarget,
)

_df_exercise: pd.DataFrame | None = None


def parse_list_string(value: Any) -> list | None:
    if not value or pd.isna(value):
        return None
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            try:
                return ast.literal_eval(value)
            except ValueError, SyntaxError:
                try:
                    return json.loads(value.replace("'", '"'))
                except json.JSONDecodeError:
                    return [v.strip() for v in value[1:-1].split(",")]
        return [value]
    return [str(value)]


async def import_exercise(
    db: AsyncSession,
    file_path: str,
) -> dict[str, Any]:
    """
    Import exercises from Excel or CSV file
    """
    try:
        with tempfile.NamedTemporaryFile() as tmp_file:
            file_type = file_path.split(".")[-1].lower()
            s3_download(file_path, tmp_file.name)

            if file_type == "xlsx":
                df = pd.read_excel(tmp_file.name)
            elif file_type == "csv":
                df = pd.read_csv(tmp_file.name)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to read file: {str(e)}",
            "imported_count": 0,
            "skipped_count": 0,
        }

    imported_count = 0
    skipped_count = 0

    for _, row in df.iterrows():
        normalized_row = {str(k).lower(): v for k, v in row.items()}

        if "name" not in normalized_row or pd.isna(normalized_row["name"]):
            skipped_count += 1
            continue

        name = str(normalized_row["name"])

        stmt = select(Exercise).where(Exercise.name == name)
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()

        data = {
            "description": normalized_row.get("description"),
            "body_part": normalized_row.get("body_part"),
            "equipment": normalized_row.get("equipment"),
            "target": normalized_row.get("target"),
            "secondary_muscles": parse_list_string(
                normalized_row.get("secondary_muscles")
            ),
            "instructions": parse_list_string(normalized_row.get("instructions")),
            "difficulty": normalized_row.get("difficulty"),
            "category": normalized_row.get("category"),
        }

        try:
            if existing:
                for key, value in data.items():
                    setattr(existing, key, value)
            else:
                exercise = Exercise(
                    id=str(int(normalized_row.get("id", random.randint(1000, 9999)))),
                    name=name,
                    **data,
                )
                db.add(exercise)
            imported_count += 1
        except Exception:
            skipped_count += 1
            continue

    await db.commit()

    return {
        "success": True,
        "message": "Import completed successfully",
        "imported_count": imported_count,
        "skipped_count": skipped_count,
    }


async def list_exercises(
    db: AsyncSession,
    cursor: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """
    List exercises with cursor pagination (ordered by name ASC)
    """
    stmt = select(Exercise)
    if cursor:
        stmt = stmt.where(Exercise.name > cursor)

    stmt = stmt.order_by(Exercise.name.asc()).limit(limit + 1)

    result = await db.execute(stmt)
    exercises = result.scalars().all()

    has_more = len(exercises) > limit
    if has_more:
        exercises = exercises[:limit]
        next_cursor = exercises[-1].name
    else:
        next_cursor = None

    return {
        "data": exercises,
        "next_cursor": next_cursor,
        "has_more": has_more,
        "limit": limit,
    }


def load_exercise_recommendation_dataframe() -> pd.DataFrame:
    global _df_exercise

    if _df_exercise is not None:
        return _df_exercise

    csv_path = _hub_download(settings.HF_EXERCISE_RECOMMENDATION_CSV)
    _df_exercise = pd.read_csv(csv_path)

    return _df_exercise


async def recommend_exercise(
    body_part: ExcerciseBodyPart,
    equipment: ExerciseEquipment,
    target: ExerciseTarget,
    difficulty: ExerciseDifficulty,
    category: ExerciseCategory,
    top_n: int = 5,
) -> list[Exercise]:
    input_dict = {
        "body_part": [body_part],
        "equipment": [equipment],
        "target": [target],
        "difficulty": [difficulty],
        "category": [category],
    }
    df = load_exercise_recommendation_dataframe()
    p = load_exercise_recommendation_model()

    X = pd.DataFrame(input_dict)
    X_encoded = p.feature_encoder.transform(X)

    _, indices = p.model.kneighbors(X_encoded, n_neighbors=top_n)

    exercises_id = []
    for indice in indices[0]:
        exercise = df.iloc[indice]
        exercises_id.append(exercise["id"])

    async with async_session() as db:
        query = await db.execute(select(Exercise).where(Exercise.id.in_(exercises_id)))
        exercises = list(query.scalars().all())

    return exercises
