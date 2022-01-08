"Centralized location for constants"
import utils.env as env

BUMBLEBEE_ONLINE_BASE_URL_PROD = 'https://c9o8fm.deta.dev'
BUMBLEBEE_ONLINE_BASE_URL_LOCAL = 'http://127.0.0.1:8000'

BUMBLEBEE_ONLINE_BASE_URL = \
    BUMBLEBEE_ONLINE_BASE_URL_LOCAL if \
    env.is_local else BUMBLEBEE_ONLINE_BASE_URL_PROD


BUMBLEBEE_ONLINE_LOGIN_URL = BUMBLEBEE_ONLINE_BASE_URL + '/auth/jwt/login'
BUMBLEBEE_ONLINE_GET_COMMANDS_URL = BUMBLEBEE_ONLINE_BASE_URL + '/commands'

BUMBLEBEE_ONLINE_GET_NEW_API_KEY_URL = \
    BUMBLEBEE_ONLINE_BASE_URL + '/api-key/new'

BUMBLEBEE_ONLINE_GET_ACTIVE_API_KEY_URL = \
    BUMBLEBEE_ONLINE_BASE_URL + '/api-key/active'
