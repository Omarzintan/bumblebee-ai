'''Open zoom link in a web browser'''
from features.default import BaseFeature
from features.feature_helpers import get_search_query
from tinydb import TinyDB, Query
import pyperclip as pc
import webbrowser


class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "open_zoom_link"
        self.patterns = ["take me to", "time for class"]
        super().__init__()

        zoom_db_path = self.config['Database']['zoom']
        self.zoom_db = TinyDB(zoom_db_path)

    def action(self, spoken_text):
        # get class name from the query
        name = self.get_search_query(spoken_text)
        # open zoom link in browser
        link_found, has_password = self.open_zoom(name.lower())
        if not link_found:
            self.bs.respond('I could not find this zoom link.')
            return
        self.bs.respond('I have opened the zoom link in a browser window.')
        if has_password:
            self.bs.respond(
                'I have copied the password to the clip board.'
                'Press ctrl+v to paste it.'
            )
        return

    def search_db(self, name):
        '''Searches for specific item based on its name'''
        Item = Query()
        results_list = self.zoom_db.search(Item.name == name)
        return results_list

    def open_zoom(self, name):
        '''
        Opens zoom link based on given name.
        Arguments: <string> name
        Return type: <boolean> found, <boolean> has_password
        '''
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

    def get_search_query(self, spoken_text):
        '''
        Parse spoken text to retrieve a search query for Zoom.
        e.g. spoken_text: I would like to go to french class
        query = french class
        '''
        search_terms = ['to', 'for']
        search_query = get_search_query(
            spoken_text,
            self.patterns,
            search_terms
        )
        return search_query
