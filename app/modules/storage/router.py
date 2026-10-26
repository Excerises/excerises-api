import uuid
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.modules.auth.dependencies import get_current_user_id
from app.modules.storage.service import get_file, upload_file
from app.shared.model.api import ApiResponse, api_response

router = APIRouter(prefix="/storage", tags=["Storage"])


@router.post("/", response_model=ApiResponse[str])
async def _upload_file(
    file: UploadFile,
    dir: str | None = None,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    result = await upload_file(file, dir)
    return api_response("File uploaded successfully", result)


@router.get("/{filepath:path}")
async def _get_file(filepath: str):
    filepath, mime_type = await get_file(filepath)
    return FileResponse(
        filepath,
        media_type=mime_type,
    )
