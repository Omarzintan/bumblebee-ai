import os, json

'''
Open my contacts.json file and load it as json. ADD TO GLOBALS
'''
f = open(os.environ.get('BUMBLEBEE_PATH')+'database/contacts.json')
data = json.load(f)
