from features.default import BaseFeature
import wikipedia
import sys

class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "search_wikipedia"
        self.patterns = ["wikipedia"]
        self.index

    def action(self, spoken_text):
        search_query = self.get_search_query(spoken_text, self.keywords)
        try:
            results = wikipedia.summary(search_query, sentences = 3)
            bs.respond('According to Wikipedia')
            bs.respond(results)
            return
        except:
            bs.respond('I could not find anything on Wikipedia related to your search.')
            return

    '''
    Parses spoken text to retrieve a search query for Wikipedia
    Argument: <string> spoken_text, <list> keywords
    Return type: <string> spoken_text (this is actually the search query as retrieved from spoken_text.
    '''
    def get_search_query(self, spoken_text, keywords):
        for word in keywords:
            spoken_text = spoken_text.replace(word, '')
        return spoken_text
