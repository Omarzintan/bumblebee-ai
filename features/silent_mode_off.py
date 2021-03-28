'''Turn off silent mode.'''
from features.default import BaseFeature

class Feature(BaseFeature):
    def __init__(self):
        self.tag_name = "silent_mode_off"
        self.patterns = ["turn off silent mode", "voice mode", "exit silent mode", "stop silent mode"]
        super().__init__()

    def action(self, spoken_text):
        self.bs.set_silent_mode(False)
        self.bs.respond('Welcome to voice mode.')
        return
