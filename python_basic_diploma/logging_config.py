""" Файл с кастомными конфигурациями логгера. """

import logging
import logging.config


class FilterError(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR


class ColorHandler(logging.Formatter):
    colors = {
        logging.DEBUG: '\033[37m',
        logging.INFO: '\033[36m',
        logging.WARNING: '\033[33m',
        logging.ERROR: '\033[31m',
        logging.CRITICAL: '\033[101m',
    }

    reset = '\033[0m'
    fmtr_console = "%(levelname)s | %(asctime)s | %(filename)s | %(funcName)s | %(lineno)s | %(message)s"
    fmtr = logging.Formatter(fmtr_console)


    def format(self, record):
        color = self.colors[record.levelno]
        log = self.fmtr.format(record)
        reset = self.reset
        return color + log + reset


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
                "()": ColorHandler
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "base",
        },
        "info": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "when": "H",
            "interval": 24,
            "formatter": "base",
            "filename": "info.log",
        },
        "error": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "ERROR",
            "when": "H",
            "interval": 24,
            "formatter": "base",
            "filename": "error.log",
            "filters": ["error"]
        },
    },
    "loggers": {
        "bot_logger": {
            "level": "INFO",
            "handlers": ["console", "info", "error"]
        },
    },
    "filters": {
        "error": {
            "()": FilterError
        }
    }
}



def custom_logger(logger_name: str) -> logging.Logger:

    """
    Функция - для применения кастомной конфигурации Логгера
    :param logger_name: str
    :return: Logger
    """

    logging.config.dictConfig(LOGGING_CONFIG)
    log = logging.getLogger(logger_name)
    return log





