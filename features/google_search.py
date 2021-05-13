#!python3
from features.default import BaseFeature
import webbrowser


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "google_search"
        self.patterns = [
            "google",
            "open a google search on",
            "google search",
            "show me on google"
        ]
        super().__init__(bumblebee_api)

    def action(self, spoken_text):
        query = self.search(spoken_text, self.patterns)
        self.bs.respond(
            'I have opened a browser window with your search on {}.'
            .format(query))
        return

    '''
    Parses spoken text to retrieve a search query for Google
    Argument: <list> spoken_text (tokenized. i.e. list of words),
              <list> patterns
    Return type: <string> spoken_text (this is actually the search query
    as retrieved from spoken_text.)
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

        # In case none of the search terms are included in spoken_text.
        if not query_found:
            for phrase in patterns:
                # split the phrase into individual words
                phrase_list = phrase.split(' ')
                # remove phrase list from spoken_text
                spoken_text = [
                    word for word in spoken_text if word not in phrase_list
                ]

        return ' '.join(spoken_text)

    '''
    Opens up google search in browser with search string.
    Argument: <string> spoken_text, <list> patterns
    Return type: <string> query
    '''

    def search(self, spoken_text, patterns):
        query = self.get_search_query(spoken_text, patterns)
        webbrowser.open("https://google.com/search?q={}".format(query))
        return query
