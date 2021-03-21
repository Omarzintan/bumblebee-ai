#!python3
from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.google import helpers
import webbrowser

class GoogleSearch(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords
        
    def action(self, spoken_text):
        query = self.search(spoken_text, self.keywords)
        bs.respond('I have opened a browser window with your search on {}.'.format(query))
        return



    '''
    Parses spoken text to retrieve a search query for Google
    Argument: <string> spoken_text, <list> keywords
    Return type: <string> spoken_text (this is actually the search query as retrieved from spoken_text.
    '''
    def get_search_query(spoken_text, keywords):
        for word in keywords:
            spoken_text = spoken_text.replace(word, '')
        return spoken_text

    '''
    Opens up google search in browser with search string.
    Argument: <string> spoken_text, <list> keywords
    Return type: <string> query
    '''
    def search(spoken_text, keywords):
        query = get_search_query(spoken_text, keywords)
        webbrowser.open("https://google.com/search?q={}".format(query))
        return query
