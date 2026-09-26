import time
from typing import Any
import uuid
from fastapi import Request, Response
from app.core import logger
from app.core.context import set_context, req_context

SENSITIVE_FIELDS = [
    "password",
    "token",
    "pin",
    "code",
    "nik",
]


def filtered_params(params: dict[str, Any]):
    filtered = {}
    for key, value in params.items():
        for sf in SENSITIVE_FIELDS:
            print(sf, key, sf.lower() in key.lower())
            if sf.lower() in key.lower():
                filtered[key] = "*redacted*"
                break

        if filtered[key] is None:
            filtered[key] = value

    return filtered


async def log_middleware(request: Request, call_next):

    request_id = (
        request.headers.get("x-request-id")
        or request.headers.get("X-Request-Id")
        or str(uuid.uuid4())
    )
    method = request.method
    url = request.url
    path = url.path
    start_time = time.time()

    token = set_context("request_id", request_id)
    set_context("path", path)
    set_context("method", method)

    information: dict[str, Any] = {}

    try:
        information["params"] = filtered_params(await request.json())
    except Exception as _:
        pass

    try:
        response: Response = await call_next(request)

        status_code = response.status_code
        duration = round((time.time() - start_time) * 100)

        information["duration"] = f"{duration}ms"
        information["status_code"] = status_code

        if status_code >= 200 and status_code <= 299:
            logger.log.info(information)
        else:
            logger.log.error(information)
        req_context.reset(token)

        return response
    except Exception as e:
        information["error"] = str(e)
        logger.log.error(information)
        req_context.reset(token)

        raise e
