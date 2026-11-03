import logging.config

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "estandar": {"format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"},
    },
    "handlers": {
        "consola": {"class": "logging.StreamHandler", "formatter": "estandar"},
        "archivo": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 5_000_000,
            "backupCount": 3,
            "formatter": "estandar",
            "encoding": "utf-8",
        },
    },
    "root": {"level": "INFO", "handlers": ["consola", "archivo"]},
}


def setup_logging():
    logging.config.dictConfig(LOGGING)