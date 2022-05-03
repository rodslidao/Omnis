
from logging import getLogger, DEBUG, INFO, WARNING, ERROR, CRITICAL
from src.utility.system.log_setup.setup import default_setup
from src.utility.system.log_setup.decorators import exception

levels = {
    "debug": DEBUG,
    "info": INFO,
    "warning": WARNING,
    "error": ERROR,
    "critical": CRITICAL,
}
lvl = "info"

log_paths = ["src/logs/untimed_log.json", "src/logs/timed_log.json"]
logger = default_setup(getLogger(str(__name__)), *log_paths, level=levels[lvl])

# custom_handler(logger, "mongo", "json", dbo, levels[lvl])

if __name__ == "__main__":

    @exception(logger)
    def test_log():
        logger.debug("debug")
        logger.info("info")
        logger.warning("warning")
        logger.error("error")
        logger.critical("critical")
