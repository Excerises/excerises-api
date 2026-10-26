import mimetypes
from os.path import exists
import uuid
from fastapi import UploadFile
from pathlib import Path

_storage_dir = "./storage"


def _ensure_dir_exist(dir: str | None):
    dir = dir or "/"
    normalized_dir = dir if dir.startswith("/") else f"/{dir}"

    path = Path(f"{_storage_dir}{normalized_dir}")
    path.mkdir(parents=True, exist_ok=True)

    return normalized_dir


async def upload_file(file: UploadFile, dir: str | None = None):
    dir = _ensure_dir_exist(dir)
    filename = (
        f"{uuid.uuid4()}.{file.filename.split('.')[-1] if file.filename else "txt"}"
    )
    filepath = f"{dir}/{filename}"
    with open(f"{_storage_dir}{filepath}", "wb") as f:
        content = await file.read()
        f.write(content)

    return filepath


async def get_file(filepath: str):
    normalized_filepath = filepath if filepath.startswith("/") else f"/{filepath}"
    filepath = f"{_storage_dir}{normalized_filepath}"
    if not exists(filepath):
        raise ValueError("File not found")

    media_type, _ = mimetypes.guess_type(filepath)
    return filepath, media_type or "application/octet-stream"
