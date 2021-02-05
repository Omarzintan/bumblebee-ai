from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.mywikipedia import helpers
import wikipedia
import sys

class WikipediaSearch(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        search_query = helpers.get_search_query(spoken_text, self.keywords)
        try:
            results = wikipedia.summary(search_query, sentences = 3)
            bs.respond('According to Wikipedia')
            bs.respond(results)
            return
        except:
            bs.respond('I could not find anything on Wikipedia related to your search.')
            return
