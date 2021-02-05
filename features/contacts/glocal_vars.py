'''Contains all glocal variables. i.e. variables shared with all modules in this folder.'''

import os, json
from helpers import get_root_directory

'''
Open my contacts.json file and load it as json.
'''
f = open(get_root_directory()+'database/contacts.json')
data = json.load(f)
