from fastapi import FastAPI, Request

from .log_middleware import log_middleware


def add_middleware(app: FastAPI):
    @app.middleware("http")
    async def log(req: Request, call_next):
        return await log_middleware(req, call_next)
