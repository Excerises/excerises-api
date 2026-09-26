from fastapi import FastAPI, Request

from app.shared.model.api import ApiRequest
from .log_middleware import log_middleware


def add_middleware(app: FastAPI):
    @app.middleware("http")
    async def log(req: ApiRequest, call_next):
        return await log_middleware(req, call_next)
