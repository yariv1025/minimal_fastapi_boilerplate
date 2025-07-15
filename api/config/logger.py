import logging
from logging.config import dictConfig

_LOGGING_ALREADY_CONFIGURED = False

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s | PID %(process)d | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
        },
        "simple": {
            "format": "%(levelname)s | %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",  # use DEBUG in dev if needed
    },
    "loggers": {
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False
        },
    },
}


def setup_logging() -> None:
    """
    Apply the logging configuration.
    """
    global _LOGGING_ALREADY_CONFIGURED

    if _LOGGING_ALREADY_CONFIGURED:
        return

    dictConfig(LOGGING_CONFIG)
    logging.getLogger(__name__).info("Logging is configured.")
    _LOGGING_ALREADY_CONFIGURED = True