import logging
from pathlib import Path


class TransfoldLogger(object):
    def __new__(
        self,
        prefix: Path,
        name: str,
        start_time: str,
        logging_level: int,
        verbose=False,
    ):
        if not prefix.exists():  # pragma: no cover
            prefix.mkdir(parents=True)

        logger = logging.getLogger(name)
        level = (logging_level + 1) * 10
        logger.setLevel(level)
        # overwrite handlers if they already exist
        if logger.handlers:
            logger.handlers.clear()
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(f"{prefix}/{start_time}_{name}.log")
        if verbose:
            c_handler.setLevel(level)
            c_format = logging.Formatter(
                "%(asctime)-30s %(funcName)-40s %(levelname)-10s %(message)s"
            )
        else:
            c_handler.setLevel(logging.CRITICAL)
            c_format = logging.Formatter(
                "[%(funcName)s] - %(levelname)s - %(message)s"
            )

        f_handler.setLevel(logging.DEBUG)
        f_format = logging.Formatter(
            "%(asctime)-30s %(funcName)-40s %(levelname)-10s %(message)s"
        )
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        return logger
