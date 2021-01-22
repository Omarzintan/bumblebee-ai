'''Contains all glocal variables. i.e. variables shared with all modules in this folder.'''

import os, json

'''
Open my contacts.json file and load it as json.
'''
f = open(os.environ.get('BUMBLEBEE_PATH')+'database/contacts.json')
data = json.load(f)
