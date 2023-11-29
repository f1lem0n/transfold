from pathlib import Path
from time import localtime, strftime

from transfold.modules.logger import get_logger

LOGS_PATH = Path("tests/logs").absolute()
LOGGER_NAME = "test_logger"


def test_logger_file_handler():
    logger = get_logger(LOGS_PATH, LOGGER_NAME)
    logfile = (
        LOGS_PATH
        / f"{strftime('%Y-%m-%d_%H%M%S', localtime())}_{LOGGER_NAME}.log"
    ).absolute()
    logger.info("This is an info message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning")
    logger.error("This is an error")
    logger.critical("This is a critical error")
    with open(logfile, "r") as f:
        lines = f.readlines()
        # assert len(lines) == 5
        assert ["test_logger", "INFO", "This is an info message\n"] == lines[
            0
        ].split(" - ")[1:]
        assert ["test_logger", "DEBUG", "This is a debug message\n"] == lines[
            1
        ].split(" - ")[1:]
        assert ["test_logger", "WARNING", "This is a warning\n"] == lines[
            2
        ].split(" - ")[1:]
        assert ["test_logger", "ERROR", "This is an error\n"] == lines[
            3
        ].split(" - ")[1:]
        assert [
            "test_logger",
            "CRITICAL",
            "This is a critical error\n",
        ] == lines[4].split(" - ")[1:]
    assert (logfile).exists()


def test_logger_console_handler(capfd):
    logger = get_logger(LOGS_PATH, LOGGER_NAME)
    logger.info("This is an info message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning")
    logger.error("This is an error")
    logger.critical("This is a critical error")
    # due to a bug, pytest needs to be run with -s flag to capture stderr
    captured = capfd.readouterr()
    assert (
        captured.err == "test_logger - CRITICAL - This is a critical error\n"
    )
