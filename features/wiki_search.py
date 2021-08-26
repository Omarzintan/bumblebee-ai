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

    def action(self, spoken_text, arguments_list: list = []):
        search_query = self.get_search_query(spoken_text, self.patterns)
        try:
            results = wikipedia.summary(search_query, sentences=2)
            self.bs.respond('According to Wikipedia, ' + results)
            return
        except wikipedia.exceptions.PageError:
            self.bs.respond('I could not find any pages '
                            'related to your search.')
        except wikipedia.exceptions.DisambiguationError:
            self.bs.respond('Please be more specific in your '
                            'search as there are a couple of'
                            'other options meaning the same.')
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
