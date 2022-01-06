import os
import logging
import stdiomask
import requests
import subprocess
from colorlog import ColoredFormatter
from halo import Halo


BUMBLEBEE_ONLINE_API_KEY_FILENAME = 'bumblebee_token'
BUMBLEBEE_ONLINE_GET_API_KEY_URL = "https://c9o8fm.deta.dev/api-key/new"
BUMBLEBEE_ONLINE_LOGIN_URL = "https://c9o8fm.deta.dev/auth/jwt/login"
TEST_URL_BUMBLEBEE_LOGIN = "http://127.0.0.1:8000/api-key/new"
TEST_URL_GET_BUMBLEBEE_API_KEY = "http://127.0.0.1:8000/api-key/new"


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


def log_user_in():
    '''
    Allows user to login to Bumblebee Online account.
    '''
    decision_prompt = """
Enter the number of the desired option to proceed:
1. Log in
2. Skip
Note: To log in, you need to have signed up for an account
on Bumblebee Online here: https://c9o8fm.deta.dev/
"""
    print(decision_prompt)
    while True:
        decision = input("type here:")
        if decision == '1':
            # Get username
            username = input("Email:")
            # Get password
            password = stdiomask.getpass()
            # Send post req to Bumblebee online to log user in.
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            payload = {
                "username": username,
                "password": password,
            }
            try:
                response = requests.post(TEST_URL_BUMBLEBEE_LOGIN,
                                         headers=headers, data=payload)
                if response.status_code == 200:
                    return response.json().get("access_token")
                return
            except(requests.ConnectionError):
                print("Failed to connect to server.")
                return
        elif decision == '2':
            print("Log in skipped.")
            return
        else:
            print("Please enter 1 or 2 to proceed")


def get_api_key(jwt: str = None):
    '''
    Gets Bumblebee Online Api Key for a logged in user.
    '''
    # Use jwt token to ask for api key from Bumblebee Online
    # api.
    headers = {"Authorization": f"Bearer {jwt}"}
    response = requests.post(TEST_URL_GET_BUMBLEBEE_API_KEY, headers=headers)
    # Store the api key in a file locally under a specified
    # BUMBLEBEE_ONLINE_API_KEY filename.
    if response.status_code == 200:
        with open(
                bumblebee_root+BUMBLEBEE_ONLINE_API_KEY_FILENAME, "w") as file:
            file.write(response.json().get("value"))
    return response.status_code


spinner = Halo(spinner='dots2')
