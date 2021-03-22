from features.default import BaseFeature
from database import wolframalpha_key as wak
import wolframalpha
from features import wiki_search
import sys

class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "wolfram_search"
        self.patterns = ["calculate", "what is", "i wonder why", "compute"]
        super().__init__()

    def action(self, spoken_text):
        search_query = self.get_search_query(spoken_text, self.keywords)
        app_id = wak.get_key()
        client = wolframalpha.Client(app_id)
        try:
            res = client.query(search_query, width=200)
            answer = next(res.results).text
            self.bs.respond(answer)
        except:
            # Trying Wikipedia
            #keywords = Keywords()
            #wiki_keywords = keywords.get('search_wikipedia')
            #wiki_search_obj = wiki_search.WikipediaSearch(wiki_keywords)
            wiki_search_obj.action(spoken_text)
            return

    '''
    Parses spoken text to retrieve a search query for Wolframalpha
    Argument: <string> spoken_text, <list> keywords
    Return type: <string> spoken_text (this is actually the search query as retrieved from spoken_text.
    '''
    def get_search_query(self, spoken_text, keywords):
        for word in keywords:
            spoken_text = spoken_text.replace(word, '')
        return spoken_text
