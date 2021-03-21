'''Turn on silent mode.'''
from features.default import BaseFeature

class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "silent_mode_on"
        self.patterns = ["silent mode", "turn on silent mode", "start silent mode"]
        self.index

    def action(self, spoken_text):
        bs.respond('Okay. Starting silent mode.')
        bs.set_silent_mode(True)
        bs.respond('Welcome to silent mode.')
        return
