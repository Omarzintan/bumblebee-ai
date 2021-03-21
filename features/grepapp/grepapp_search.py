from features.default import BaseFeature
from features.global_vars import bumble_speech as bs
import webbrowser

class Feature(BaseFeature):
    def __init__(self, keywords):
        self.tag_name = "search_grepapp"
        self.patterns = ["grep search", "search github", "do a grep search", "search on github"]
        self.index

    def action(self, spoken_text):
        query = self.search(spoken_text, self.keywords)
        bs.respond('I have opened a browser with your grepapp search')
        return

    '''
    Parses spoken text to retrieve a search query for YouTube
    Argument: <string> spoken_text, <list> keywords
    Return type: <string> spoken_text (this is actually the search query as retrieved from spoken_text.
    '''
    def get_search_query(self, spoken_text, keywords):
        for word in keywords:
            spoken_text = spoken_text.replace(word, '')
        return spoken_text

    '''
    Opens up a grep.app search in browser.
    Argument: <string> spoken_text, <list> keywords
    Return type: <string> query
    '''
    def search(self, spoken_text, keywords):
        query = get_search_query(spoken_text, keywords)
        webbrowser.open('https://grep.app/search?q={}'.format(query))
        return query
    
