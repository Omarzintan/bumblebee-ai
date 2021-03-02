'''Turn off silent mode.'''
from features.features import BaseFeature
from features.global_vars import bumble_speech as bs

class SilentModeOff(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        bs.set_silent_mode(False)
        bs.respond('Welcome to voice mode.')
        return
