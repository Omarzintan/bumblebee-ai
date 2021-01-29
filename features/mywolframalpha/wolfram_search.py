from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.mywolframalpha import helpers
from database import wolframalpha_key as wak
import wolframalpha
from features.keywords import Keywords
from features.mywikipedia import *
import sys

class WolframalphaSearch(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        search_query = helpers.get_search_query(spoken_text, self.keywords)
        app_id = wak.get_key()
        client = wolframalpha.Client(app_id)
        try:
            bs.respond('Searching Wolframalpha')
            res = client.query(search_query)
            answer = next(res.results).text
            bs.respond('The answer is ' + answer)
        except:
            # Trying Wikipedia
            bs.respond('I found nothing on Wolframalpha. Trying Wikipedia')
            keywords = Keywords()
            wiki_keywords = keywords.get('search_wikipedia')
            wiki_search_obj = wiki_search.WikipediaSearch(wiki_keywords)
            wiki_search_obj.action(spoken_text)
            return
