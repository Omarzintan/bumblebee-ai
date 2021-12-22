import os
import logging
import subprocess
from colorlog import ColoredFormatter
from halo import Halo


def get_logger(
    name,
    with_formatting=True,
    dest=None,
    format_string=None,
    log_level=logging.DEBUG
):
    '''
    Get logger with specific format string. Raises exception if error occurs.
    Sources: https://www.machinelearningplus.com/python/python-logging-guide/,
    https://docs.python.org/3/howto/logging.html
    '''
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    default_log_format = '%(log_color)s%(levelname)s: [%(name)s]: %(message)s'

    handler = None
    try:
        if dest:
            handler = logging.FileHandler(dest)
        else:
            handler = logging.StreamHandler()  # default to console
    except Exception as e:
        raise e

    if with_formatting or format_string:
        log_format = format_string if format_string else default_log_format
        formatter = ColoredFormatter(log_format)  # create formatter
        handler.setFormatter(formatter)  # set formatter

    logger.addHandler(handler)
    return logger


logger = get_logger(__name__)


def get_root_directory():
    '''
    Gets the root directory of the project.
    Source:
    https://www.kite.com/python/answers/how-to-get-the-path-of-the-root-project-structure-in-python
    '''
    bumblebee_root_dir = os.getenv('BUMBLEBEE_PATH')
    if not bumblebee_root_dir:
        logger.debug(
            """No BUMBLEBEE_PATH is set in environment.
             Computing root directory instead.""")
        top_level_filename = "main.py"
        bumblebee_root_dir = os.path.dirname(
            os.path.abspath(top_level_filename)
        )
        return bumblebee_root_dir + "/"
    return bumblebee_root_dir


def get_python3_path():
    '''Gets the python3 path which Bumblebee is using to run.'''
    python3_path = os.getenv("PYTHON3_PATH")
    if not python3_path:
        logger.debug(
            """No PYTHON3_PATH is set in environment.
            Computing path using 'which python' instead."""
        )
        python3_path = subprocess.check_output(
            ["which", "python3.7"]
        ).decode('utf-8').strip()
    return python3_path


bumblebee_root = get_root_directory()
python3_path = get_python3_path()

spinner = Halo(spinner='dots2')
