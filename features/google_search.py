from features.default import BaseFeature
from features.feature_helpers import get_search_query
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
        self.bs = bumblebee_api.get_speech()

    def action(self, spoken_text, arguments_list: list = []):
        if arguments_list:
            for argument in arguments_list:
                self.search(argument)
            self.bs.respond(
                f"I have opened browser tabs for the following search terms \
                 {arguments_list}")
            return arguments_list
        query = self.search(self.get_search_query(spoken_text, self.patterns))
        self.bs.respond(
            'I have opened a browser window with your search on {}.'
            .format(query))
        return query

    def get_search_query(self, spoken_text, patterns):
        '''
        Parses spoken text to retrieve a search query for Google
        Argument: <list> spoken_text (tokenized. i.e. list of words) OR
                <str> spoken_text (not tokenized),
                <list> patterns
        Return type: <string> spoken_text (this is actually the search query
        as retrieved from spoken_text.)
        '''
        search_terms = ['about', 'on', 'for', 'search']
        query = get_search_query(
            spoken_text,
            patterns,
            search_terms
        )
        return query

    '''
    Opens up google search in browser with search string.
    Argument: <string> query
    Return type: <string> query
    '''

    def search(self, query):
        webbrowser.open("https://google.com/search?q={}".format(query))
        return query
