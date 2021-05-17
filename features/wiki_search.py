from features.default import BaseFeature
from features.feature_helpers import get_search_query
import wikipedia


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "wiki_search"
        self.patterns = [
            "wikipedia",
            "search wikipedia for",
            "look up on wikipedia"
        ]
        self.bs = bumblebee_api.get_speech()

    def action(self, spoken_text):
        search_query = self.get_search_query(spoken_text, self.patterns)
        try:
            results = wikipedia.summary(search_query, sentences=2)
            self.bs.respond('According to Wikipedia')
            self.bs.respond(results)
            return
        except Exception:
            self.bs.respond('I could not find anything on Wikipedia '
                            'related to your search.')
            return

    def get_search_query(self, spoken_text, patterns):
        '''
        Parses spoken text to retrieve a search query for Wikipedia
        Argument: <string> spoken_text (tokenized. i.e. list of words),
                <list> patterns
        Return type: <string> spoken_text (this is actually the search query
        as retrieved from spoken_text.
        '''
        search_terms = ['about', 'on', 'for', 'search']
        query = get_search_query(
            spoken_text,
            patterns,
            search_terms
        )
        return query
