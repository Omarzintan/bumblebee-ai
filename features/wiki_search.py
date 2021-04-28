from features.default import BaseFeature
import wikipedia
import sys


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "wiki_search"
        self.patterns = [
            "wikipedia",
            "search wikipedia for",
            "look up on wikipedia"
            ]
        super().__init__()

    def action(self, spoken_text):
        search_query = self.get_search_query(spoken_text, self.patterns)
        try:
            results = wikipedia.summary(search_query, sentences=2)
            self.bs.respond('According to Wikipedia')
            self.bs.respond(results)
            return
        except:
            self.bs.respond('I could not find anything on Wikipedia '
                            'related to your search.')
            return

    '''
    Parses spoken text to retrieve a search query for Wikipedia
    Argument: <string> spoken_text (tokenized. i.e. list of words),
              <list> patterns
    Return type: <string> spoken_text (this is actually the search query
    as retrieved from spoken_text.
    '''
    def get_search_query(self, spoken_text, patterns):
        search_terms = ['about', 'on', 'for', 'search']
        query_found = False

        for search_term in search_terms:
            if search_term in spoken_text:
                search_index = spoken_text.index(search_term)
                # get everything after the search term
                spoken_text = spoken_text[search_index+1:]
                query_found = True
                break

        if not query_found:
            for phrase in patterns:
                # split the phrase into individual words
                phrase_list = phrase.split(' ')
                # remove phrase list from spoken_text
                spoken_text = [
                    word for word in spoken_text if word not in phrase_list
                    ]

        return ' '.join(spoken_text)
