from contextvars import ContextVar
from typing import Any

req_context: ContextVar[dict[str, Any]] = ContextVar("request_context", default={})


def set_context(key: str, value: Any | None):
    data = req_context.get().copy()
    data[key] = value

    return req_context.set(data)


def get_context(key: str):
    return req_context.get().get(key)


def del_context(key: str):
    data = req_context.get().copy()
    data.pop(key)

    req_context.set(data)
