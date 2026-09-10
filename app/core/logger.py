import structlog
import logging

from app.core import config

log_level = {
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "ERROR": logging.ERROR,
    "WARN": logging.WARN,
}[config.settings.LOG_LEVEL.upper()]

structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(log_level))

log = structlog.get_logger()
