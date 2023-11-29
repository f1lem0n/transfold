from pathlib import Path
from time import localtime, strftime

from transfold.modules.logger import get_logger

LOGS_PATH = Path("tests/logs").absolute()
LOGGER_NAME = "test_logger"

start_time = strftime(r"%Y-%m-%d_%H%M%S", localtime())
logger = get_logger(LOGS_PATH, LOGGER_NAME, start_time)


def test_logger_file_handler():
    logfile = (LOGS_PATH / f"{start_time}_{LOGGER_NAME}.log").absolute()
    logger.info("This is an info message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning")
    logger.error("This is an error")
    logger.critical("This is a critical error")
    with open(logfile, "r") as f:
        lines = f.readlines()
        assert len(lines) == 5
        assert [
            "test_logger_file_handler",
            "INFO",
            "This is an info message\n",
        ] == lines[0].split(" - ")[1:]
        assert [
            "test_logger_file_handler",
            "DEBUG",
            "This is a debug message\n",
        ] == lines[1].split(" - ")[1:]
        assert [
            "test_logger_file_handler",
            "WARNING",
            "This is a warning\n",
        ] == lines[2].split(" - ")[1:]
        assert [
            "test_logger_file_handler",
            "ERROR",
            "This is an error\n",
        ] == lines[3].split(" - ")[1:]
        assert [
            "test_logger_file_handler",
            "CRITICAL",
            "This is a critical error\n",
        ] == lines[4].split(" - ")[1:]
    assert (logfile).exists()


def test_logger_console_handler(capfd):
    logger.info("This is an info message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning")
    logger.error("This is an error")
    logger.critical("This is a critical error")
    # due to a bug, pytest needs to be run with -s flag to capture stderr
    captured = capfd.readouterr()
    assert captured.err.split(" - ") == [
        "test_logger_console_handler",
        "CRITICAL",
        "This is a critical error\n",
    ]
