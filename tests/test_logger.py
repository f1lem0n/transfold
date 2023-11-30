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
        assert "test_logger_file_handler" in lines[0]
        assert "INFO" in lines[0]
        assert "This is an info message\n" in lines[0]
        assert "test_logger_file_handler" in lines[1]
        assert "DEBUG" in lines[1]
        assert "This is a debug message\n" in lines[1]
        assert "test_logger_file_handler" in lines[2]
        assert "WARNING" in lines[2]
        assert "This is a warning\n" in lines[2]
        assert "test_logger_file_handler" in lines[3]
        assert "ERROR" in lines[3]
        assert "This is an error\n" in lines[3]
        assert "test_logger_file_handler" in lines[4]
        assert "CRITICAL" in lines[4]
        assert "This is a critical error\n" in lines[4]
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
        "[test_logger_console_handler]",
        "CRITICAL",
        "This is a critical error\n",
    ]


def test_logger_verbose(capsys):
    # overwrite logger with verbose logger
    logger = get_logger(LOGS_PATH, LOGGER_NAME, start_time, verbose=True)
    logger.info("This is an info message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning")
    logger.error("This is an error")
    logger.critical("This is a critical error")
    captured_verbose = capsys.readouterr()
    assert "test_logger_verbose" in captured_verbose.err
    assert "INFO" in captured_verbose.err
    assert "This is an info message\n" in captured_verbose.err
    assert "DEBUG" in captured_verbose.err
    assert "This is a debug message\n" in captured_verbose.err
    assert "WARNING" in captured_verbose.err
    assert "This is a warning\n" in captured_verbose.err
    assert "ERROR" in captured_verbose.err
    assert "This is an error\n" in captured_verbose.err
    assert "CRITICAL" in captured_verbose.err
    assert "This is a critical error\n" in captured_verbose.err
