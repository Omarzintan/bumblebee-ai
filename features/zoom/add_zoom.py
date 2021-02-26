from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.zoom import helpers
import sys

class AddZoom(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        try:
            helpers.add_zoom_details()
            bs.respond('Added zoom link successfully.')
        except:
            print(sys.exc_info())
            bs.respond('Could not add zoom link.')

        return
    
