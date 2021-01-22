#!python3
import json, os

'''
Open my contacts.json file and load it as json. ADD TO GLOBALS
'''
f = open(os.environ.get('BUMBLEBEE_PATH')+'database/contacts.json')
data = json.load(f)

'''
Returns all the names in my conctacts.json file.
'''
def get_names():
    names = []
    for contact in data['contacts']:
        names.append(contact['name'].lower())
    return names        

