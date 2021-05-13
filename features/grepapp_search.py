from features.default import BaseFeature
import webbrowser


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "grepapp_search"
        self.patterns = [
            "grep search",
            "search github",
            "do a grep search",
            "search on github"
        ]
        self.bs = bumblebee_api.get_speech()

    def action(self, spoken_text):
        query = self.search(spoken_text)
        self.bs.respond(
            f'I have opened a browser with your grepapp search on {query}')
        return

    '''
    Parses spoken text to retrieve a search query for Grepapp
    Argument: <list> spoken_text (tokenized. i.e. list of words),
              <list> patterns
    Return type: <string> spoken_text (this is actually the search
    query as retrieved from spoken_text.)
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

    def search(self, spoken_text):
        '''
        Opens up a grep.app search in browser.
        Argument: <string> spoken_text, <list> keywords
        Return type: <string> query
        '''
        query = self.get_search_query(spoken_text, self.patterns)
        webbrowser.open('https://grep.app/search?q={}'.format(query))
        return query
