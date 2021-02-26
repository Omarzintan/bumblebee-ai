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
        print(name)
        link_found, has_password = helpers.open_zoom(name)
        print(link_found, has_password)
        if not link_found:
            bs.respond('I could not find this zoom link.')
            return
        bs.respond('I have opened the zoom link in a browser window.')
        if has_password:
            bs.respond('I have copied the password to the clip board. Press ctrl+v to paste it.')
        return
