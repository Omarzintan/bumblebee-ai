'''Open zoom link in a web browser'''
from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.zoom import glocal_vars, helpers

class OpenZoom(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        # get class name from the query
        # search database for class details (in helpers)
        # if class has password, copy password to clipboard (in helpers)
            # if (has_password(): bs.respond(copied password to clipboard)
        # open zoom link in browser
        pass
