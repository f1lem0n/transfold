import logging
from pathlib import Path


def get_logger(prefix: Path, name: str, start_time: str) -> logging.Logger:
    if not prefix.exists():
        prefix.mkdir(parents=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # add handlers if not already added
    if not logger.handlers:
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(f"{prefix}/{start_time}_{name}.log")
        c_handler.setLevel(logging.CRITICAL)
        f_handler.setLevel(logging.DEBUG)

        c_format = logging.Formatter(
            "%(funcName)s - %(levelname)s - %(message)s"
        )
        f_format = logging.Formatter(
            "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
        )
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger
