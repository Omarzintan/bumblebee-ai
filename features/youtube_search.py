from features.default import BaseFeature
from features.feature_helpers import get_search_query
import webbrowser


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "youtube_search"
        self.patterns = [
            "youtube",
            "open a youtube search on",
            "show me a video about",
            "find a video on"
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
            'I have opened YouTube with a search on {}'.format(query)
        )
        return query

    def get_search_query(self, spoken_text, patterns):
        '''
        Parses spoken text to retrieve a search query for Youtube
        Argument: <list> spoken_text (tokenized. i.e. list of words),
        <list> patterns
        Return type: <string> query
        '''
        search_terms = ['about', 'on', 'for', 'search']
        query = get_search_query(
            spoken_text,
            patterns,
            search_terms
        )
        return query

    def search(self, query):
        '''
        Opens YouTube in a browser with the specified search query.
        Argument: <string> query
        Return type: <string> query
        '''
        webbrowser.open(
            "https://www.youtube.com/results?search_query='{}'".format(query)
        )
        return query
