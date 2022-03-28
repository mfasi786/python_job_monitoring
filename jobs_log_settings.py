import sys
import logging
from logging.config import dictConfig

logging_config = dict(
    version=1,
    formatters={
        'verbose': {
            'format': ("[%(asctime)s] %(levelname)s "
                       "[%(name)s:%(lineno)s] %(message)s"),
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    handlers={
        'custom_logger': {'class': 'logging.handlers.RotatingFileHandler',
                           'formatter': 'verbose',
                           'level': logging.DEBUG,
                           'filename': 'CEMonitorLogs/CEMonitorLogs.txt',
                           'maxBytes': 10000000,
                           'backupCount': 5},
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': sys.stdout,
        },
    },
    loggers={
        'custom_logger': {
            'handlers': ['custom_logger', 'console'],
            'level': logging.DEBUG
        }
    }
)

dictConfig(logging_config)

custom_logger = logging.getLogger('custom_logger')