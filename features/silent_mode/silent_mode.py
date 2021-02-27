'''Turn on silent mode.'''
from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.silent_mode import shell

class SilentMode(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        # set silent_mode to on
        bs.set_silent_mode(True)
        bs.respond('Welcome to silent mode.')
        return
