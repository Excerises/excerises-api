import base64
import io
import json
import ast
from typing import Any

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exercises.exercise_model import Exercise


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
    file_content: str,
    file_type: str,
) -> dict[str, Any]:
    """
    Import exercises from Excel or CSV file
    """
    try:
        decoded_data = base64.b64decode(file_content)
        buffer = io.BytesIO(decoded_data)

        if file_type == "xlsx":
            df = pd.read_excel(buffer)
        elif file_type == "csv":
            df = pd.read_csv(buffer)
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

    # Define expected columns
    expected_columns = {"name"}

    for _, row in df.iterrows():
        # Normalize column names
        normalized_row = {k.lower(): v for k, v in row.items()}

        if "name" not in normalized_row or pd.isna(normalized_row["name"]):
            skipped_count += 1
            continue

        name = str(normalized_row["name"])

        # Check if exercise exists by name
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

        # Remove None values
        data = {k: v for k, v in data.items() if pd.notna(v)}

        try:
            if existing:
                for key, value in data.items():
                    setattr(existing, key, value)
            else:
                exercise = Exercise(
                    id=str(normalized_row.get("id"))
                    if pd.notna(normalized_row.get("id"))
                    else None,
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
