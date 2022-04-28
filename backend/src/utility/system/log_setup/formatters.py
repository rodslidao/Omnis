from logging import Formatter, getLogger
from json import dumps
from traceback import format_exception
from datetime import datetime
from coloredlogs import ColoredFormatter

logger = getLogger(__name__)


class JsonFormatter(Formatter):
    """
    JsonFormatter : extends logging.Formatter
    """

    def __init__(self):
        pass

    def get_exc_fields(self, record):
        """
        returns execution/exception info for log record
        """
        if record.exc_info:
            exc_info = self.format_exception(record.exc_info)
        else:
            exc_info = record.exc_text
        return {"exc_info": exc_info}

    @classmethod
    def format_exception(cls, exc_info):
        return "".join(format_exception(*exc_info)) if exc_info else ""

    def format(self, record, *args, **kw):
        """
        :param takes log record, function logging.Formatter.format\n
        :returns JSON Structured Logging Format
        """
        json_log_object = {
            "@timestamp": datetime.utcnow().isoformat(),
            "error": {"stack_trace": self.get_exc_fields(record)},
            "event": {
                "created": datetime.utcfromtimestamp(record.created).isoformat(),
                "module": record.module,
            },
            "log": {
                "level": record.levelname,
                "logger": record.name,
                "origin": {
                    "file": {
                        "line": record.lineno,
                        "name": record.filename,
                        "fullpath": record.pathname,
                    },
                    "function": record.funcName,
                },
            },
            "message": record.getMessage(),
            "process": {
                "pid": record.process,
                "name": record.name,
                "thread": {
                    "id": record.thread,
                    "name": record.threadName,
                },
            },
        }
        return dumps(remove_none(json_log_object))


def remove_none(d):
    try:
        if not isinstance(d, (dict, list)):
            return d
        if isinstance(d, list):
            return [v for v in (remove_none(v) for v in d) if v]
        return {k: v for k, v in ((k, remove_none(v)) for k, v in d.items()) if v}
    except Exception:
        logger.exception("Issue stripping None value from nested object")


console_formatter = ColoredFormatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

formatters = {"json": JsonFormatter(), "console": console_formatter}
