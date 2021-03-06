import logging
from logging.config import dictConfig
import os
import socket

# TODO: Use a config style that is not required at import time
try:
    SERVER_INFO = {
        "host": os.getenv("HLL_HOST"),
        "port": int(os.getenv("HLL_PORT")),
        "password": os.getenv("HLL_PASSWORD")
    }
except ValueError as e:
    raise ValueError("HLL_PORT must be an integer") from e

for k, v in SERVER_INFO.items():
    if not v:
        raise ValueError(f"{k} environment variable must be set")


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s '
                      '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
            },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
            },
        'file': {
            'level': 'DEBUG',
            'formatter': 'console',
            'class': 'logging.FileHandler',
            'filename':  os.path.join(
                os.getenv('LOGGING_PATH', ""),
                os.getenv("LOGGING_FILENAME", f"{socket.gethostname()}.log")
            )
            },
        },

    'loggers': {
        __package__: {
            'handlers': ['console', 'file'],
            'level': os.getenv('LOGGING_LEVEL', 'DEBUG'),
            'propagate': False,
        },
        '__main__': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}


dictConfig(LOGGING)
