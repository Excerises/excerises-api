import structlog
import logging

from app.core import config
from app.core.context import req_context

log_level = {
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "ERROR": logging.ERROR,
    "WARN": logging.WARN,
}[config.settings.LOG_LEVEL.upper()]


def add_log_context(logger, method, event_dict):
    context = req_context.get()
    return {
        **context,
        **event_dict,
    }


def configure_logging():
    structlog.configure(
        processors=[
            add_log_context,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
    )


configure_logging()

log = structlog.get_logger()
