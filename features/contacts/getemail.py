from features.features import BaseFeature
from features.global_vars import *
from features.contacts import glocal_vars
# USES DATA GLOBAL VAR
# Not actually a feature. This is just a helper function.

class GetEmail(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    '''
    Get email from the contacts.json file, given a name.
    Returns an empty string if the name does not exist.
    '''
    def action(self, name):
        print('action reached')
        print(glocal_vars.data) #printing glocal var works
        for contact in glocal_vars.data['contacts']:
            if name == contact['name'].lower():
                return contact['email']
        return ''

