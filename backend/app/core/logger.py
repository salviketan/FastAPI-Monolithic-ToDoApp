import logging
import sys
from logging.config import dictConfig
from pathlib import Path
from typing import Any, TextIO

from app.core.config import BASE_DIR

logging_config: dict[
    str,
    int
    | dict[str, dict[str, str]]
    | dict[str, dict[str, str | int] | dict[str, str | TextIO | Any]],
] = {
    "version": 1,
    "formatters": {
        "verbose": {
            "format": ("[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"),
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {
            "format": "%(levelname)s %(message)s",
        },
    },
    "handlers": {
        "api-logger": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            # API log usually captures high-level traffic status
            "level": logging.INFO,
            "filename": "logs/api.log",
            "maxBytes": 26214400,
            "backupCount": 7,
        },
        # ADDED: Handlers specifically for granular code debugging
        "debug-logger": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "level": logging.DEBUG,
            "filename": "logs/debug.log",
            "maxBytes": 26214400,
            "backupCount": 7,
        },
        "batch-process-logger": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "level": logging.DEBUG,
            "filename": "logs/batch.log",
            "maxBytes": 26214400,
            "backupCount": 7,
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "api_logger": {
            "handlers": ["api-logger", "console"],
            "level": logging.INFO,
        },
        "debug_logger": {
            "handlers": ["debug-logger", "console"],
            "level": logging.DEBUG,
        },
        # "batch_process_logger": {
        #     "handlers": ["batch-process-logger", "console"],
        #     "level": logging.DEBUG,
        # },
    },
}


# 1. Define the path to the logs directory
logs_dir: Path = BASE_DIR.parent / "logs"

# 2. Create the folder automatically if it doesn't exist
logs_dir.mkdir(parents=True, exist_ok=True)

# 3. Load your configuration securely
dictConfig(logging_config)


api_logger: logging.Logger = logging.getLogger("api_logger")
debug_logger: logging.Logger = logging.getLogger("debug_logger")
# batch_process_logger: logging.Logger = logging.getLogger("batch_process_logger")
