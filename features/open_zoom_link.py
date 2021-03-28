'''Open zoom link in a web browser'''
from features.default import BaseFeature
from tinydb import TinyDB, Query
import pyperclip as pc
import webbrowser
import os


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "open_zoom_link"
        self.patterns = ["take me to", "time for class"]
        super().__init__()

        # self.config is defined in BaseFeature class
        zoom_db_path = self.config['Databases']['zoom']
        self.zoom_db = TinyDB(zoom_db_path)
        
    def action(self, spoken_text):
        # get class name from the query
        name = self.get_search_query(spoken_text, self.patterns)
        # open zoom link in browser
        link_found, has_password = self.open_zoom(name.lower())
        if not link_found:
            self.bs.respond('I could not find this zoom link.')
            return
        self.bs.respond('I have opened the zoom link in a browser window.')
        if has_password:
            self.bs.respond('I have copied the password to the clip board. Press ctrl+v to paste it.')
        return


    '''Searches for specific item based on its name'''
    def search_db(self, name):
        Item = Query()
        results_list = self.zoom_db.search(Item.name == name)
        return results_list

    '''
    Opens zoom link based on given name.
    Arguments: <string> name
    Return type: <boolean> found, <boolean> has_password
    '''
    def open_zoom(self, name):
        has_password = False
        found = False

        search_results = self.search_db(name)
        if not search_results:
            return found, has_password

        found = True
        # current policy is to use the first search result from search_db
        result = search_results[0]
        if result['password']:
            has_password = True
            # copy password to clipboard
            pc.copy(result.password)
            
        webbrowser.open(result['link'])
        return found, has_password

    '''
    Parse spoken text to retrieve a search query for Zoom.
    Arguments: <string> spoken_text, <list> patterns
    Return type: <string> spoken_text (now stripped down to only the search query.)
    '''
    def get_search_query(self, spoken_text, patterns):
        search_terms = ['to', 'for']
        false_search_term_indicators = ['like', 'love', 'ready', 'want']
        query_found = False

        for search_term in search_terms:
            if search_term in spoken_text:
                search_index = spoken_text.index(search_term)
                # ignore cases with "like to", "love to" "ready to"
                if spoken_text[search_index-1] in false_search_term_indicators:
                    # looking for the search term in rest of text after the false search term indicator.
                    search_index = spoken_text[search_index+1:].index(search_term)
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


        spoken_text = ' '.join(spoken_text)
        # Need to remove whitespace before and after the wanted query, otherwise the zoom_db search will return nothing.
        spoken_text = spoken_text.strip()
        print(spoken_text)
        return spoken_text
