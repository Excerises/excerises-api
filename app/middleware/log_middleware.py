import datetime
import time
import uuid
from fastapi import Response

from app.core import logger
from app.shared.model.api import ApiRequest


def filtered_params(params: dict):
    exceptions = ["password", "token", "pin", "code"]

    filtered = {}
    for key, value in params.items():
        filtered[key] = value if key not in exceptions else "*redacted*"

    return filtered


async def log_middleware(request: ApiRequest, call_next):
    method = request.method
    url = request.url
    path = url.path
    start_time = time.time()
    params = filtered_params(await request.json())

    request.id = str(uuid.uuid4())
    response: Response = await call_next(request)

    status_code = response.status_code
    duration = round((time.time() - start_time) * 100)

    information = {
        "id": request.id,
        "time": datetime.datetime.now().isoformat(),
        "method": method,
        "path": path,
        "duration": f"{duration}ms",
        "status_code": status_code,
        "params": params,
    }

    if status_code >= 200 and status_code <= 299:
        logger.log.info(information)
    else:
        logger.log.error(information)

    return response
