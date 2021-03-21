'''Open zoom link in a web browser'''
from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.zoom import helpers

class OpenZoom(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        # get class name from the query
        name = helpers.get_search_query(spoken_text, self.keywords)
        # open zoom link in browser
        link_found, has_password = helpers.open_zoom(name.lower())
        if not link_found:
            bs.respond('I could not find this zoom link.')
            return
        bs.respond('I have opened the zoom link in a browser window.')
        if has_password:
            bs.respond('I have copied the password to the clip board. Press ctrl+v to paste it.')
        return


    '''Searches for specific item based on its name'''
    def search_db(self, name):
        global zoom_db # FIND A WAY TO ACCESS ZOOM DB FROM CONFIG FILE
        Item = Query()
        results_list = zoom_db.search(Item.name == name)
        return results_list

    '''
    Opens zoom link based on given name.
    Arguments: <string> name
    Return type: <boolean> found, <boolean> has_password
    '''
    def open_zoom(name):
        has_password = False
        found = False

        search_results = search_db(name)
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
    Arguments: <string> spoken_text, <list> keywords
    Return type: <string> spoken_text (now stripped down to only the search query.)
    '''
    def get_search_query(spoken_text, keywords):
        for word in keywords:
            spoken_text = spoken_text.replace(word, '')
            # Need to remove whitespace before and after the wanted query, otherwise the zoom_db search will return nothing.
        spoken_text = spoken_text.strip()
        return spoken_text
