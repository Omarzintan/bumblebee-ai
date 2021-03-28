from features.default import BaseFeature
from database import wolframalpha_key as wak
import wolframalpha
from features import wiki_search
import sys

class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "wolfram_search"
        self.patterns = ["calculate", "what is", "how many", "how much", "compute"]
        super().__init__()

    def action(self, spoken_text):
        search_query = self.get_search_query(spoken_text, self.patterns)
        app_id = wak.get_key()
        client = wolframalpha.Client(app_id)
        try:
            res = client.query(search_query, width=200)
            answer = next(res.results).text
            self.bs.respond(answer)
        except:
            # Trying Wikipedia
            wiki_search_obj = wiki_search.Feature()
            wiki_search_obj.action(spoken_text)
            return

    '''
    Parses spoken text to retrieve a search query for Wolframalpha
    Argument: <list> spoken_text (tokenized. i.e. list of words), <list> patterns
    Return type: <string> spoken_text (this is actually the search query as retrieved from spoken_text.)
    '''
    def get_search_query(self, spoken_text, patterns):
        search_terms = patterns
        query_found = False

        for search_term in search_terms:
            if search_term in spoken_text:
                search_index = spoken_text.index(search_term)
                # get everything after the search term
                spoken_text = spoken_text[search_index+1:]
                query_found = True
                break

        # In case none of the search terms are included in spoken_text.
        if not query_found:
            for phrase in patterns:
                # split the phrase into individual words
                phrase_list = phrase.split(' ')
                # remove phrase list from spoken_text
                spoken_text = [word for word in spoken_text if word not in phrase_list]
                
        return ' '.join(spoken_text)
