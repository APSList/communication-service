import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
_level = getattr(logging, LOG_LEVEL, logging.INFO)


def configure_logging():
    fmt = "%(asctime)s %(levelname)s %(name)s: %(message)s"
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt))
    root = logging.getLogger()
    # Avoid adding duplicate handlers when imported multiple times
    if not root.handlers:
        root.addHandler(handler)
    root.setLevel(_level)


configure_logging()


def get_logger(name: str):
    """Return a module logger configured with the project's logging settings."""
    return logging.getLogger(name)

