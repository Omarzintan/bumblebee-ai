#!python3
from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.youtube import helpers


class YoutubeSearch(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        query = helpers.search(spoken_text, self.keywords)
        bs.respond('I have opened YouTube with a search on {}'.format(query)) 
        return
