'''
This file is for retrieving system environment variables and helper
variables directly derived from them.

In decreasing order of precedence, environment variables can be set by:
1. adding them to .env file at root of this project
2. exporting and then running bumblebee in then same terminal.
   E.g. export BUMBLEBEE_ENV=local; bumblebee
3. prefixing 'bumblebee' command with the environment variable when running.
   E.g. BUMBLEBEE_ENV=local bumblebee
'''
from dotenv import load_dotenv
import os

load_dotenv()

environment = os.environ.get('BUMBLEBEE_ENV', 'production')
is_local = environment == 'local'
