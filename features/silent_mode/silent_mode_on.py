'''Turn on silent mode.'''
from features.features import BaseFeature
from features.global_vars import bumble_speech as bs

class SilentModeOn(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        bs.respond('Okay. Starting silent mode.')
        bs.set_silent_mode(True)
        bs.respond('Welcome to silent mode.')
        return
