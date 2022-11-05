import logging

import coloredlogs


def log_function(func):
    def logged_function(*args, **kwargs):
        logging.debug(f"{func.__name__} started")
        result = func(*args, **kwargs)
        logging.debug(f"{func.__name__} finished")
        return result

    return logged_function


def init(level=logging.INFO):
    coloredlogs.DEFAULT_FIELD_STYLES = dict(
        asctime=dict(color='white'),
        hostname=dict(color='magenta'),
        levelname=dict(color='blue'),
        name=dict(color='blue'),
        programname=dict(color='cyan'),
        username=dict(color='yellow'),
        filename=dict(color='white', faint=True),
        lineno=dict(color='white', faint=True),
    )

    coloredlogs.DEFAULT_LEVEL_STYLES = dict(
        spam=dict(color='green', faint=True),
        debug=dict(color='white', faint=True),
        verbose=dict(color='blue', faint=True),
        info=dict(color='green', bold=True),
        notice=dict(color='magenta', bold=True),
        warning=dict(color='yellow', bold=True),
        success=dict(color='green', bold=True),
        error=dict(color='red', bold=True),
        critical=dict(color='red', bold=True),
    )
    coloredlogs.DEFAULT_LOG_LEVEL = level
    coloredlogs.DEFAULT_LOG_FORMAT = '%(asctime)s %(levelname).4s %(filename)s:%(lineno)d %(message)s'
    coloredlogs.DEFAULT_DATE_FORMAT = '%H:%M:%S'
    coloredlogs.install()
