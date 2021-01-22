from features.keywords import Keywords
from features.contacts import *
from features.google import *

keywords = Keywords()

getEmail = getemail.GetEmail(['get email'])
google_search = google_search.GoogleSearch(keywords.get('search_google'))

config_actions = [
    getEmail,
    google_search
    ]

 #print(config_actions)
