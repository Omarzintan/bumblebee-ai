from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.grepapp import helpers

class GrepappSearch(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        query = helpers.search(spoken_text, self.keywords)
        bs.respond('I have opened a browser with you grepapp search')
        return
