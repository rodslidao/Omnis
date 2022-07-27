
from logging import getLogger, DEBUG, INFO, WARNING, ERROR, CRITICAL
from src.utility.system.log_setup.setup import default_setup, custom_handler
from src.utility.system.log_setup.decorators import exception
from dotenv import load_dotenv
from os import environ
# load_dotenv()
# load_dotenv(f'.env.{environ.get("NODE_ENV")}')

levels = {
    "debug": DEBUG,
    "info": INFO,
    "warning": WARNING,
    "error": ERROR,
    "critical": CRITICAL,
}
lvl = environ.get("LOG_LEVEL", "debug").lower()

log_paths = ["src/logs/untimed_log.json", "src/logs/timed_log.json"]
logger = default_setup(getLogger(str(__name__)), *log_paths, level=levels[lvl])
if __name__ == "__main__":

    @exception(logger)
    def test_log():
        logger.debug("debug")
        logger.info("info")
        logger.warning("warning")
        logger.error("error")
        logger.critical("critical")
