#!python3
import json, os
import sys
import logging
from helpers import get_root_directory, get_logger

logger = get_logger(__name__)

'''
Open my contacts.json file and load it as json. ADD TO GLOBALS
'''
empty_data_dict = {
    "contacts": []
}

try:
    f = open(get_root_directory()+'database/contacts.json')
    data = json.load(f)
except Exception as e:
    data = empty_data_dict
    logger.warning('No contacts.json found in database directory. Contacts feature may not work as expected.')

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


