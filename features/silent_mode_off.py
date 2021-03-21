'''Turn off silent mode.'''
from features.default import BaseFeature

class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "silent_mode_off"
        self.patterns = ["turn off silent mode", "voice mode", "exit silent mode", "stop silent mode"]
        self.index

    def action(self, spoken_text):
        bs.set_silent_mode(False)
        bs.respond('Welcome to voice mode.')
        return
