'''
This file is for retrieving system environment variables and helper
variables directly derived from them.
'''
from dotenv import load_dotenv
import os

load_dotenv()

environment = os.environ.get('BUMBLEBEE_ENV', 'production')
is_local = environment == 'local'
