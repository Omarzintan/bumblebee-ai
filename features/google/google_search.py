#!python3

import webbrowser as wb
from features.features import BaseFeature
from features.global_vars import bumble_speech

class GoogleSearch(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords
        
    '''
    Opens up google search in browser with search string.
    Argument: <string> search
    Return type: None
    '''
    def action(self, spoken_text):
        for word in self.keywords:
            spoken_text = spoken_text.replace(word, '')
        wb.open('https://google.com/search?q={}'.format(spoken_text))
        bumble_speech.respond('I have opened a browser window with your search on {}.'.format(spoken_text))
