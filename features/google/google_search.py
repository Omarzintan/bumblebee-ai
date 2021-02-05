#!python3
from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.google import helpers

class GoogleSearch(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords
        
    def action(self, spoken_text):
        query = helpers.search(spoken_text, self.keywords)
        bs.respond('I have opened a browser window with your search on {}.'.format(query))
        return
