'''Contains all glocal variables. i.e. variables shared with all modules in this folder.'''

import os, json
from helpers import bumblebee_root

'''
Open my contacts.json file and load it as json.
'''
f = open(bumblebee_root+'database/contacts.json')
data = json.load(f)
