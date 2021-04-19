import os
import logging
from colorlog import ColoredFormatter

def get_logger(name, with_formatting=True, dest=None, format_string=None, log_level=logging.DEBUG):
    '''Get logger with specific format string. Raises exception if error occurs.
    Sources: https://www.machinelearningplus.com/python/python-logging-guide/, 
    https://docs.python.org/3/howto/logging.html
    '''
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    default_log_format = '%(log_color)s%(levelname)s: [%(name)s]: %(message)s'

    handler = None
    try:
        handler = logging.FileHandler(dest) if dest else logging.StreamHandler() # default to console
    except Exception as e:
       raise e

    if with_formatting or format_string:
        log_format = format_string if format_string else default_log_format
        formatter = ColoredFormatter(log_format) # create formatter
        handler.setFormatter(formatter) # set formatter
        
    logger.addHandler(handler)
    return logger

logger  = get_logger(__name__)

def get_root_directory():
    '''Gets the root directory of the project. Source: https://www.kite.com/python/answers/how-to-get-the-path-of-the-root-project-structure-in-python'''
    top_level_filename = "main.py"
    bumblebee_root_dir = os.path.dirname(os.path.abspath(top_level_filename))
        
    return bumblebee_root_dir + "/" 

bumblebee_root = get_root_directory()
