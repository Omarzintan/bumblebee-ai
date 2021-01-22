#!python3
import json, os

# To be Deprecated soon.

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

'''
Get email from the contacts.json file, given a name.
Returns an empty string if the name does not exist.
'''
def get_email(name):
    for contact in data['contacts']:
        if name == contact['name'].lower():
            return contact['email']
    return ''


