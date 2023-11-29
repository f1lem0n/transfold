import logging
from pathlib import Path
from time import localtime, strftime


def get_logger(prefix: Path, name: str) -> logging.Logger:
    if not prefix.exists():
        prefix.mkdir(parents=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # add handlers if not already added
    if not logger.handlers:
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(
            f"{prefix}/{strftime(r'%Y-%m-%d_%H%M%S', localtime())}_{name}.log"
        )
        c_handler.setLevel(logging.CRITICAL)
        f_handler.setLevel(logging.DEBUG)

        c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        f_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger
