#!python3
from features.default import BaseFeature
import webbrowser


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "youtube_search"
        self.patterns = ["youtube", "open a youtube search on", "show me a video about", "find a video on"]
        super().__init__()

    def action(self, spoken_text):
        query = self.search(spoken_text)
        self.bs.respond('I have opened YouTube with a search on {}'.format(query)) 
        return

    '''
    Parses spoken text to retrieve a search query for Youtube
    Argument: <list> spoken_text (tokenized. i.e. list of words), <list> patterns
    Return type: <string> spoken_text (this is actually the search query as retrieved from spoken_text.)
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
                spoken_text = [word for word in spoken_text if word not in phrase_list]

        return ' '.join(spoken_text)

    '''
    Opens YouTube in a browser with the specified search query.
    Argument: <string> spoken_text, <list> keywords
    Return type: <string> query
    '''
    def search(self, spoken_text):
        query = self.get_search_query(spoken_text, self.patterns)
        webbrowser.open("https://www.youtube.com/results?search_query='{}'".format(query))
        return query
